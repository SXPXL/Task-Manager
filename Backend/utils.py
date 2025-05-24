from passlib.context import CryptContext
from jose import jwt 
from datetime import datetime, timedelta
from fastapi import HTTPException,status



# Password hashing
password_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

# Setting for token creation
secret_key = "mysecretkey"
algorithm="HS256"

# fucntion to create a hashed password
def hash_password(password):
  return password_context.hash(password)

# function to verify the password
def check_password(password,hash_password):
  return password_context.verify(password,hash_password)

# function to create a token
def create_token(data: dict, minutes: int=30):
  copy_data = data.copy()
  expire = datetime.utcnow()+timedelta(minutes=minutes)
  copy_data.update({"exp":expire})
  token = jwt.encode(copy_data,secret_key,algorithm=algorithm)
  return token


def validate_password(password: str):
    if len(password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters long")
    if not any(char.isdigit() for char in password):
        raise HTTPException(status_code=400, detail="Password must include at least one number")
    if not any(char.isupper() for char in password):
        raise HTTPException(status_code=400, detail="Password must include at least one uppercase letter")
    if not any(char.islower() for char in password):
        raise HTTPException(status_code=400, detail="Password must include at least one lowercase letter")
    if not any(char in "!@#$%^&*()-_=+[]{}|;:',.<>?/`~" for char in password):
        raise HTTPException(status_code=400, detail="Password must include at least one special character")
    

def check_comment_permission(comment, current_user):
    if comment.user_id != current_user.id and current_user.role not in ["admin", "manager"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this comment"
        )