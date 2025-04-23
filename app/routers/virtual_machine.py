from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import crud, models, schemas
from ..database import get_db
from ..auth import get_current_active_user

router = APIRouter()

@router.post("/", response_model=schemas.VirtualMachineInDB)
def create_virtual_machine(
    virtual_machine: schemas.VirtualMachineCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    return crud.create_virtual_machine(db=db, vm=virtual_machine, user_id=current_user.id)

@router.get("/", response_model=List[schemas.VirtualMachineInDB])
def read_virtual_machines(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    if current_user.is_superuser:
        virtual_machines = crud.get_virtual_machines(db, skip=skip, limit=limit)
    else:
        virtual_machines = crud.get_user_virtual_machines(db, current_user.id, skip=skip, limit=limit)
    return virtual_machines

@router.get("/{virtual_machine_id}", response_model=schemas.VirtualMachineInDB)
def read_virtual_machine(
    virtual_machine_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    db_virtual_machine = crud.get_virtual_machine(db, vm_id=virtual_machine_id)
    if db_virtual_machine is None:
        raise HTTPException(status_code=404, detail="Virtual machine not found")
    if not current_user.is_superuser and db_virtual_machine.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return db_virtual_machine

@router.put("/{virtual_machine_id}", response_model=schemas.VirtualMachineInDB)
def update_virtual_machine(
    virtual_machine_id: int,
    virtual_machine: schemas.VirtualMachineUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    db_virtual_machine = crud.get_virtual_machine(db, vm_id=virtual_machine_id)
    if db_virtual_machine is None:
        raise HTTPException(status_code=404, detail="Virtual machine not found")
    if not current_user.is_superuser and db_virtual_machine.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return crud.update_virtual_machine(db=db, vm_id=virtual_machine_id, vm=virtual_machine)

@router.delete("/{virtual_machine_id}", response_model=schemas.VirtualMachineInDB)
def delete_virtual_machine(
    virtual_machine_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    db_virtual_machine = crud.get_virtual_machine(db, vm_id=virtual_machine_id)
    if db_virtual_machine is None:
        raise HTTPException(status_code=404, detail="Virtual machine not found")
    if not current_user.is_superuser and db_virtual_machine.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return crud.delete_virtual_machine(db=db, vm_id=virtual_machine_id)
