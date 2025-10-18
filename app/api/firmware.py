from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.device import Device, FirmwareUpdate
from app.schemas.device import FirmwareUpdate as FirmwareUpdateSchema, FirmwareUpdateCreate
from app.services.firmware_service import initiate_firmware_update

router = APIRouter()

@router.post("/", response_model=FirmwareUpdateSchema)
def create_firmware_update(firmware: FirmwareUpdateCreate, db: Session = Depends(get_db)):
    db_firmware = FirmwareUpdate(**firmware.dict())
    db.add(db_firmware)
    db.commit()
    db.refresh(db_firmware)
    return db_firmware

@router.get("/", response_model=List[FirmwareUpdateSchema])
def get_firmware_updates(
    device_type: str = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(FirmwareUpdate)
    
    if device_type:
        query = query.filter(FirmwareUpdate.device_type == device_type)
    
    return query.offset(skip).limit(limit).all()

@router.post("/{firmware_id}/deploy/{device_id}")
def deploy_firmware_update(
    firmware_id: int,
    device_id: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    firmware = db.query(FirmwareUpdate).filter(FirmwareUpdate.id == firmware_id).first()
    if not firmware:
        raise HTTPException(status_code=404, detail="Firmware update not found")
    
    device = db.query(Device).filter(Device.device_id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    if device.device_type != firmware.device_type:
        raise HTTPException(status_code=400, detail="Firmware not compatible with device type")
    
    background_tasks.add_task(initiate_firmware_update, device_id, firmware.version, firmware.file_url)
    
    return {"message": f"Firmware update initiated for device {device_id}"}