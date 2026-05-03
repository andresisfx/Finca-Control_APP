from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException, status

from app.models.precio_leche import PrecioLeche
from app.schemas.precio_leche import PrecioLecheCreate, PrecioLecheUpdate
from app.services import quincena_service

def get_precio_leche(db: Session, precio_id: int) -> PrecioLeche:
    precio = db.get(PrecioLeche, precio_id)
    if not precio:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Precio de leche no encontrado")
    return precio

def get_precio_por_quincena(db: Session, quincena_id: int) -> PrecioLeche:
    quincena_service.get_quincena(db, quincena_id)
    stmt = select(PrecioLeche).where(PrecioLeche.quincena_id == quincena_id)
    precio = db.scalars(stmt).first()
    if not precio:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se ha definido precio de leche para esta quincena")
    return precio

def create_precio_leche(db: Session, precio_in: PrecioLecheCreate) -> PrecioLeche:
    quincena_service.get_quincena(db, precio_in.quincena_id)
    
    # Validar que no exista ya un precio para esa quincena
    stmt = select(PrecioLeche).where(PrecioLeche.quincena_id == precio_in.quincena_id)
    if db.scalars(stmt).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un registro de precio para esta quincena. Actualícelo en su lugar."
        )
        
    db_precio = PrecioLeche(**precio_in.model_dump())
    db.add(db_precio)
    db.commit()
    db.refresh(db_precio)
    return db_precio

def update_precio_leche(db: Session, precio_id: int, precio_in: PrecioLecheUpdate) -> PrecioLeche:
    db_precio = get_precio_leche(db, precio_id)
    update_data = precio_in.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_precio, field, value)
        
    db.add(db_precio)
    db.commit()
    db.refresh(db_precio)
    return db_precio

def delete_precio_leche(db: Session, precio_id: int) -> None:
    db_precio = get_precio_leche(db, precio_id)
    db.delete(db_precio)
    db.commit()
