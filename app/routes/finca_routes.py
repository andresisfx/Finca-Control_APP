from fastapi import APIRouter, Depends, status
from pydantic import UUID4
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.finca import FincaCreate, FincaUpdate, FincaOut
from app.services import finca_service
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=FincaOut, status_code=status.HTTP_201_CREATED)
def create_finca(
    finca_in: FincaCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Registra una nueva finca asignada a un usuario autenticado.
    """
    # Sobreescribimos el usuario_id con el del usuario autenticado por seguridad
    finca_in.usuario_id = current_user.id
    return finca_service.create_finca(db=db, finca_in=finca_in)

@router.get("/mis-fincas", response_model=list[FincaOut])
def read_mis_fincas(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Obtiene la lista de fincas que le pertenecen al usuario autenticado.
    """
    return finca_service.get_fincas_por_usuario(db=db, usuario_id=current_user.id, skip=skip, limit=limit)

@router.get("/{finca_id}", response_model=FincaOut)
def read_finca(
    finca_id: UUID4, 
    db: Session = Depends(get_db)
):
    """
    Obtiene los detalles de una finca específica.
    """
    return finca_service.get_finca(db=db, finca_id=finca_id)

@router.put("/{finca_id}", response_model=FincaOut)
def update_finca(
    finca_id: UUID4, 
    finca_in: FincaUpdate, 
    db: Session = Depends(get_db)
):
    """
    Actualiza los datos de una finca.
    """
    return finca_service.update_finca(db=db, finca_id=finca_id, finca_in=finca_in)

@router.delete("/{finca_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_finca(
    finca_id: UUID4, 
    db: Session = Depends(get_db)
):
    """
    Elimina una finca (Cascada eliminará animales, vendedores, etc.).
    """
    finca_service.delete_finca(db=db, finca_id=finca_id)
