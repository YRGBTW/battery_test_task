from fastapi import HTTPException
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models import Device, Battery

async def get_devices_db(session: AsyncSession):
    result = await session.execute(
        select(Device).options(selectinload(Device.batteries))
    )
    devices =  result.scalars().all()
    return devices

async def get_device_by_id_db(session: AsyncSession, device_id: int):
    result = await session.execute(
        select(Device)
        .options(selectinload(Device.batteries))
        .filter(Device.id == device_id)
    )
    device = result.scalars().first()

    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    return device

async def create_device_db(session: AsyncSession, name: str, version: str, state: bool):
    result = await session.execute(select(Device).filter(Device.name == name))
    existing_device = result.scalars().first()

    if existing_device:
        raise HTTPException(status_code=400, detail="Device with this name already exists")

    new_device = Device(name=name, version=version, state=state)

    session.add(new_device)
    await session.commit()
    await session.refresh(new_device)

    return new_device

async def update_device_db(session: AsyncSession, device_id: int, name: str = None, version: str = None, state: bool = None):
    result = await session.execute(select(Device).filter(Device.name == name))
    existing_device = result.scalars().first()

    if existing_device:
        raise HTTPException(status_code=400, detail="Device with this name already exists")

    device = await get_device_by_id_db(session, device_id)

    if name:
        device.name = name
    if version:
        device.version = version
    if state is not None:
        device.state = state

    await session.commit()
    await session.refresh(device)

    return device


async def delete_device_db(session: AsyncSession, device_id: int):
    device = await get_device_by_id_db(session, device_id)

    await session.delete(device)
    await session.commit()
    return {"message": f"Device '{device.name}' deleted successfully"}


async def check_device_battery_limit(session: AsyncSession, device_id: int):
    result = await session.execute(
        select(Battery).filter(Battery.device_id == device_id)
    )
    batteries = result.scalars().all()
    if len(batteries) >= 5:
        raise HTTPException(status_code=400, detail="Device cannot have more than 5 batteries")
