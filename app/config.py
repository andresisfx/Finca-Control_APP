"""
Configuración global de la aplicación cargada desde variables de entorno.
"""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Configuración de la app, cargada desde .env"""

    DATABASE_URL: str
    APP_NAME: str = "FincaControl API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    SECRET_KEY: str = "change-this-in-production"

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }


@lru_cache
def get_settings() -> Settings:
    """Retorna instancia cacheada de Settings (singleton)."""
    return Settings()
