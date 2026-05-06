import uuid
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password

def get_user(db: Session, user_id: uuid.UUID) -> User:
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return user

def get_user_by_email(db: Session, email: str) -> User | None: #scalars() → convierte esas filas en valores simples
    stmt = select(User).where(User.email == email)
    return db.scalars(stmt).first()

def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[User]: #limit → tamaño máximo de resultados
    stmt = select(User).offset(skip).limit(limit) 
    #skip → número de filas a saltar
    #offset → saltar filas
    return list(db.scalars(stmt).all()) #all() → todas las filas restantes

def create_user(db: Session, user_in: UserCreate) -> User:
    # Verificamos que el email no exista
    if get_user_by_email(db, email=user_in.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado."
        )
    
    # Creamos la instancia encriptando la contraseña
    db_user = User(
        email=user_in.email,
        password=get_password_hash(user_in.password), 
        nombre=user_in.nombre
    )
    #Agregamos el nuevo usuario a la base de datos
    db.add(db_user)
    # confirmamos la transacción
    db.commit()
    #Actualizamos el objeto con la información más reciente de la base de datos
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: uuid.UUID, user_in: UserUpdate) -> User:
    db_user = get_user(db, user_id)
    #Evita sobrescribir datos existentes si no fueron enviados
    update_data = user_in.model_dump(exclude_unset=True)
    
    #Validamos que el email que se pretende actualizar no se repita con otro usuario existente
    if "email" in update_data and update_data["email"] != db_user.email:
        if get_user_by_email(db, email=update_data["email"]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El email ya está en uso."
            )
    #Recorremos todos los campos que se actualizarán
    for field, value in update_data.items():
        #Si el campo es la contraseña, la encriptamos
        if field == "password":
            setattr(db_user, field, get_password_hash(value))
        #En cualquier otro caso, actualizamos el campo directamente
        else:
            setattr(db_user, field, value)
        
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: uuid.UUID) -> None:
    try:
        db_user = db.get(User, user_id)
        if not db_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
        db.delete(db_user)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al eliminar el usuario")

def authenticate_user(db: Session, email: str, password: str) -> User | None:
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user
