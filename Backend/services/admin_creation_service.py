"""
Admin Creation Service
---------------------
Provides logic to ensure an admin user exists in the database at startup.

Functions:
- create_admin_if_not_exists: Creates or promotes a user to admin if not present
"""

from passlib.context import CryptContext
from sqlalchemy.orm import Session
from models import user_model as models

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_admin_if_not_exists(db: Session, admin_data: dict):
    """
    Ensures that an admin user exists in the database. If a user with the given email exists but is not an admin, promotes them to admin. Otherwise, creates a new admin user.
    
    Args:
        db (Session): SQLAlchemy database session for DB operations.
        admin_data (dict): Dictionary containing 'username', 'email', and 'password' for the admin user.
    
    Variables:
        existing_user: The user object found by email, if any.
        hashed_password: The hashed version of the admin password (if creating new admin).
        admin_user: The new User object to be added if no admin exists.
    """
    existing_user = db.query(models.User).filter(models.User.email == admin_data["email"]).first()

    if existing_user:
        if existing_user.role != "admin":
            existing_user.role = "admin"
            db.commit()
            print("[INFO] Existing user promoted to admin.")
        else:
            print("[INFO] Admin user already exists.")
    else:
        hashed_password = pwd_context.hash(admin_data["password"])
        admin_user = models.User(
            username=admin_data["username"],
            email=admin_data["email"],
            hashed_password=hashed_password,
            role="admin"
        )
        db.add(admin_user)
        db.commit()
        print("[INFO] Admin user created.")
