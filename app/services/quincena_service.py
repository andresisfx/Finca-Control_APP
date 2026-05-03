import uuid
from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException, status

from app.models.quincena import Quincena
from app.schemas.quincena import QuincenaCreate, QuincenaUpdate
from app.services import finca_service

def get_quincena(db: Session, quincena_id: int) -> Quincena:
    quincena = db.get(Quincena, quincena_id)
    if not quincena:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quincena no encontrada")
    return quincena

def get_quincenas_por_finca(db: Session, finca_id: uuid.UUID, skip: int = 0, limit: int = 100) -> list[Quincena]:
    finca_service.get_finca(db, finca_id)
    stmt = select(Quincena).where(Quincena.finca_id == finca_id).order_by(Quincena.fecha_inicio.desc()).offset(skip).limit(limit)
    return list(db.scalars(stmt).all())

def create_quincena(db: Session, quincena_in: QuincenaCreate) -> Quincena:
    finca_service.get_finca(db, quincena_in.finca_id)
    
    if quincena_in.fecha_fin < quincena_in.fecha_inicio:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="La fecha de fin no puede ser anterior a la fecha de inicio"
        )
        
    db_quincena = Quincena(**quincena_in.model_dump())
    db.add(db_quincena)
    db.commit()
    db.refresh(db_quincena)
    return db_quincena

def update_quincena(db: Session, quincena_id: int, quincena_in: QuincenaUpdate) -> Quincena:
    db_quincena = get_quincena(db, quincena_id)
    update_data = quincena_in.model_dump(exclude_unset=True)
    
    nueva_inicio = update_data.get("fecha_inicio", db_quincena.fecha_inicio)
    nueva_fin = update_data.get("fecha_fin", db_quincena.fecha_fin)
    
    if nueva_fin < nueva_inicio:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="La fecha de fin no puede ser anterior a la fecha de inicio"
        )
        
    for field, value in update_data.items():
        setattr(db_quincena, field, value)
        
    db.add(db_quincena)
    db.commit()
    db.refresh(db_quincena)
    return db_quincena

def delete_quincena(db: Session, quincena_id: int) -> None:
    db_quincena = get_quincena(db, quincena_id)
    db.delete(db_quincena)
    db.commit()
