from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

from app.models.evento import Evento
from app.schemas.evento import EventoCreate, EventoUpdate
from app.services import animal_service

def get_evento(db: Session, evento_id: int) -> Evento:
    evento = db.get(Evento, evento_id)
    if not evento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evento no encontrado")
    return evento

def get_eventos_por_animal(db: Session, animal_id: int, skip: int = 0, limit: int = 100) -> list[Evento]:
    # Validar que el animal exista
    animal_service.get_animal(db, animal_id)
    
    # Ordenar por fecha descendente
    stmt = select(Evento).where(Evento.animal_id == animal_id).order_by(Evento.fecha.desc()).offset(skip).limit(limit)
    return list(db.scalars(stmt).all())

def create_evento(db: Session, evento_in: EventoCreate) -> Evento:
    # Validar que el animal exista
    animal_service.get_animal(db, evento_in.animal_id)
    
    db_evento = Evento(**evento_in.model_dump())
    
    db.add(db_evento)
    db.commit()
    db.refresh(db_evento)
    return db_evento

def update_evento(db: Session, evento_id: int, evento_in: EventoUpdate) -> Evento:
    db_evento = get_evento(db, evento_id)
    
    update_data = evento_in.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_evento, field, value)
        
    db.add(db_evento)
    db.commit()
    db.refresh(db_evento)
    return db_evento

def delete_evento(db: Session, evento_id: int) -> None:
    try:
        db_evento = db.get(Evento, evento_id)
        if not db_evento:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evento no encontrado")
        db.delete(db_evento)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al eliminar el evento")
