from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Device(Base):
    __tablename__ = "devices"
    
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    device_type = Column(String, nullable=False)
    status = Column(String, default="offline")
    firmware_version = Column(String)
    last_seen = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    sensor_data = relationship("SensorData", back_populates="device")
    alerts = relationship("Alert", back_populates="device")

class SensorData(Base):
    __tablename__ = "sensor_data"
    
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, ForeignKey("devices.device_id"))
    sensor_type = Column(String, nullable=False)
    value = Column(Float, nullable=False)
    unit = Column(String)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    device = relationship("Device", back_populates="sensor_data")

class Alert(Base):
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, ForeignKey("devices.device_id"))
    alert_type = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    severity = Column(String, default="info")
    is_resolved = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    device = relationship("Device", back_populates="alerts")

class FirmwareUpdate(Base):
    __tablename__ = "firmware_updates"
    
    id = Column(Integer, primary_key=True, index=True)
    version = Column(String, nullable=False)
    device_type = Column(String, nullable=False)
    file_url = Column(String, nullable=False)
    changelog = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())