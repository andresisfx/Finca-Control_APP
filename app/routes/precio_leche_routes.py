from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.precio_leche import PrecioLecheCreate, PrecioLecheUpdate, PrecioLecheOut
from app.services import precio_leche_service

router = APIRouter()

@router.post("/", response_model=PrecioLecheOut, status_code=status.HTTP_201_CREATED)
def create_precio_leche(precio_in: PrecioLecheCreate, db: Session = Depends(get_db)):
    """Establece los precios de compra y venta para una quincena específica."""
    return precio_leche_service.create_precio_leche(db=db, precio_in=precio_in)

@router.get("/quincena/{quincena_id}", response_model=PrecioLecheOut)
def read_precio_por_quincena(quincena_id: int, db: Session = Depends(get_db)):
    """Obtiene los precios de compra y venta establecidos para una quincena."""
    return precio_leche_service.get_precio_por_quincena(db=db, quincena_id=quincena_id)

@router.put("/{precio_id}", response_model=PrecioLecheOut)
def update_precio_leche(precio_id: int, precio_in: PrecioLecheUpdate, db: Session = Depends(get_db)):
    """Actualiza los precios de leche ya definidos."""
    return precio_leche_service.update_precio_leche(db=db, precio_id=precio_id, precio_in=precio_in)

@router.delete("/{precio_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_precio_leche(precio_id: int, db: Session = Depends(get_db)):
    """Elimina la definición de precios de una quincena."""
    precio_leche_service.delete_precio_leche(db=db, precio_id=precio_id)
