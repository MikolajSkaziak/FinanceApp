from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.db import get_db
from backend.crud import user_crud
from pydantic import BaseModel

router = APIRouter()

# Walidacje danych
class UserCreate(BaseModel):
    username: str
    email: str
    password_hash: str

# POST users
@router.post("/", response_model=dict)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = user_crud.create_user(db, **user.dict())
    return {"id": db_user.id, "username": db_user.username, "email": db_user.email}

# GET usets
@router.get("/", response_model=list[dict])
def list_users(db: Session = Depends(get_db)):
    users = user_crud.get_users(db)
    return [{"id": u.id, "username": u.username, "email": u.email} for u in users]

@router.get("/{user_id}", response_model=dict)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = user_crud.get_user_by_id(db, user_id)
    if user:
        return {"id": user.id, "username": user.username, "email": user.email}
    return {}

@router.delete("/{user_id}", response_model=dict)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    success = user_crud.delete_user(db, user_id)
    return {"success": success}