from pydantic import BaseModel, ConfigDict, Field
from datetime import date
from decimal import Decimal

class EntregaBase(BaseModel):
    fecha: date
    litros: Decimal = Field(...,max_digits=10, decimal_places=2, ge=0)

class EntregaCreate(EntregaBase):
    comprador_id: int
    quincena_id: int

class EntregaUpdate(BaseModel):
    fecha: date | None = None
    litros: Decimal | None = Field(None,max_digits=10, decimal_places=2, ge=0)

class EntregaOut(EntregaBase):
    id: int
    comprador_id: int
    quincena_id: int

    model_config = ConfigDict(from_attributes=True)
