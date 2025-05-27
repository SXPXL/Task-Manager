from fastapi import APIRouter, Depends, HTTPException,status
import schemas,utils,models
from sqlalchemy.orm import Session
from database import get_db
from jose import JWTError,jwt
from utils import secret_key, algorithm
from fastapi.security import OAuth2PasswordBearer
from models import User




router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
  '''
  Extract and return the current authenticated user based on the JWt token.

  Args:
    token (str): JWT access token ectracted via OAuth2PasswordBearer dependency.
    db (Session): SQLAlchemy DB session.

  Raises:
    HTTPException: Raises 401 Unauthorized if the token is invalid or the user in not found.

  Returns:
    User: SQLAlchemy User object corresponding to the token's user_id.
  
  '''
  
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
 Register a new user by creating a user record in the database.

 Validates the password strength, checks for email uniqueness, hashes the password,
 and add the new user to the db.

 Args:
   user (schemas.UserCreate): Incoming user data (username,email,password).
   db (Session): SQLAlchemy DB session.

  Raises:
    HttpException: 400 Bad Request if email already exists.
  
  Returns:
    models.User: Newly created user object.
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
  Authenticate user and return JWT token if credentials are valid.
  
  Checks user email and password, then generates a JWT acces token with user info.

  Args:
    user (schemas.UserLogin): Loginn credentials (email and password).
    db (Session): SQLAlchemy DB session.

  Raises: 
    HTTPException: 400 bad request if email or password is incorrect.

  Returns:
    dict: Contains access_token (JWT) and token_type ("bearer").
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
  Change the role of a user identified by user_id.

  Validates if user exists and if the requested role is valid,
  then updates the user's role.

  Args:
      user_id (int): ID of the user whose role is to be changed.
      role (str): New role to assign ("admin", "manager", or "member").
      db (Session): DB session.

  Raises:
      HTTPException: 404 if user not found.
      HTTPException: 400 if role is invalid.

  Returns:
      models.User: Updated user object with the new role.
  '''
    current_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")
    if role not in ["admin", "manager", "member"]:
        raise HTTPException(status_code=400, detail="Invalid role")
    
    current_user.role = role
    db.commit()
    db.refresh(current_user)
    
    return current_user


  
@router.get("/get-users",response_model=list[schemas.UserOut])
def get_users(db: Session = Depends(get_db)):
  '''
  Retrieve a list of all users stored in the database.

  Args:
      db (Session): DB session.

  Returns:
      List[models.User]: List of all user records.
  '''
  users = db.query(models.User).all()
  return users

@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    '''
    Delete a user by their user_id if the current user has admin privileges.

    Args:
        user_id (int): ID of the user to be deleted.
        db (Session): DB session.
        current_user (User): Currently authenticated user from JWT token.

    Raises:
        HTTPException: 404 if user to delete does not exist.
        HTTPException: 403 if current user is not an admin.

    Returns:
        dict: Confirmation message of successful deletion.
    '''
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    db.delete(user)
    db.commit()
    return {"message": f"User '{user.username}' deleted successfully"}



