from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class DeviceBase(BaseModel):
    device_id: str
    name: str
    device_type: str
    firmware_version: Optional[str] = None

class DeviceCreate(DeviceBase):
    pass

class DeviceUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[str] = None
    firmware_version: Optional[str] = None

class Device(DeviceBase):
    id: int
    status: str
    last_seen: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True

class SensorDataBase(BaseModel):
    sensor_type: str
    value: float
    unit: Optional[str] = None

class SensorDataCreate(SensorDataBase):
    device_id: str

class SensorData(SensorDataBase):
    id: int
    device_id: str
    timestamp: datetime

    class Config:
        from_attributes = True

class AlertBase(BaseModel):
    alert_type: str
    message: str
    severity: str = "info"

class AlertCreate(AlertBase):
    device_id: str

class Alert(AlertBase):
    id: int
    device_id: str
    is_resolved: bool
    created_at: datetime

    class Config:
        from_attributes = True

class FirmwareUpdateBase(BaseModel):
    version: str
    device_type: str
    file_url: str
    changelog: Optional[str] = None

class FirmwareUpdateCreate(FirmwareUpdateBase):
    pass

class FirmwareUpdate(FirmwareUpdateBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True