from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import models,schemas,utils


router = APIRouter()

@router.post("/register",response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
  '''
  Function to register a new user into the database
  
  existing_user: stores a boolean value if a user is present in the database or not.
  hashed: stores the hashed password.
  new_user: stores all the details of the user.
  '''
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
  '''
  Function gives a token to the use after a successful login.

  db_user: stores a boolean value if the user is present in the database or not.
  token: stores the token for using the app.
  '''
  db_user = db.query(models.User).filter(models.User.email == user.email).first()
  if not db_user:
    raise HTTPException(status_code=400,detail="Wrong email or Password")
  token = utils.create_token({"user_id":db_user.id})
  return {"access_token":token,"token_type":"bearer"}

  