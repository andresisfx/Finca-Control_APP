from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException, status

from app.models.entrega import Entrega
from app.schemas.entrega import EntregaCreate, EntregaUpdate
from app.services import comprador_service, quincena_service

def get_entrega(db: Session, entrega_id: int) -> Entrega:
    entrega = db.get(Entrega, entrega_id)
    if not entrega:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entrega no encontrada")
    return entrega

def get_entregas_por_quincena(db: Session, quincena_id: int, skip: int = 0, limit: int = 100) -> list[Entrega]:
    quincena_service.get_quincena(db, quincena_id)
    stmt = select(Entrega).where(Entrega.quincena_id == quincena_id).order_by(Entrega.fecha.desc()).offset(skip).limit(limit)
    return list(db.scalars(stmt).all())

def create_entrega(db: Session, entrega_in: EntregaCreate) -> Entrega:
    # Validar comprador y quincena
    comprador_service.get_comprador(db, entrega_in.comprador_id)
    quincena_service.get_quincena(db, entrega_in.quincena_id)
    
    db_entrega = Entrega(**entrega_in.model_dump())
    db.add(db_entrega)
    db.commit()
    db.refresh(db_entrega)
    return db_entrega

def update_entrega(db: Session, entrega_id: int, entrega_in: EntregaUpdate) -> Entrega:
    db_entrega = get_entrega(db, entrega_id)
    update_data = entrega_in.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_entrega, field, value)
        
    db.add(db_entrega)
    db.commit()
    db.refresh(db_entrega)
    return db_entrega

def delete_entrega(db: Session, entrega_id: int) -> None:
    db_entrega = get_entrega(db, entrega_id)
    db.delete(db_entrega)
    db.commit()
