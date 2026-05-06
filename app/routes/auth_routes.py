from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.security import create_access_token
from app.config import get_settings
from app.db.session import get_db
from app.services.user_service import authenticate_user

settings = get_settings()
router = APIRouter()

@router.post("/login/access-token")
def login_access_token(
    db: Session = Depends(get_db),
    # OAuth2PasswordRequestForm es una clase de FastAPI que permite recibir datos de formulario
    # en formato application/x-www-form-urlencoded, que es el estándar para formularios
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    Endpoint para iniciar sesión.
    Recibe username (email) y password en formato form-data (por estándar de OAuth2).
    Devuelve un token JWT.
    """
    user = authenticate_user(db, email=form_data.username, password=form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # El 'sub' del token será el UUID del usuario
    access_token = create_access_token(
        subject=user.id, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
