from passlib.context import CryptContext
from sqlalchemy.orm import Session
from models import user_model as models

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_admin_if_not_exists(db: Session, admin_data: dict):
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
