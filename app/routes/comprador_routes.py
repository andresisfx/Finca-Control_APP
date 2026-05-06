from fastapi import APIRouter, Depends, status
from pydantic import UUID4
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.comprador import CompradorCreate, CompradorUpdate, CompradorOut
from app.services import comprador_service
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=CompradorOut, status_code=status.HTTP_201_CREATED)
def create_comprador(
    comprador_in: CompradorCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Registra un nuevo comprador para una finca."""
    return comprador_service.create_comprador(db=db, comprador_in=comprador_in)

@router.get("/finca/{finca_id}", response_model=list[CompradorOut])
def read_compradores_por_finca(
    finca_id: UUID4, 
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obtiene todos los compradores asociados a una finca."""
    return comprador_service.get_compradores_por_finca(db=db, finca_id=finca_id, skip=skip, limit=limit)

@router.get("/{comprador_id}", response_model=CompradorOut)
def read_comprador(
    comprador_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obtiene los detalles de un comprador específico."""
    return comprador_service.get_comprador(db=db, comprador_id=comprador_id)

@router.put("/{comprador_id}", response_model=CompradorOut)
def update_comprador(
    comprador_id: int, 
    comprador_in: CompradorUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Actualiza la información de un comprador."""
    return comprador_service.update_comprador(db=db, comprador_id=comprador_id, comprador_in=comprador_in)

@router.delete("/{comprador_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comprador(
    comprador_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Elimina un comprador de la base de datos."""
    comprador_service.delete_comprador(db=db, comprador_id=comprador_id)
