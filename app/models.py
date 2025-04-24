from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base
from .schemas import Role

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    role = Column(Enum(Role), default=Role.CLIENT)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relación con las máquinas virtuales
    virtual_machines = relationship("VirtualMachine", back_populates="owner")

class VirtualMachine(Base):
    __tablename__ = "virtual_machine"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text, nullable=True)
    status = Column(String, default="stopped")  # stopped, running, paused
    ip_address = Column(String, nullable=True)
    memory = Column(Integer)  # en MB
    cpu_cores = Column(Integer)
    disk_size = Column(Integer)  # en GB
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relación con el usuario propietario
    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="virtual_machines")