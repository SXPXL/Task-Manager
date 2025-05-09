from passlib.context import CryptContext
from jose import jwt 
from datetime import datetime, timedelta

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
