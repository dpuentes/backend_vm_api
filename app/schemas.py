from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum

class Role(str, Enum):
    ADMIN = "admin"
    CLIENT = "client"

class VMStatus(str, Enum):
    RUNNING = "running"
    STOPPED = "stopped"
    SUSPENDED = "suspended"

# User schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = None

class UserInDB(UserBase):
    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Authentication schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# VM schemas
class VMBase(BaseModel):
    name: str
    cores: int = Field(..., gt=0)
    ram: int = Field(..., gt=0)  # En GB
    disk: int = Field(..., gt=0)  # En GB
    os: str
    status: VMStatus

class VMCreate(VMBase):
    pass

class VMUpdate(BaseModel):
    cores: int = Field(..., gt=0)
    ram: int = Field(..., gt=0)  # En GB
    disk: int = Field(..., gt=0)  # En GB
    os: str
    status: VMStatus

class VM(VMBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    owner_id: int

    class Config:
        orm_mode = True

# Virtual Machine schemas
class VirtualMachineBase(BaseModel):
    name: str
    description: Optional[str] = None
    memory: int
    cpu_cores: int
    disk_size: int

class VirtualMachineCreate(VirtualMachineBase):
    pass

class VirtualMachineUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    ip_address: Optional[str] = None
    memory: Optional[int] = None
    cpu_cores: Optional[int] = None
    disk_size: Optional[int] = None

class VirtualMachineInDB(VirtualMachineBase):
    id: int
    status: str
    ip_address: Optional[str] = None
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True