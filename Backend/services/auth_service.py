"""
Authentication Service
---------------------
Service layer for user registration, login, and role management.

Functions:
- register_user: Registers a new user
- login_user: Authenticates a user and returns a token
- change_user_role: Changes a user's role
"""

from fastapi import HTTPException, status
import common.utils as utils
from sqlalchemy.orm import Session
from models.user_model import User

def register_user(db: Session, user):
    """
    Registers a new user in the database after validating the password and checking for email uniqueness.
    
    Args:
        db (Session): SQLAlchemy database session for DB operations.
        user: UserCreate schema containing username, email, and password.
    
    Variables:
        existing_user: The user object found by email, if any.
        hashed: The hashed version of the user's password.
        new_user: The new User object to be added.
    Returns:
        The created User object.
    Raises:
        HTTPException: If the email already exists.
    """
    utils.validate_password(user.password)
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    hashed = utils.hash_password(user.password)
    new_user = User(username=user.username, email=user.email, hashed_password=hashed)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def login_user(db: Session, user):
    """
    Authenticates a user and returns a JWT token if credentials are valid.
    
    Args:
        db (Session): SQLAlchemy database session for DB operations.
        user: UserLogin schema containing email and password.
    
    Variables:
        db_user: The user object found by email, if any.
        token: The generated JWT token for the user.
    Returns:
        A dictionary with the access token and token type.
    Raises:
        HTTPException: If credentials are invalid.
    """
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not utils.check_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Wrong email or Password")
    
    token = utils.create_token({
        "user_id": db_user.id,
        "username": db_user.username,
        "email": db_user.email,
        "role": db_user.role
    })
    return {"access_token": token, "token_type": "bearer"}

def change_user_role(db: Session, user_id: int, role: str):
    """
    Changes the role of a user in the database.
    
    Args:
        db (Session): SQLAlchemy database session for DB operations.
        user_id (int): ID of the user to update.
        role (str): New role to assign (admin, manager, member).
    
    Variables:
        user: The user object found by user_id.
    Returns:
        The updated User object.
    Raises:
        HTTPException: If user is not found or role is invalid.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if role not in ["admin", "manager", "member"]:
        raise HTTPException(status_code=400, detail="Invalid role")
    user.role = role
    db.commit()
    db.refresh(user)
    return user

def get_all_users(db: Session):
    """
    Retrieves all users from the database.
    
    Args:
        db (Session): SQLAlchemy database session for DB operations.
    Returns:
        List of User objects.
    """
    return db.query(User).all()

def delete_user(db: Session, user_id: int, current_user: User):
    """
    Deletes a user from the database by user ID.
    
    Args:
        db (Session): SQLAlchemy database session for DB operations.
        user_id (int): ID of the user to delete.
        current_user (User): The user performing the deletion.
    Returns:
        None
    Raises:
        HTTPException: If user is not found or not authorized.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    db.delete(user)
    db.commit()
    return {"message": f"User '{user.username}' deleted successfully"}
