from pydantic import BaseModel
from typing import Optional, List

class BatteryShort(BaseModel):
    id: int
    name: str
    voltage: float
    capacity: float
    lifespan: int

    class Config:
        orm_mode = True


class DeviceBase(BaseModel):
    name: str
    version: str
    state: bool


class DeviceCreate(DeviceBase):
    pass


class DeviceUpdate(BaseModel):
    name: Optional[str] = None
    version: Optional[str] = None
    state: Optional[bool] = None


class DeviceResponse(DeviceBase):
    id: int

    class Config:
        orm_mode = True
