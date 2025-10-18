import json
import asyncio
from datetime import datetime
from typing import Dict, Any
import paho.mqtt.client as mqtt
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import SessionLocal
from app.models.device import Device, SensorData, Alert
from app.services.websocket_manager import manager

class MQTTService:
    def __init__(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        
    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected to MQTT broker with result code {rc}")
        client.subscribe("devices/+/data")
        client.subscribe("devices/+/status")
        client.subscribe("devices/+/alerts")
    
    def on_message(self, client, userdata, msg):
        try:
            topic_parts = msg.topic.split('/')
            device_id = topic_parts[1]
            message_type = topic_parts[2]
            
            payload = json.loads(msg.payload.decode())
            
            db = SessionLocal()
            try:
                if message_type == "data":
                    self.handle_sensor_data(db, device_id, payload)
                elif message_type == "status":
                    self.handle_device_status(db, device_id, payload)
                elif message_type == "alerts":
                    self.handle_device_alert(db, device_id, payload)
            finally:
                db.close()
                
        except Exception as e:
            print(f"Error processing MQTT message: {e}")
    
    def handle_sensor_data(self, db: Session, device_id: str, payload: Dict[str, Any]):
        # Update device last_seen
        device = db.query(Device).filter(Device.device_id == device_id).first()
        if device:
            device.last_seen = datetime.utcnow()
            device.status = "online"
        
        # Store sensor data
        sensor_data = SensorData(
            device_id=device_id,
            sensor_type=payload.get("sensor_type"),
            value=payload.get("value"),
            unit=payload.get("unit")
        )
        db.add(sensor_data)
        db.commit()
        
        # Send real-time update via WebSocket
        asyncio.create_task(manager.broadcast_sensor_data({
            "device_id": device_id,
            "sensor_type": payload.get("sensor_type"),
            "value": payload.get("value"),
            "timestamp": datetime.utcnow().isoformat()
        }))
    
    def handle_device_status(self, db: Session, device_id: str, payload: Dict[str, Any]):
        device = db.query(Device).filter(Device.device_id == device_id).first()
        if device:
            device.status = payload.get("status", "unknown")
            device.last_seen = datetime.utcnow()
            db.commit()
            
            # Send real-time update via WebSocket
            asyncio.create_task(manager.broadcast_device_status({
                "device_id": device_id,
                "status": device.status,
                "last_seen": device.last_seen.isoformat()
            }))
    
    def handle_device_alert(self, db: Session, device_id: str, payload: Dict[str, Any]):
        alert = Alert(
            device_id=device_id,
            alert_type=payload.get("alert_type"),
            message=payload.get("message"),
            severity=payload.get("severity", "info")
        )
        db.add(alert)
        db.commit()
        
        # Send real-time alert via WebSocket
        asyncio.create_task(manager.broadcast_alert({
            "device_id": device_id,
            "alert_type": alert.alert_type,
            "message": alert.message,
            "severity": alert.severity,
            "timestamp": alert.created_at.isoformat()
        }))
    
    def start(self):
        self.client.connect(settings.mqtt_broker, settings.mqtt_port, 60)
        self.client.loop_start()
    
    def stop(self):
        self.client.loop_stop()
        self.client.disconnect()

mqtt_service = MQTTService()