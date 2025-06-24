"""
This module sets up the database configuration and provides a session dependency for FastAPI routes.

Components:
- database_url: Defines the SQLite database location (in this case, 'users.db' in the current directory)
- engine: SQLAlchemy engine created to connect to the database
- SessionLocal: Session factory for creating and managing DB sessions (used as a dependency in FastAPI)
- Base: Declarative base class used to define ORM models (tables)
- get_db(): Dependency function that yields a database session and ensures it's closed after use
"""



from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from configuration.config import DATABASE_URL


engine = create_engine(
  DATABASE_URL,
  pool_size=10,
  max_overflow=5,
  pool_timeout=30,
  pool_recycle=1800
 )

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()

def get_db():
  db=SessionLocal()
  try:
    yield db
  finally:
    db.close()