from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Any
from enum import Enum



class TipoEvento(str, Enum):
    VACUNACION = "vacunacion"
    ENFERMEDAD = "enfermedad"
    PARTO = "parto"
    CELO = "celo"
    MONTA = "monta"
    SERVICIO = "servicio"
    VENDIDO = "vendido"
    MUERTE = "muerte"

class EventoBase(BaseModel):
    tipo: TipoEvento
    fecha: datetime | None = None  # Si viene null, la DB asigna func.now()
    nota: str | None = None
    metadata_extra: dict[str, Any] | None = None


class EventoCreate(EventoBase):
    animal_id: int


class EventoUpdate(BaseModel):
    tipo: TipoEvento | None = None
    fecha: datetime | None = None
    nota: str | None = None
    metadata_extra: dict[str, Any] | None = None


class EventoOut(EventoBase):
    id: int
    animal_id: int
    fecha: datetime  # Siempre viene de la DB

    model_config = ConfigDict(from_attributes=True)