from fastapi import APIRouter, Depends, status
from pydantic import UUID4
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.animal import AnimalCreate, AnimalUpdate, AnimalOut
from app.services import animal_service
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=AnimalOut, status_code=status.HTTP_201_CREATED)
def create_animal(
    animal_in: AnimalCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Registra un nuevo animal en una finca."""
    return animal_service.create_animal(db=db, animal_in=animal_in)

@router.get("/finca/{finca_id}", response_model=list[AnimalOut])
def read_animales_por_finca(
    finca_id: UUID4, 
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obtiene el listado de animales pertenecientes a una finca específica."""
    return animal_service.get_animales_por_finca(db=db, finca_id=finca_id, skip=skip, limit=limit)

@router.get("/{animal_id}", response_model=AnimalOut)
def read_animal(
    animal_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obtiene los detalles de un animal específico."""
    return animal_service.get_animal(db=db, animal_id=animal_id)

@router.put("/{animal_id}", response_model=AnimalOut)
def update_animal(
    animal_id: int, 
    animal_in: AnimalUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Actualiza la información de un animal."""
    return animal_service.update_animal(db=db, animal_id=animal_id, animal_in=animal_in)

@router.delete("/{animal_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_animal(
    animal_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Elimina un animal (Cascada eliminará sus eventos)."""
    animal_service.delete_animal(db=db, animal_id=animal_id)
