"""
Configuración global de la aplicación cargada desde variables de entorno.
"""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Configuración de la app, cargada desde .env"""

    DATABASE_URL: str
    APP_NAME: str 
    APP_VERSION: str 
    #pasar DEBUG=True para entorno de desarrollo
    #!pasar DEBUG=False para entorno de producción
    DEBUG: bool 
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }


@lru_cache
def get_settings() -> Settings:
    """Retorna instancia cacheada de Settings (singleton)."""
    return Settings()
