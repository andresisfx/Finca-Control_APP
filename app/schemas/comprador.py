from pydantic import BaseModel, ConfigDict, Field, UUID4

class CompradorBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    telefono: str | None = Field(None, min_length=1, max_length=20)

class CompradorCreate(CompradorBase):
    finca_id: UUID4

class CompradorUpdate(BaseModel):
    nombre: str | None = Field(None, min_length=1, max_length=100)
    telefono: str | None = Field(None, min_length=1, max_length=20)

class CompradorOut(CompradorBase):
    id: int
    finca_id: UUID4

    model_config = ConfigDict(from_attributes=True)
