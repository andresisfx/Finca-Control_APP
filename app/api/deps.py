from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from pydantic import ValidationError
import uuid

from app.db.session import get_db
from app.config import get_settings
from app.models.user import User
from app.services.user_service import get_user

settings = get_settings()

# Define el endpoint donde la gente va a enviar sus credenciales para sacar el token
reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login/access-token"
)

def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> User:
    """
    Dependencia principal. Se encarga de:
    1. Leer el token de la cabecera 'Authorization: Bearer <token>'
    2. Verificar que no haya expirado ni sido alterado
    3. Sacar el UUID del usuario y buscarlo en la DB
    4. Devolver el objeto User
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id_str: str = payload.get("sub")
        if user_id_str is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No se pudo validar las credenciales",
            )
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se pudo validar las credenciales o el token ha expirado",
        )
        
    try:
        user_uuid = uuid.UUID(user_id_str)
    except ValueError:
        raise HTTPException(status_code=401, detail="ID de usuario inválido en token")
        
    user = db.get(User, user_uuid)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
    return user
