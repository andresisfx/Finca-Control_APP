"""
Schemas de validación para el usuario.
"""
from pydantic import BaseModel, EmailStr, ConfigDict, Field, UUID4

class UserBase(BaseModel):
    email: EmailStr
    nombre: str = Field(..., min_length=5, max_length=150)

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=128)

class UserUpdate(BaseModel):
    email: EmailStr | None = None
    nombre: str | None = Field(None, min_length=5, max_length=150)
    password: str | None = Field(None, min_length=8, max_length=128)

class UserOut(UserBase):
    id: UUID4
    
    # Esto le dice a Pydantic que está leyendo de un modelo ORM y no de un dict
    model_config = ConfigDict(from_attributes=True)
