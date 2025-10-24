from pydantic import BaseModel
from typing import Optional


class BatteryBase(BaseModel):
    name: str
    voltage: float
    capacity: float
    lifespan: int
    device_id: Optional[int] = None


class BatteryCreate(BatteryBase):
    pass

class BatteryUpdate(BaseModel):
    name: Optional[str] = None
    voltage: Optional[float] = None
    capacity: Optional[float] = None
    lifespan: Optional[int] = None
    device_id: Optional[int] = None


class BatteryResponse(BatteryBase):
    id: int

    class Config:
        orm_mode = True
