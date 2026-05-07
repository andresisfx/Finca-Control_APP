from fastapi import APIRouter, Depends, status
from pydantic import UUID4
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.vendedor import VendedorCreate, VendedorUpdate, VendedorOut
from app.services import vendedor_service


router = APIRouter()

@router.post("/", response_model=VendedorOut, status_code=status.HTTP_201_CREATED)
def create_vendedor(
    vendedor_in: VendedorCreate, 
    db: Session = Depends(get_db)
):
    """Registra un nuevo pequeño productor (vendedor) para una finca."""
    return vendedor_service.create_vendedor(db=db, vendedor_in=vendedor_in)

@router.get("/finca/{finca_id}", response_model=list[VendedorOut])
def read_vendedores_por_finca(
    finca_id: UUID4, 
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """Obtiene todos los vendedores asociados a una finca."""
    return vendedor_service.get_vendedores_por_finca(db=db, finca_id=finca_id, skip=skip, limit=limit)

@router.get("/{vendedor_id}", response_model=VendedorOut)
def read_vendedor(
    vendedor_id: int, 
    db: Session = Depends(get_db)
):
    """Obtiene los detalles de un vendedor específico."""
    return vendedor_service.get_vendedor(db=db, vendedor_id=vendedor_id)

@router.put("/{vendedor_id}", response_model=VendedorOut)
def update_vendedor(
    vendedor_id: int, 
    vendedor_in: VendedorUpdate, 
    db: Session = Depends(get_db)
):
    """Actualiza la información de un vendedor."""
    return vendedor_service.update_vendedor(db=db, vendedor_id=vendedor_id, vendedor_in=vendedor_in)

@router.delete("/{vendedor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vendedor(
    vendedor_id: int, 
    db: Session = Depends(get_db)
):
    """Elimina un vendedor."""
    vendedor_service.delete_vendedor(db=db, vendedor_id=vendedor_id)
