from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.evento import EventoCreate, EventoUpdate, EventoOut
from app.services import evento_service
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=EventoOut, status_code=status.HTTP_201_CREATED)
def create_evento(
    evento_in: EventoCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Registra un nuevo evento para un animal."""
    return evento_service.create_evento(db=db, evento_in=evento_in)

@router.get("/animal/{animal_id}", response_model=list[EventoOut])
def read_eventos_por_animal(
    animal_id: int, 
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obtiene el historial de eventos de un animal."""
    return evento_service.get_eventos_por_animal(db=db, animal_id=animal_id, skip=skip, limit=limit)

@router.get("/{evento_id}", response_model=EventoOut)
def read_evento(
    evento_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obtiene los detalles de un evento específico."""
    return evento_service.get_evento(db=db, evento_id=evento_id)

@router.put("/{evento_id}", response_model=EventoOut)
def update_evento(
    evento_id: int, 
    evento_in: EventoUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Actualiza la información de un evento."""
    return evento_service.update_evento(db=db, evento_id=evento_id, evento_in=evento_in)

@router.delete("/{evento_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_evento(
    evento_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Elimina un evento del historial."""
    evento_service.delete_evento(db=db, evento_id=evento_id)
