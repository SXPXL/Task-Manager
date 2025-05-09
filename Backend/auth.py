from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import models,schemas,utils


router = APIRouter()

@router.post("/register",response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
  existing_user = db.query(models.User).filter(models.User.email == user.email).first()
  if existing_user:
    raise HTTPException(status_code=400,detail="Email already exists")
  hashed = utils.hash_password(user.password)
  new_user = models.User(username=user.username,email=user.email,hashed_password=hashed)
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  return new_user

@router.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
  db_user = db.query(models.User).filter(models.User.email == user.email).first()
  if not db_user:
    raise HTTPException(status_code=400,detail="Wrong email or Password")
  token = utils.create_token({"user_id":db_user.id})
  return {"access_token":token,"token_type":"bearer"}

  