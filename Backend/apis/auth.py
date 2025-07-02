"""
Authentication API Routes
------------------------
Defines endpoints for user registration, login, role management, user listing, and deletion.

Routes:
- /register: Register a new user
- /login: Authenticate a user and return a token
- /change-role/{user_id}: Change a user's role
- /get-users: List all users
- /users/{user_id}: Delete a user

Each route delegates business logic to the auth_service module.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas import user_schemas as schemas
from database.database import get_db
from models.user_model import User
from common.utils import get_current_user 
from services import auth_service

router = APIRouter()

@router.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Registers a new user.
    
    Args:
        user: UserCreate schema with registration details.
        db: Database session.
    Returns:
        UserOut schema of the created user.
    """
    return auth_service.register_user(db, user)

@router.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    """
    Authenticates a user and returns a token.
    
    Args:
        user: UserLogin schema with login credentials.
        db: Database session.
    Returns:
        Authentication token and user info.
    """
    return auth_service.login_user(db, user)

@router.put("/change-role/{user_id}")
def change_role(user_id: int, role: str, db: Session = Depends(get_db)):
    """
    Changes the role of a user.
    
    Args:
        user_id: ID of the user to update.
        role: New role to assign.
        db: Database session.
    Returns:
        Updated user info.
    """
    return auth_service.change_user_role(db, user_id, role)

@router.get("/get-users", response_model=list[schemas.UserOut])
def get_users(db: Session = Depends(get_db)):
    """
    Retrieves a list of all users.
    
    Args:
        db: Database session.
    Returns:
        List of UserOut schemas.
    """
    return auth_service.get_all_users(db)

@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Deletes a user by ID.
    
    Args:
        user_id: ID of the user to delete.
        db: Database session.
        current_user: User performing the deletion.
    Returns:
        Result of the deletion operation.
    """
    return auth_service.delete_user(db, user_id, current_user)
