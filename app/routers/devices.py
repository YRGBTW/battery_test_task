from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.crud.devices_crud import (
    get_devices_db,
    get_device_by_id_db,
    create_device_db,
    update_device_db,
    delete_device_db,
)
from app.schemas.device_schemas import (
    DeviceCreate,
    DeviceUpdate,
    DeviceResponse,
)
from typing import List

router = APIRouter(prefix="/devices", tags=["devices"])

@router.get("/", response_model=List[DeviceResponse])
async def get_devices(db: AsyncSession = Depends(get_db)):
    devices = await get_devices_db(db)
    return devices

@router.get("/{device_id}", response_model=DeviceResponse)
async def get_device(device_id: int, db: AsyncSession = Depends(get_db)):
    device = await get_device_by_id_db(db, device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device

@router.post("/", response_model=DeviceResponse)
async def create_device(data: DeviceCreate, db: AsyncSession = Depends(get_db)):
    device = await create_device_db(db, data.name, data.version, data.state)
    return device

@router.put("/{device_id}", response_model=DeviceResponse)
async def update_device(device_id: int, data: DeviceUpdate, db: AsyncSession = Depends(get_db)):
    updated_device = await update_device_db(
        db,
        device_id,
        name=data.name,
        version=data.version,
        state=data.state,
    )
    return updated_device

@router.delete("/{device_id}")
async def delete_device(device_id: int, db: AsyncSession = Depends(get_db)):
    await delete_device_db(db, device_id)
    return {"message": f"Device {device_id} deleted successfully"}
