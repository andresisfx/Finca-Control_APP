import uuid
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

from app.models.comprador import Comprador
from app.schemas.comprador import CompradorCreate, CompradorUpdate
from app.services import finca_service

def get_comprador(db: Session, comprador_id: int) -> Comprador:
    comprador = db.get(Comprador, comprador_id)
    if not comprador:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comprador no encontrado")
    return comprador

def get_compradores_por_finca(db: Session, finca_id: uuid.UUID, skip: int = 0, limit: int = 100) -> list[Comprador]:
    finca_service.get_finca(db, finca_id)
    stmt = select(Comprador).where(Comprador.finca_id == finca_id).offset(skip).limit(limit)
    return list(db.scalars(stmt).all())

def create_comprador(db: Session, comprador_in: CompradorCreate) -> Comprador:
    finca_service.get_finca(db, comprador_in.finca_id)
    db_comprador = Comprador(**comprador_in.model_dump())
    db.add(db_comprador)
    db.commit()
    db.refresh(db_comprador)
    return db_comprador

def update_comprador(db: Session, comprador_id: int, comprador_in: CompradorUpdate) -> Comprador:
    db_comprador = get_comprador(db, comprador_id)
    update_data = comprador_in.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_comprador, field, value)
        
    db.add(db_comprador)
    db.commit()
    db.refresh(db_comprador)
    return db_comprador

def delete_comprador(db: Session, comprador_id: int) -> None:
    try:
        db_comprador = db.get(Comprador, comprador_id)
        if not db_comprador:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comprador no encontrado")
        db.delete(db_comprador)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al eliminar el comprador")
