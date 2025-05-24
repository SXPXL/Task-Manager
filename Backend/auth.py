from fastapi import APIRouter, Depends, HTTPException,status
import schemas,utils,models
from sqlalchemy.orm import Session
from database import get_db
from jose import JWTError,jwt
from utils import secret_key, algorithm
from fastapi.security import OAuth2PasswordBearer
from models import User
import schemas


router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
  credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)
  try:
    payload = jwt.decode(token,secret_key,algorithms=[algorithm])
    user_id: int = payload.get("user_id")
    if user_id is None:
        raise credentials_exception
  except JWTError:
    raise credentials_exception

  user = db.query(User).filter(User.id == user_id).first()
  if user is None:
      raise credentials_exception
  return user

@router.post("/register",response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
  '''
  Function to register a new user into the database
  
  existing_user: stores user object based on the email.
  hashed: stores the hashed password.
  new_user: stores all the details of the user.
  '''
  utils.validate_password(user.password)
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
  Function gives a token to the user after a successful login.

  db_user: stores user object based on the email.
  token: stores the token for using the app.
  '''
  db_user = db.query(models.User).filter(models.User.email == user.email).first()
  if not db_user:
    raise HTTPException(status_code=400,detail="Wrong email or Password")
  if not utils.check_password(user.password,db_user.hashed_password):
    raise HTTPException(status_code=400,detail="Wrong email or Password")
  token = utils.create_token({"user_id":db_user.id,"username":db_user.username,"email":db_user.email,"role":db_user.role})
  return {"access_token":token,"token_type":"bearer"}

@router.put("/change-role/{user_id}")
def change_role(user_id: int, role: str, db: Session = Depends(get_db)):
    '''
    Function to change the role of a user. 

    current_user: stores user object based on the user id.
    '''
    current_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")
    if role not in ["admin", "manager", "member"]:
        raise HTTPException(status_code=400, detail="Invalid role")
    
    # Change the role
    current_user.role = role
    db.commit()
    db.refresh(current_user)
    
    return current_user


  
@router.get("/get-users",response_model=list[schemas.UserOut])
def get_users(db: Session = Depends(get_db)):
  '''
  Function to get all the users present in the database.

  '''
  users = db.query(models.User).all()
  return users



