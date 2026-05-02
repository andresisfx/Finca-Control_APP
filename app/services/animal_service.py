import uuid
from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException, status

from app.models.animal import Animal
from app.schemas.animal import AnimalCreate, AnimalUpdate
from app.services import finca_service

def get_animal(db: Session, animal_id: int) -> Animal:
    animal = db.get(Animal, animal_id)
    if not animal:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Animal no encontrado")
    return animal

def get_animales_por_finca(db: Session, finca_id: uuid.UUID, skip: int = 0, limit: int = 100) -> list[Animal]:
    # Validar que la finca exista
    finca_service.get_finca(db, finca_id)
    
    stmt = select(Animal).where(Animal.finca_id == finca_id).offset(skip).limit(limit)
    return list(db.scalars(stmt).all())

def create_animal(db: Session, animal_in: AnimalCreate) -> Animal:
    # Validar que la finca exista
    finca_service.get_finca(db, animal_in.finca_id)
    
    # Validar que el código no exista en esa misma finca
    stmt = select(Animal).where(Animal.finca_id == animal_in.finca_id, Animal.codigo == animal_in.codigo)
    if db.scalars(stmt).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Ya existe un animal con el código {animal_in.codigo} en esta finca"
        )
        
    db_animal = Animal(**animal_in.model_dump())
    
    db.add(db_animal)
    db.commit()
    db.refresh(db_animal)
    return db_animal

def update_animal(db: Session, animal_id: int, animal_in: AnimalUpdate) -> Animal:
    db_animal = get_animal(db, animal_id)
    
    update_data = animal_in.model_dump(exclude_unset=True)
    
    # Si se actualiza el código, verificar que no colisione con otro
    if "codigo" in update_data and update_data["codigo"] != db_animal.codigo:
        stmt = select(Animal).where(Animal.finca_id == db_animal.finca_id, Animal.codigo == update_data["codigo"])
        if db.scalars(stmt).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="El nuevo código ya está en uso en esta finca"
            )
            
    for field, value in update_data.items():
        setattr(db_animal, field, value)
        
    db.add(db_animal)
    db.commit()
    db.refresh(db_animal)
    return db_animal

def delete_animal(db: Session, animal_id: int) -> None:
    db_animal = get_animal(db, animal_id)
    db.delete(db_animal)
    db.commit()
