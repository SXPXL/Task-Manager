from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional



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
  role: str

  class Config:
    orm_mode = True

class ProjectCreate(BaseModel):
  title: str
  description: str

class ProjectOut(BaseModel):
  id: int
  title: str
  description: str
  
  

class TaskCreate(BaseModel):
  title: str
  description: str
  due_date: date
  assigned_to: int
  project_id: int
  


class TaskOut(BaseModel):
  id:int
  title:str
  status:str
  due_date:date
  assigned_to:int
  project_id:int
  description:str

  class Config:
    orm_mode = True

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    due_date: Optional[date] = None

  
