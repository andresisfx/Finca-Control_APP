"""
Endpoints de autenticacion: login, refresh y logout.
"""

from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.security import create_access_token
from app.config import get_settings
from app.db.session import get_db
from app.services.user_service import authenticate_user
from app.services import refresh_token_service
from app.schemas.token import TokenResponse, RefreshRequest

settings = get_settings()
router = APIRouter()


@router.post(
    "/login/access-token",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
)
def login_access_token(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = authenticate_user(db, email=form_data.username, password=form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.id, expires_delta=access_token_expires
    )

    refresh_token_value, _ = refresh_token_service.create_refresh_token(
        db=db, user_id=user.id
    )

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token_value,
        token_type="bearer",
    )


@router.post(
    "/refresh",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
)
def refresh_access_token(
    refresh_request: RefreshRequest,
    db: Session = Depends(get_db),
):
    db_refresh_token = refresh_token_service.get_valid_refresh_token(
        db=db, token_value=refresh_request.refresh_token
    )

    user_id = db_refresh_token.user_id

    refresh_token_service.revoke_refresh_token(db=db, refresh_token=db_refresh_token)

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    new_access_token = create_access_token(
        subject=user_id, expires_delta=access_token_expires
    )

    new_refresh_token_value, _ = refresh_token_service.create_refresh_token(
        db=db, user_id=user_id
    )

    return TokenResponse(
        access_token=new_access_token,
        refresh_token=new_refresh_token_value,
        token_type="bearer",
    )


@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
)
def logout(
    refresh_request: RefreshRequest,
    db: Session = Depends(get_db),
):
    db_refresh_token = refresh_token_service.get_valid_refresh_token(
        db=db, token_value=refresh_request.refresh_token
    )
    refresh_token_service.revoke_refresh_token(db=db, refresh_token=db_refresh_token)
