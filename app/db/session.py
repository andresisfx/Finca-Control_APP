"""
Motor de base de datos y manejo de sesiones SQLAlchemy.
"""

from collections.abc import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.config import get_settings

settings = get_settings()

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,      # Verifica conexión antes de usarla
    pool_size=10,             # Conexiones permanentes en el pool
    max_overflow=20,          # Conexiones extras bajo alta demanda
    echo=settings.DEBUG,      # Loguea SQL en modo debug
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


def get_db() -> Generator[Session, None, None]:
    """Dependencia de FastAPI que provee una sesión de DB por request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
