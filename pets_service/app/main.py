from fastapi import FastAPI, HTTPException, status, Depends
from typing import Annotated
from uuid import UUID
from model.pet import Pet
import uvicorn
import os
from database import database as database
from sqlalchemy.orm import Session

app = FastAPI()


database.Base.metadata.create_all(bind=database.engine)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/health", status_code=status.HTTP_200_OK)
async def pet_health():
    return {'message': 'service is active'}


@app.get("/get_pets")
async def get_pets(db: db_dependency):
    result = db.query(database.Pet).offset(0).limit(100).all()
    return result


@app.get("/get_pet_by_id")
async def get_pet_by_id(pet_id: UUID, db: db_dependency):
    result = db.query(database.Pet).filter(database.Pet.id == pet_id).first()
    print(pet_id)
    print(result)
    if not result:
        raise HTTPException(
            status_code=404,
            detail=f'pet with such owner id is not found. pet_id: {pet_id}'
        )
    return result


@app.post('/add_pet')
async def add_doc(pet: Pet, db: db_dependency):
    db_pet = database.Pet(
        id=pet.id,
        name=pet.name,
        age=pet.age,
        favorite_delicacy=pet.favorite_delicacy,
        weight=pet.weight,
        favorite_activity=pet.favorite_activity
    )
    db.add(db_pet)
    db.commit()
    db.refresh(db_pet)
    return "Success"


@app.delete("/delete_pet")
async def delete_doc(pet_id: UUID, db: db_dependency):
    try:
        pet_db = db.query(database.Pet).filter(database.Pet.id == pet_id).first()
        db.delete(pet_db)
        db.commit()
        return "Success"
    except Exception:
        return "cant find pet"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv('PORT', 80)))
