from fastapi import APIRouter, Depends, status
from pydantic import UUID4
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.quincena import QuincenaCreate, QuincenaUpdate, QuincenaOut
from app.services import quincena_service
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=QuincenaOut, status_code=status.HTTP_201_CREATED)
def create_quincena(
    quincena_in: QuincenaCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Crea una nueva quincena para una finca."""
    return quincena_service.create_quincena(db=db, quincena_in=quincena_in)

@router.get("/finca/{finca_id}", response_model=list[QuincenaOut])
def read_quincenas_por_finca(
    finca_id: UUID4, 
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lista las quincenas de una finca."""
    return quincena_service.get_quincenas_por_finca(db=db, finca_id=finca_id, skip=skip, limit=limit)

@router.get("/{quincena_id}", response_model=QuincenaOut)
def read_quincena(
    quincena_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obtiene los detalles de una quincena."""
    return quincena_service.get_quincena(db=db, quincena_id=quincena_id)

@router.put("/{quincena_id}", response_model=QuincenaOut)
def update_quincena(
    quincena_id: int, 
    quincena_in: QuincenaUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Actualiza las fechas de una quincena."""
    return quincena_service.update_quincena(db=db, quincena_id=quincena_id, quincena_in=quincena_in)

@router.delete("/{quincena_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_quincena(
    quincena_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Elimina una quincena."""
    quincena_service.delete_quincena(db=db, quincena_id=quincena_id)
