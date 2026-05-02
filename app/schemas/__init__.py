"""
Exposición de todos los schemas (Pydantic Models).
Facilita las importaciones en otros archivos.
"""

from .user import UserBase, UserCreate, UserUpdate, UserOut
from .finca import FincaBase, FincaCreate, FincaUpdate, FincaOut
from .animal import AnimalBase, AnimalCreate, AnimalUpdate, AnimalOut
from .evento import EventoBase, EventoCreate, EventoUpdate, EventoOut
from .vendedor import VendedorBase, VendedorCreate, VendedorUpdate, VendedorOut
from .comprador import CompradorBase, CompradorCreate, CompradorUpdate, CompradorOut
from .quincena import QuincenaBase, QuincenaCreate, QuincenaUpdate, QuincenaOut
from .precio_leche import PrecioLecheBase, PrecioLecheCreate, PrecioLecheUpdate, PrecioLecheOut
from .produccion_vendedor_diaria import ProduccionVendedorDiariaBase, ProduccionVendedorDiariaCreate, ProduccionVendedorDiariaUpdate, ProduccionVendedorDiariaOut
from .entrega import EntregaBase, EntregaCreate, EntregaUpdate, EntregaOut

__all__ = [
    "UserBase", "UserCreate", "UserUpdate", "UserOut",
    "FincaBase", "FincaCreate", "FincaUpdate", "FincaOut",
    "AnimalBase", "AnimalCreate", "AnimalUpdate", "AnimalOut",
    "EventoBase", "EventoCreate", "EventoUpdate", "EventoOut",
    "VendedorBase", "VendedorCreate", "VendedorUpdate", "VendedorOut",
    "CompradorBase", "CompradorCreate", "CompradorUpdate", "CompradorOut",
    "QuincenaBase", "QuincenaCreate", "QuincenaUpdate", "QuincenaOut",
    "PrecioLecheBase", "PrecioLecheCreate", "PrecioLecheUpdate", "PrecioLecheOut",
    "ProduccionVendedorDiariaBase", "ProduccionVendedorDiariaCreate", "ProduccionVendedorDiariaUpdate", "ProduccionVendedorDiariaOut",
    "EntregaBase", "EntregaCreate", "EntregaUpdate", "EntregaOut",
]
