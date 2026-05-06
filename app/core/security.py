from datetime import datetime, timedelta
from typing import Any, Union
from jose import jwt
from passlib.context import CryptContext
from app.config import get_settings

settings = get_settings()

# Configuración de Passlib para el hashing de contraseñas usando el algoritmo bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# El subject es el identificador único del usuario
# El expires_delta es el tiempo de expiración del token

def create_access_token(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
    """
    Genera un token JWT (JSON Web Token) válido para el usuario.
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        # Si no se especifica, expira según la configuración (ej. 8 días)
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    # Payload que se encriptará dentro del token. 
    # 'sub' es el estándar para 'subject' (identificador del usuario).
    to_encode = {"exp": expire, "sub": str(subject)}
    
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.SECRET_KEY, 
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica si una contraseña en texto plano coincide con su versión encriptada.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Convierte una contraseña en texto plano en un hash irreversible usando bcrypt.
    """
    return pwd_context.hash(password)
