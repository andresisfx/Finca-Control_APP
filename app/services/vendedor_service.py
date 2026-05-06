import uuid
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

from app.models.vendedor import Vendedor
from app.schemas.vendedor import VendedorCreate, VendedorUpdate
from app.services import finca_service

def get_vendedor(db: Session, vendedor_id: int) -> Vendedor:
    vendedor = db.get(Vendedor, vendedor_id)
    if not vendedor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vendedor no encontrado")
    return vendedor

def get_vendedores_por_finca(db: Session, finca_id: uuid.UUID, skip: int = 0, limit: int = 100) -> list[Vendedor]:
    # Validar que la finca exista
    finca_service.get_finca(db, finca_id)
    
    stmt = select(Vendedor).where(Vendedor.finca_id == finca_id).offset(skip).limit(limit)
    return list(db.scalars(stmt).all())

def create_vendedor(db: Session, vendedor_in: VendedorCreate) -> Vendedor:
    # Validar que la finca exista
    finca_service.get_finca(db, vendedor_in.finca_id)
    
    db_vendedor = Vendedor(**vendedor_in.model_dump())
    
    db.add(db_vendedor)
    db.commit()
    db.refresh(db_vendedor)
    return db_vendedor

def update_vendedor(db: Session, vendedor_id: int, vendedor_in: VendedorUpdate) -> Vendedor:
    db_vendedor = get_vendedor(db, vendedor_id)
    
    update_data = vendedor_in.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_vendedor, field, value)
        
    db.add(db_vendedor)
    db.commit()
    db.refresh(db_vendedor)
    return db_vendedor

def delete_vendedor(db: Session, vendedor_id: int) -> None:
    try:
        db_vendedor = db.get(Vendedor, vendedor_id)
        if not db_vendedor:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vendedor no encontrado")
        db.delete(db_vendedor)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al eliminar el vendedor")
