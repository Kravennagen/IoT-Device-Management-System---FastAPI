import json
from app.services.mqtt_service import mqtt_service

async def initiate_firmware_update(device_id: str, version: str, file_url: str):
    """Send firmware update command to device via MQTT"""
    update_command = {
        "command": "firmware_update",
        "version": version,
        "download_url": file_url,
        "timestamp": "2024-01-01T00:00:00Z"
    }
    
    topic = f"devices/{device_id}/commands"
    mqtt_service.client.publish(topic, json.dumps(update_command))
    
    print(f"Firmware update command sent to device {device_id}")