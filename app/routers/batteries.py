from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.crud.devices_crud import get_device_by_id_db, check_device_battery_limit
from app.db.database import get_db
from app.crud.batteries_crud import (
    get_batteries_db,
    get_batteries_by_device_db,
    create_battery_db,
    update_battery_db,
    delete_battery_db, get_battery_by_id_db,
)
from app.schemas.battery_schemas import (
    BatteryCreate,
    BatteryUpdate,
    BatteryResponse,
)

router = APIRouter(prefix="/batteries", tags=["batteries"])


@router.get("/", response_model=List[BatteryResponse])
async def get_all_batteries(db: AsyncSession = Depends(get_db)):
    batteries = await get_batteries_db(db)
    return batteries

@router.get("/device/{device_id}", response_model=List[BatteryResponse])
async def get_batteries_by_device(device_id: int, db: AsyncSession = Depends(get_db)):
    batteries = await get_batteries_by_device_db(db, device_id)
    return batteries

@router.post("/", response_model=BatteryResponse)
async def create_battery(data: BatteryCreate, db: AsyncSession = Depends(get_db)):
    # (опционально) можно вставить проверку лимита на 5 аккумуляторов
    battery = await create_battery_db(
        db,
        name=data.name,
        voltage=data.voltage,
        capacity=data.capacity,
        lifespan=data.lifespan,
    )
    return battery

@router.put("/{battery_id}", response_model=BatteryResponse)
async def update_battery(battery_id: int, data: BatteryUpdate, db: AsyncSession = Depends(get_db)):
    battery = await update_battery_db(db, battery_id, data)
    return battery

@router.delete("/{battery_id}")
async def delete_battery(battery_id: int, db: AsyncSession = Depends(get_db)):
    await delete_battery_db(db, battery_id)
    return {"message": f"Battery with id={battery_id} deleted successfully"}

@router.post("/{battery_id}/assign/{device_id}", response_model=BatteryResponse)
async def assign_battery_to_device(
    battery_id: int,
    device_id: int,
    db: AsyncSession = Depends(get_db)
):

    battery = await get_battery_by_id_db(db, battery_id)

    device = await get_device_by_id_db(db, device_id)

    await check_device_battery_limit(db, device.id)

    battery.device_id = device_id
    await db.commit()
    await db.refresh(battery)

    return battery
