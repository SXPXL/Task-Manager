"""
This module provides utility functions for authentication and security.

Includes:
- Password hashing and verification using bcrypt.
- JWT token creation for user authentication.
- Password strength validation.
- Permission checks for user actions.

Dependencies:
- Passlib for secure password hashing.
- JOSE for JWT encoding.
- FastAPI for exception handling.
"""


from passlib.context import CryptContext
from jose import jwt 
from datetime import datetime, timedelta
from fastapi import HTTPException,status

# Password hashing
password_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

# Settings for token creation
secret_key = "mysecretkey"
algorithm="HS256"


def hash_password(password):
  """
    Generate a hashed version of the given password.

    Args:
    password (str): Plain text password.

    Returns:
    str: Hashed password.
  """
  return password_context.hash(password)


def check_password(password,hash_password):
  """
    Verify a plain password against the stored hashed password.

    Args:
        password (str): User input password.
        hash_password (str): Stored hashed password.

    Returns:
        bool: True if match, else False.
  """
  return password_context.verify(password,hash_password)


def create_token(data: dict, minutes: int=30):
  """
    Create a JWT token for user authentication.

    Args:
        data (dict): Payload to encode in the token (e.g., user ID, role).
        minutes (int, optional): Expiry time in minutes. Defaults to 30.

    Returns:
        str: JWT token.
    """
  copy_data = data.copy()
  expire = datetime.utcnow()+timedelta(minutes=minutes)
  copy_data.update({"exp":expire})
  token = jwt.encode(copy_data,secret_key,algorithm=algorithm)
  return token


def validate_password(password: str):
    """
    Validate password strength against defined rules.

    Raises:
        HTTPException: If password doesn't meet the criteria.
    """
    if len(password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters long")
    if not any(char.isdigit() for char in password):
        raise HTTPException(status_code=400, detail="Password must include at least one number")
    if not any(char.isupper() for char in password):
        raise HTTPException(status_code=400, detail="Password must include at least one uppercase letter")
    if not any(char.islower() for char in password):
        raise HTTPException(status_code=400, detail="Password must include at least one lowercase letter")
    if not any(char in "!@#$%^&*()-_=+[]{}|;:',.<>?/`~" for char in password):
        raise HTTPException(status_code=400, detail="Password must include at least one special character")
    

def check_comment_permission(comment, current_user):
    """
    Check if the current user is authorized to delete a comment.

    Args:
        comment: Comment object (must include user_id).
        current_user: Current logged-in user (must include id and role).

    Raises:
        HTTPException: If user is not the comment owner or lacks sufficient role.
    """
    if comment.user_id != current_user.id and current_user.role not in ["admin", "manager"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this comment"
        )