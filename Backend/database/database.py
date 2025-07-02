"""
Database Configuration Module
----------------------------
Sets up the SQLAlchemy database engine, session, and base class.

Components:
- engine: SQLAlchemy engine for database connection
- SessionLocal: Factory for database sessions
- Base: Declarative base for ORM models
- get_db: Dependency for providing a session to FastAPI routes

Usage:
Imported by models and API routes to interact with the database.
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
    """
    Dependency function for FastAPI routes to provide a database session.
    
    Purpose:
        - Yields a SQLAlchemy session for use in API endpoints/services.
        - Ensures the session is closed after the request is handled.
    
    Variables:
        db: A new SQLAlchemy session instance from SessionLocal.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()