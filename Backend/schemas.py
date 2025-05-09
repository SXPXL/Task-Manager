from pydantic import BaseModel, EmailStr


# Used during registration
class UserCreate(BaseModel):
  username: str
  email: EmailStr
  password: str

# Used during login 
class UserLogin(BaseModel):
  email: EmailStr
  password: str

# For sendin as response to the user
class UserOut(BaseModel):
  id: int
  username: str
  email: EmailStr

  class Config:
    orm_mode = True