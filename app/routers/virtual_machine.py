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
    # Verificar que el usuario sea administrador
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden crear máquinas virtuales"
        )

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

@router.get("/{vm_id}", response_model=schemas.VirtualMachineInDB)
def read_virtual_machine(
    vm_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    db_vm = crud.get_virtual_machine(db, vm_id=vm_id)
    if db_vm is None:
        raise HTTPException(status_code=404, detail="Máquina virtual no encontrada")

    # Verificar permisos
    if not current_user.is_superuser and db_vm.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos para acceder a esta máquina virtual"
        )

    return db_vm

@router.put("/{vm_id}", response_model=schemas.VirtualMachineInDB)
def update_virtual_machine(
    vm_id: int,
    virtual_machine: schemas.VirtualMachineUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    # Verificar que el usuario sea administrador
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden actualizar máquinas virtuales"
        )

    db_vm = crud.get_virtual_machine(db, vm_id=vm_id)
    if db_vm is None:
        raise HTTPException(status_code=404, detail="Máquina virtual no encontrada")

    return crud.update_virtual_machine(db=db, vm_id=vm_id, vm=virtual_machine)

@router.delete("/{vm_id}", response_model=schemas.VirtualMachineInDB)
def delete_virtual_machine(
    vm_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    # Verificar que el usuario sea administrador
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los administradores pueden eliminar máquinas virtuales"
        )

    db_vm = crud.get_virtual_machine(db, vm_id=vm_id)
    if db_vm is None:
        raise HTTPException(status_code=404, detail="Máquina virtual no encontrada")

    return crud.delete_virtual_machine(db=db, vm_id=vm_id)
