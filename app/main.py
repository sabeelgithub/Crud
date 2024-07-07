from fastapi import FastAPI,Depends,HTTPException
from typing import List,Annotated
from sqlalchemy.orm import Session

from app.database import engine,get_db
from .schemas import UserCreate,UserResponse,UserUpdate
from . import models
from .models import User

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

db_dependency = Annotated[Session,Depends(get_db)]

@app.post("/add_users", response_model=UserResponse)
def create_user(user: UserCreate, db:db_dependency):
    db_user = User(**user.dict(exclude_unset=True))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/get_users", response_model=List[UserResponse])
def get_users(db: db_dependency):
    return db.query(User).all()

@app.patch("/update_users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate, db:db_dependency):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in user.model_dump(exclude_unset=True).items():
        setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

@app.delete("/delete_users/{user_id}")
def delete_user(user_id: int, db:db_dependency):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted"}

