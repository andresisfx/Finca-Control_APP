from fastapi import APIRouter, Depends, status
from pydantic import UUID4
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.user import UserCreate, UserUpdate, UserOut
from app.services import user_service

router = APIRouter()

@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo usuario en el sistema.
    """
    return user_service.create_user(db=db, user_in=user_in)

@router.get("/", response_model=list[UserOut])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Obtiene la lista de todos los usuarios.
    """
    return user_service.get_users(db=db, skip=skip, limit=limit)

@router.get("/{user_id}", response_model=UserOut)
def read_user(user_id: UUID4, db: Session = Depends(get_db)):
    """
    Obtiene un usuario específico por su ID.
    """
    return user_service.get_user(db=db, user_id=user_id)

@router.put("/{user_id}", response_model=UserOut)
def update_user(user_id: UUID4, user_in: UserUpdate, db: Session = Depends(get_db)):
    """
    Actualiza la información de un usuario.
    """
    return user_service.update_user(db=db, user_id=user_id, user_in=user_in)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: UUID4, db: Session = Depends(get_db)):
    """
    Elimina un usuario del sistema (Cascada eliminará sus fincas).
    """
    user_service.delete_user(db=db, user_id=user_id)
