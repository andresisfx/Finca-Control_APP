import uuid
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

from app.models.finca import Finca
from app.schemas.finca import FincaCreate, FincaUpdate
from app.services import user_service

def get_finca(db: Session, finca_id: uuid.UUID) -> Finca:
    finca = db.get(Finca, finca_id)
    if not finca:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Finca no encontrada")
    return finca

def get_fincas_por_usuario(db: Session, usuario_id: uuid.UUID, skip: int = 0, limit: int = 100) -> list[Finca]:
    # Opcional: validar que el usuario exista
    user_service.get_user(db, usuario_id)
    
    stmt = select(Finca).where(Finca.usuario_id == usuario_id).offset(skip).limit(limit)
    return list(db.scalars(stmt).all())

def create_finca(db: Session, finca_in: FincaCreate) -> Finca:
    # Validar que el usuario exista
    user_service.get_user(db, finca_in.usuario_id)
    
    db_finca = Finca(**finca_in.model_dump())
    
    db.add(db_finca)
    db.commit()
    db.refresh(db_finca)
    return db_finca

def update_finca(db: Session, finca_id: uuid.UUID, finca_in: FincaUpdate) -> Finca:
    db_finca = get_finca(db, finca_id)
    
    update_data = finca_in.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_finca, field, value)
        
    db.add(db_finca)
    db.commit()
    db.refresh(db_finca)
    return db_finca

def delete_finca(db: Session, finca_id: uuid.UUID) -> None:
    try:
        db_finca = db.get(Finca, finca_id)
        if not db_finca:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Finca no encontrada")
        db.delete(db_finca)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al eliminar la finca")
