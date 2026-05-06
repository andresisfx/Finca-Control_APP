from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.precio_leche import PrecioLecheCreate, PrecioLecheUpdate, PrecioLecheOut
from app.services import precio_leche_service
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=PrecioLecheOut, status_code=status.HTTP_201_CREATED)
def create_precio(
    precio_in: PrecioLecheCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Asigna un precio de leche a una quincena."""
    return precio_leche_service.create_precio(db=db, precio_in=precio_in)

@router.get("/quincena/{quincena_id}", response_model=list[PrecioLecheOut])
def read_precios_por_quincena(
    quincena_id: int, 
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obtiene los precios definidos para una quincena."""
    return precio_leche_service.get_precios_por_quincena(db=db, quincena_id=quincena_id, skip=skip, limit=limit)

@router.get("/{precio_id}", response_model=PrecioLecheOut)
def read_precio(
    precio_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obtiene el detalle de un registro de precio."""
    return precio_leche_service.get_precio(db=db, precio_id=precio_id)

@router.put("/{precio_id}", response_model=PrecioLecheOut)
def update_precio(
    precio_id: int, 
    precio_in: PrecioLecheUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Actualiza el valor de un precio registrado."""
    return precio_leche_service.update_precio(db=db, precio_id=precio_id, precio_in=precio_in)

@router.delete("/{precio_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_precio(
    precio_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Elimina un registro de precio."""
    precio_leche_service.delete_precio(db=db, precio_id=precio_id)
