from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException, status

from app.models.produccion_vendedor_diaria import ProduccionVendedorDiaria
from app.schemas.produccion_vendedor_diaria import ProduccionVendedorDiariaCreate, ProduccionVendedorDiariaUpdate
from app.services import vendedor_service

def get_produccion(db: Session, produccion_id: int) -> ProduccionVendedorDiaria:
    produccion = db.get(ProduccionVendedorDiaria, produccion_id)
    if not produccion:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Registro de producción no encontrado")
    return produccion

def get_producciones_por_vendedor(db: Session, vendedor_id: int, skip: int = 0, limit: int = 100) -> list[ProduccionVendedorDiaria]:
    # Validar que el vendedor exista
    vendedor_service.get_vendedor(db, vendedor_id)
    
    # Ordenamos por fecha descendente
    stmt = select(ProduccionVendedorDiaria).where(
        ProduccionVendedorDiaria.vendedor_id == vendedor_id
    ).order_by(ProduccionVendedorDiaria.fecha.desc()).offset(skip).limit(limit)
    
    return list(db.scalars(stmt).all())

def create_produccion(db: Session, produccion_in: ProduccionVendedorDiariaCreate) -> ProduccionVendedorDiaria:
    # Validar que el vendedor exista
    vendedor_service.get_vendedor(db, produccion_in.vendedor_id)
    
    # Validar que no haya ya un registro para ese vendedor en esa misma fecha
    stmt = select(ProduccionVendedorDiaria).where(
        ProduccionVendedorDiaria.vendedor_id == produccion_in.vendedor_id,
        ProduccionVendedorDiaria.fecha == produccion_in.fecha
    )
    if db.scalars(stmt).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El vendedor ya tiene un registro de leche para la fecha {produccion_in.fecha}"
        )
        
    db_produccion = ProduccionVendedorDiaria(**produccion_in.model_dump())
    
    db.add(db_produccion)
    db.commit()
    db.refresh(db_produccion)
    return db_produccion

def update_produccion(db: Session, produccion_id: int, produccion_in: ProduccionVendedorDiariaUpdate) -> ProduccionVendedorDiaria:
    db_produccion = get_produccion(db, produccion_id)
    
    update_data = produccion_in.model_dump(exclude_unset=True)
    
    # Validar colisión de fecha si la fecha se actualiza
    if "fecha" in update_data and update_data["fecha"] != db_produccion.fecha:
        stmt = select(ProduccionVendedorDiaria).where(
            ProduccionVendedorDiaria.vendedor_id == db_produccion.vendedor_id,
            ProduccionVendedorDiaria.fecha == update_data["fecha"]
        )
        if db.scalars(stmt).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El vendedor ya tiene otro registro para esta nueva fecha"
            )
            
    for field, value in update_data.items():
        setattr(db_produccion, field, value)
        
    db.add(db_produccion)
    db.commit()
    db.refresh(db_produccion)
    return db_produccion

def delete_produccion(db: Session, produccion_id: int) -> None:
    db_produccion = get_produccion(db, produccion_id)
    db.delete(db_produccion)
    db.commit()
