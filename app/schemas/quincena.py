from pydantic import BaseModel, ConfigDict, UUID4
from datetime import date

class QuincenaBase(BaseModel):
    fecha_inicio: date
    fecha_fin: date

class QuincenaCreate(QuincenaBase):
    finca_id: UUID4

class QuincenaUpdate(BaseModel):
    fecha_inicio: date | None = None
    fecha_fin: date | None = None

class QuincenaOut(QuincenaBase):
    id: int
    finca_id: UUID4

    model_config = ConfigDict(from_attributes=True)
