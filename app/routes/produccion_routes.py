from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.produccion_vendedor_diaria import ProduccionVendedorDiariaCreate, ProduccionVendedorDiariaUpdate, ProduccionVendedorDiariaOut
from app.services import produccion_service


router = APIRouter()

@router.post("/", response_model=ProduccionVendedorDiariaOut, status_code=status.HTTP_201_CREATED)
def create_produccion(
    produccion_in: ProduccionVendedorDiariaCreate, 
    db: Session = Depends(get_db)
):
    """Registra los litros de leche entregados por un vendedor."""
    return produccion_service.create_produccion(db=db, produccion_in=produccion_in)

@router.get("/vendedor/{vendedor_id}", response_model=list[ProduccionVendedorDiariaOut])
def read_producciones_por_vendedor(
    vendedor_id: int, 
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """Obtiene el historial de producción por un vendedor."""
    return produccion_service.get_producciones_por_vendedor(db=db, vendedor_id=vendedor_id, skip=skip, limit=limit)

@router.get("/{produccion_id}", response_model=ProduccionVendedorDiariaOut)
def read_produccion(
    produccion_id: int, 
    db: Session = Depends(get_db)
):
    """Obtiene los detalles de un registro de producción específico."""
    return produccion_service.get_produccion(db=db, produccion_id=produccion_id)

@router.put("/{produccion_id}", response_model=ProduccionVendedorDiariaOut)
def update_produccion(
    produccion_id: int, 
    produccion_in: ProduccionVendedorDiariaUpdate, 
    db: Session = Depends(get_db)
):
    """Actualiza un registro de producción."""
    return produccion_service.update_produccion(db=db, produccion_id=produccion_id, produccion_in=produccion_in)

@router.delete("/{produccion_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_produccion(
    produccion_id: int, 
    db: Session = Depends(get_db)
):
    """Elimina un registro de producción."""
    produccion_service.delete_produccion(db=db, produccion_id=produccion_id)
