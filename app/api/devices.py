from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from datetime import datetime, timedelta
from app.core.database import get_db
from app.models.device import Device, SensorData, Alert, FirmwareUpdate
from app.schemas.device import (
    Device as DeviceSchema, DeviceCreate, DeviceUpdate,
    SensorData as SensorDataSchema, SensorDataCreate,
    Alert as AlertSchema, AlertCreate,
    FirmwareUpdate as FirmwareUpdateSchema, FirmwareUpdateCreate
)

router = APIRouter()

@router.post("/", response_model=DeviceSchema)
def create_device(device: DeviceCreate, db: Session = Depends(get_db)):
    db_device = db.query(Device).filter(Device.device_id == device.device_id).first()
    if db_device:
        raise HTTPException(status_code=400, detail="Device already registered")
    
    db_device = Device(**device.dict())
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device

@router.get("/", response_model=List[DeviceSchema])
def get_devices(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    device_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Device)
    
    if status:
        query = query.filter(Device.status == status)
    if device_type:
        query = query.filter(Device.device_type == device_type)
    
    devices = query.offset(skip).limit(limit).all()
    return devices

@router.get("/{device_id}", response_model=DeviceSchema)
def get_device(device_id: str, db: Session = Depends(get_db)):
    device = db.query(Device).filter(Device.device_id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device

@router.put("/{device_id}", response_model=DeviceSchema)
def update_device(device_id: str, device_update: DeviceUpdate, db: Session = Depends(get_db)):
    device = db.query(Device).filter(Device.device_id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    for field, value in device_update.dict(exclude_unset=True).items():
        setattr(device, field, value)
    
    db.commit()
    db.refresh(device)
    return device

@router.delete("/{device_id}")
def delete_device(device_id: str, db: Session = Depends(get_db)):
    device = db.query(Device).filter(Device.device_id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    db.delete(device)
    db.commit()
    return {"message": "Device deleted successfully"}

@router.post("/{device_id}/sensor-data", response_model=SensorDataSchema)
def add_sensor_data(device_id: str, sensor_data: SensorDataCreate, db: Session = Depends(get_db)):
    device = db.query(Device).filter(Device.device_id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    db_sensor_data = SensorData(**sensor_data.dict())
    db.add(db_sensor_data)
    
    # Update device last_seen
    device.last_seen = datetime.utcnow()
    device.status = "online"
    
    db.commit()
    db.refresh(db_sensor_data)
    return db_sensor_data

@router.get("/{device_id}/sensor-data", response_model=List[SensorDataSchema])
def get_sensor_data(
    device_id: str,
    sensor_type: Optional[str] = None,
    hours: int = Query(24, description="Hours of data to retrieve"),
    db: Session = Depends(get_db)
):
    since = datetime.utcnow() - timedelta(hours=hours)
    query = db.query(SensorData).filter(
        SensorData.device_id == device_id,
        SensorData.timestamp >= since
    )
    
    if sensor_type:
        query = query.filter(SensorData.sensor_type == sensor_type)
    
    return query.order_by(desc(SensorData.timestamp)).all()

@router.post("/{device_id}/alerts", response_model=AlertSchema)
def create_alert(device_id: str, alert: AlertCreate, db: Session = Depends(get_db)):
    device = db.query(Device).filter(Device.device_id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    db_alert = Alert(**alert.dict())
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert

@router.get("/{device_id}/alerts", response_model=List[AlertSchema])
def get_device_alerts(
    device_id: str,
    resolved: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Alert).filter(Alert.device_id == device_id)
    
    if resolved is not None:
        query = query.filter(Alert.is_resolved == resolved)
    
    return query.order_by(desc(Alert.created_at)).all()

@router.put("/alerts/{alert_id}/resolve")
def resolve_alert(alert_id: int, db: Session = Depends(get_db)):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    alert.is_resolved = True
    db.commit()
    return {"message": "Alert resolved successfully"}