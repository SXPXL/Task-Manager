from sqlalchemy import Column, Integer, String
from database import Base

# Creating the table named 'users'
class User(Base):
  __tablename__ = "users"

  id = Column(Integer, primary_key=True,index=True,autoincrement=True)
  username =  Column(String,nullable=False)
  email  = Column(String,unique=True,nullable=False,index=True,)
  hashed_password = Column(String,nullable=False)