from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.database import Base
from datetime import datetime

class User(Base):
  '''
  Represents a user in the system.

  Attributes:
    id (int): Unique identifier for the user.
    username (str): Name of the user.
    email (str): Email address of the user (unique).
    hashed_password (str): Password stored in a hashed format.
    role (str): Role of the user (e.g., admin, manager, member).
    comments (relationship): List of comments made by the user.
  '''
  __tablename__ = "users"
  id = Column(Integer, primary_key=True,index=True,autoincrement=True)
  username =  Column(String,nullable=False)
  email  = Column(String,unique=True,nullable=False,index=True,)
  hashed_password = Column(String,nullable=False)
  role = Column(String,default="member")
  comments = relationship("Comment", back_populates="user", cascade="all,delete")