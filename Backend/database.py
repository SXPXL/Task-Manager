from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Path to the database
database_url = "sqlite:///./users.db"

# creating the database engine
engine = create_engine(database_url,connect_args={"check_same_thread":False})

# For communicating with the database
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

# Base class the tables
Base = declarative_base()

# This function opens or close databse connection 
def get_db():
  db=SessionLocal()
  try:
    yield db
  finally:
    db.close()