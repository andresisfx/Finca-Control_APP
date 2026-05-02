from pydantic import BaseModel, ConfigDict, Field
from decimal import Decimal

class PrecioLecheBase(BaseModel):
    precio_compra: Decimal = Field(..., max_digits=10, decimal_places=2, ge=0)
    precio_venta: Decimal = Field(..., max_digits=10, decimal_places=2, ge=0)

class PrecioLecheCreate(PrecioLecheBase):
    quincena_id: int

class PrecioLecheUpdate(BaseModel):
    precio_compra: Decimal | None = Field(
        default=None, max_digits=10, decimal_places=2, ge=0
    )
    precio_venta: Decimal | None = Field(
        default=None, max_digits=10, decimal_places=2, ge=0
    )

class PrecioLecheOut(PrecioLecheBase):
    id: int
    quincena_id: int

    model_config = ConfigDict(from_attributes=True)
