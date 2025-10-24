from fastapi import HTTPException
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.crud.devices_crud import get_device_by_id_db
from app.db.models import Battery
from app.schemas.battery_schemas import BatteryUpdate


async def get_batteries_db(session: AsyncSession):
    q = select(Battery).options(
        selectinload(Battery.device)
    )
    result = await session.execute(q)
    return result.scalars().all()

async def get_battery_by_id_db(session: AsyncSession, battery_id: int):
    result = await session.execute(select(Battery).filter(Battery.id == battery_id))
    battery = result.scalars().first()

    if not battery:
        raise HTTPException(status_code=404, detail="Battery not found")

    return battery

async def get_batteries_by_device_db(session: AsyncSession, device_id: int):
    result = await session.execute(
        select(Battery)
        .options(selectinload(Battery.device))
        .filter(Battery.device_id == device_id)
    )
    return result.scalars().all()

async def update_battery_db(session: AsyncSession, battery_id: int, data: BatteryUpdate):
    result = await session.execute(select(Battery).filter(Battery.id == battery_id))
    battery = result.scalars().first()

    if not battery:
        raise HTTPException(status_code=404, detail="Battery not found")

    new_name = data.name
    new_voltage = data.voltage
    new_capacity = data.capacity
    new_lifespan = data.lifespan
    new_device_id = data.device_id


    if new_name:
        battery.name = new_name
    if new_voltage:
        battery.voltage = new_voltage
    if new_capacity:
        battery.capacity = new_capacity
    if new_lifespan:
        battery.lifespan = new_lifespan
    if new_device_id:
        device = await get_device_by_id_db(session, new_device_id)
        if not device:
            raise HTTPException(status_code=404, detail="Device not found")
        battery.device_id = new_device_id

    await session.commit()
    await session.refresh(battery)
    return battery

async def create_battery_db(session: AsyncSession, name: str, voltage: float, capacity: float, lifespan: int):
    battery = Battery(name=name, voltage=voltage, capacity = capacity, lifespan = lifespan)

    session.add(battery)
    await session.commit()
    await session.refresh(battery)
    return battery

async def delete_battery_db(session: AsyncSession, battery_id:int):
    result = await session.execute(select(Battery).filter(Battery.id == battery_id))
    battery = result.scalars().first()

    if not battery:
        raise HTTPException(status_code=404, detail="Battery not found")

    await session.delete(battery)
    await session.commit()
    return