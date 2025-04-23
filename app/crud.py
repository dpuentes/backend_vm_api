from sqlalchemy.orm import Session
from . import models, schemas
from .auth import get_password_hash

# Funciones CRUD para User
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Funciones CRUD para VirtualMachine
def get_virtual_machine(db: Session, virtual_machine_id: int):
    return db.query(models.VirtualMachine).filter(models.VirtualMachine.id == virtual_machine_id).first()

def get_virtual_machines(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.VirtualMachine).offset(skip).limit(limit).all()

def get_user_virtual_machines(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.VirtualMachine).filter(
        models.VirtualMachine.owner_id == user_id
    ).offset(skip).limit(limit).all()

def create_virtual_machine(db: Session, virtual_machine: schemas.VirtualMachineCreate, user_id: int):
    db_virtual_machine = models.VirtualMachine(**virtual_machine.dict(), owner_id=user_id)
    db.add(db_virtual_machine)
    db.commit()
    db.refresh(db_virtual_machine)
    return db_virtual_machine

def update_virtual_machine(db: Session, virtual_machine_id: int, virtual_machine: schemas.VirtualMachineUpdate):
    db_virtual_machine = get_virtual_machine(db, virtual_machine_id)
    if not db_virtual_machine:
        return None

    update_data = virtual_machine.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_virtual_machine, key, value)

    db.commit()
    db.refresh(db_virtual_machine)
    return db_virtual_machine

def delete_virtual_machine(db: Session, virtual_machine_id: int):
    db_virtual_machine = get_virtual_machine(db, virtual_machine_id)
    if not db_virtual_machine:
        return None
    db.delete(db_virtual_machine)
    db.commit()
    return db_virtual_machine