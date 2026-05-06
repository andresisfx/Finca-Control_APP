from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.entrega import EntregaCreate, EntregaUpdate, EntregaOut
from app.services import entrega_service
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=EntregaOut, status_code=status.HTTP_201_CREATED)
def create_entrega(
    entrega_in: EntregaCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Registra una entrega de leche a un comprador."""
    return entrega_service.create_entrega(db=db, entrega_in=entrega_in)

@router.get("/quincena/{quincena_id}", response_model=list[EntregaOut])
def read_entregas_por_quincena(
    quincena_id: int, 
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obtiene el historial de entregas de una quincena."""
    return entrega_service.get_entregas_por_quincena(db=db, quincena_id=quincena_id, skip=skip, limit=limit)

@router.get("/{entrega_id}", response_model=EntregaOut)
def read_entrega(
    entrega_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obtiene los detalles de una entrega específica."""
    return entrega_service.get_entrega(db=db, entrega_id=entrega_id)

@router.put("/{entrega_id}", response_model=EntregaOut)
def update_entrega(
    entrega_id: int, 
    entrega_in: EntregaUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Actualiza la cantidad de litros de una entrega."""
    return entrega_service.update_entrega(db=db, entrega_id=entrega_id, entrega_in=entrega_in)

@router.delete("/{entrega_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_entrega(
    entrega_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Elimina una entrega registrada."""
    entrega_service.delete_entrega(db=db, entrega_id=entrega_id)
