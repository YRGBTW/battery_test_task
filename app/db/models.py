from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Float
from sqlalchemy.orm import relationship

from app.db.database import Base

class Battery(Base):
    __tablename__ = "batteries"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    voltage = Column(Float, nullable=False)
    capacity = Column(Float, nullable=False)
    lifespan = Column(Integer, nullable=False)

    device_id = Column(Integer, ForeignKey("devices.id"))
    device = relationship("Device", back_populates="batteries")

class Device(Base):
    __tablename__ = "devices"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique= True)
    version = Column(String, nullable=False)
    state = Column(Boolean, nullable= False)

    batteries = relationship("Battery", back_populates="device")


