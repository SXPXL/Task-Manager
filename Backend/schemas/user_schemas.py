"""
User Schemas
------------
Defines Pydantic schemas for user creation, login, and output/response.

Classes:
- UserCreate: For user registration
- UserLogin: For user authentication
- UserOut: For sending user details in API responses
"""

from pydantic import BaseModel, EmailStr
from datetime import datetime, date
from typing import Optional




class UserCreate(BaseModel):
  """
    Schema for creating a new user during registration.

    Attributes:
        username (str): The user's chosen username.
        email (EmailStr): The user's email address.
        password (str): The user's password in plain text (will be hashed later).
    """
  username: str
  email: EmailStr
  password: str


class UserLogin(BaseModel):
  """
    Schema for user login credentials.

    Attributes:
        email (EmailStr): The user's email address.
        password (str): The user's password.
    """
  email: EmailStr
  password: str



class UserOut(BaseModel):
  """
    Schema for sending user details in responses.

    Attributes:
        id (int): The unique identifier for the user.
        username (str): The user's username.
        email (EmailStr): The user's email.
        role (str): The user's role (e.g., admin, member).
    """
  id: int
  username: str
  email: EmailStr
  role: str

  class Config:
    orm_mode = True