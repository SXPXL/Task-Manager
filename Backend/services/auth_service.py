from fastapi import HTTPException, status
import common.utils as utils
from sqlalchemy.orm import Session
from models.user_model import User

def register_user(db: Session, user):
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
    return db.query(User).all()

def delete_user(db: Session, user_id: int, current_user: User):
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
