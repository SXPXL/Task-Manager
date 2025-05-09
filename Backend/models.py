from sqlalchemy import Column, Integer, String
from database import Base


class User(Base):
  '''
  Table for storing user details in the database

  id: store the id of a user which can be later used for accessing a user.
  username: stores the name of the user.
  email: stores the user's email.
  hashed_password: it stores the password of the user after hashing it.
  role: stores the role assigned to a user.
  '''
  __tablename__ = "users"
  id = Column(Integer, primary_key=True,index=True,autoincrement=True)
  username =  Column(String,nullable=False)
  email  = Column(String,unique=True,nullable=False,index=True,)
  hashed_password = Column(String,nullable=False)
  '''
  role = Column(String,default="user")
  


# Creating table for storing Projects
class Project(Base):
  __tablename__= "projects"

  '''
