"""
Service para la gestion del ciclo de vida de los refresh tokens.
"""

import uuid
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.config import get_settings
from app.core.security import (
    create_refresh_token_value,
    hash_refresh_token,
)
from app.models.refresh_token import RefreshToken

settings = get_settings()


def create_refresh_token(
    db: Session, user_id: uuid.UUID
) -> tuple[str, RefreshToken]:
    token_value = create_refresh_token_value()
    token_hash = hash_refresh_token(token_value)

    expires_at = datetime.now(timezone.utc) + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )

    db_token = RefreshToken(
        token_hash=token_hash,
        user_id=user_id,
        expires_at=expires_at,
        revoked=False,
    )

    db.add(db_token)
    db.commit()
    db.refresh(db_token)

    return token_value, db_token


def get_valid_refresh_token(db: Session, token_value: str) -> RefreshToken:
    token_hash = hash_refresh_token(token_value)
    now = datetime.now(timezone.utc)

    stmt = select(RefreshToken).where(
        RefreshToken.token_hash == token_hash,
        RefreshToken.revoked == False,
        RefreshToken.expires_at > now,
    )
    db_token = db.scalars(stmt).first()

    if not db_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token invalido, expirado o revocado",
        )
    return db_token


def revoke_refresh_token(db: Session, refresh_token: RefreshToken) -> None:
    try:
        refresh_token.revoked = True
        db.add(refresh_token)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al revocar el refresh token",
        )


def revoke_all_user_tokens(db: Session, user_id: uuid.UUID) -> None:
    try:
        stmt = select(RefreshToken).where(
            RefreshToken.user_id == user_id,
            RefreshToken.revoked == False,
        )
        tokens = list(db.scalars(stmt).all())
        for token in tokens:
            token.revoked = True
            db.add(token)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al revocar los tokens del usuario",
        )
