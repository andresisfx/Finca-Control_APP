from pydantic import Field
from pydantic import BaseModel, ConfigDict
from datetime import date
from decimal import Decimal

class ProduccionVendedorDiariaBase(BaseModel):
    fecha: date 
    litros: Decimal = Field(..., max_digits=10, decimal_places=2, ge=0)

class ProduccionVendedorDiariaCreate(ProduccionVendedorDiariaBase):
    vendedor_id: int

class ProduccionVendedorDiariaUpdate(BaseModel):
    fecha: date | None = None
    litros: Decimal | None = None

class ProduccionVendedorDiariaOut(ProduccionVendedorDiariaBase):
    id: int
    vendedor_id: int

    model_config = ConfigDict(from_attributes=True)
