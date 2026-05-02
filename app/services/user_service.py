import uuid
from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException, status

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
# TODO: Hashing de passwords posteriormente (por ahora en texto plano para simplificar la prueba inicial)

def get_user(db: Session, user_id: uuid.UUID) -> User:
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return user

def get_user_by_email(db: Session, email: str) -> User | None:
    stmt = select(User).where(User.email == email)
    return db.scalars(stmt).first()

def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
    stmt = select(User).offset(skip).limit(limit)
    return list(db.scalars(stmt).all())

def create_user(db: Session, user_in: UserCreate) -> User:
    # Verificamos que el email no exista
    if get_user_by_email(db, email=user_in.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado."
        )
    
    # Creamos la instancia del modelo (Nota: deberemos encriptar la contraseña más adelante)
    db_user = User(
        email=user_in.email,
        password=user_in.password, 
        nombre=user_in.nombre
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: uuid.UUID, user_in: UserUpdate) -> User:
    db_user = get_user(db, user_id)
    
    update_data = user_in.model_dump(exclude_unset=True)
    
    if "email" in update_data and update_data["email"] != db_user.email:
        if get_user_by_email(db, email=update_data["email"]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El email ya está en uso."
            )
            
    for field, value in update_data.items():
        setattr(db_user, field, value)
        
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: uuid.UUID) -> None:
    db_user = get_user(db, user_id)
    db.delete(db_user)
    db.commit()
