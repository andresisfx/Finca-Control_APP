from pydantic import BaseModel, ConfigDict, Field, UUID4

class VendedorBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=150)
    telefono: str | None = Field(None, min_length=1, max_length=20)

class VendedorCreate(VendedorBase):
    finca_id: UUID4

class VendedorUpdate(BaseModel):
    nombre: str | None = Field(None, min_length=1, max_length=150)
    telefono: str | None = Field(None, min_length=1, max_length=20)

class VendedorOut(VendedorBase):
    id: int
    finca_id: UUID4

    model_config = ConfigDict(from_attributes=True)
