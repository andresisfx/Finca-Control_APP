from pydantic import BaseModel, ConfigDict, Field, UUID4

class AnimalBase(BaseModel):
    codigo: str = Field(..., min_length=1, max_length=50)
    nombre: str | None = Field(None, min_length=1, max_length=150)
    foto_url: str | None = None

class AnimalCreate(AnimalBase):
    finca_id: UUID4

class AnimalUpdate(BaseModel):
    codigo: str | None = Field(None, min_length=1, max_length=50)
    nombre: str | None = Field(None, min_length=1, max_length=150)
    foto_url: str | None = None

class AnimalOut(AnimalBase):
    id: int
    finca_id: UUID4

    model_config = ConfigDict(from_attributes=True)
