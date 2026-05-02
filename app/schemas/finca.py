from pydantic import BaseModel, ConfigDict, Field, UUID4

class FincaBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)

class FincaCreate(FincaBase):
    usuario_id: UUID4

class FincaUpdate(BaseModel):
    nombre: str | None = Field(
        default=None,
        min_length=1,
        max_length=100
    )

class FincaOut(FincaBase):
    id: UUID4
    usuario_id: UUID4

    model_config = ConfigDict(from_attributes=True)
