"""
Registro central de todos los modelos SQLAlchemy.
Importar este módulo garantiza que Alembic detecte todas las tablas.
"""

from app.models.base import Base
from app.models.user import User
from app.models.refresh_token import RefreshToken
from app.models.finca import Finca
from app.models.animal import Animal
from app.models.evento import Evento
from app.models.vendedor import Vendedor
from app.models.comprador import Comprador
from app.models.quincena import Quincena
from app.models.precio_leche import PrecioLeche
from app.models.produccion_vendedor_diaria import ProduccionVendedorDiaria
from app.models.entrega import Entrega

__all__ = [
    "Base", "User", "RefreshToken", "Finca", "Animal", "Evento",
    "Vendedor", "Comprador", "Quincena", "PrecioLeche",
    "ProduccionVendedorDiaria", "Entrega",
]
