from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas import user_schemas as schemas
from database.database import get_db
from models.user_model import User
from common.utils import get_current_user 
from services import auth_service

router = APIRouter()

@router.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return auth_service.register_user(db, user)

@router.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    return auth_service.login_user(db, user)

@router.put("/change-role/{user_id}")
def change_role(user_id: int, role: str, db: Session = Depends(get_db)):
    return auth_service.change_user_role(db, user_id, role)

@router.get("/get-users", response_model=list[schemas.UserOut])
def get_users(db: Session = Depends(get_db)):
    return auth_service.get_all_users(db)

@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return auth_service.delete_user(db, user_id, current_user)
