from fastapi import Depends, HTTPException, status
from auth import get_current_user
from models import User

def admin_required(current_user: User = Depends(get_current_user)):
  if current_user.role not in["admin"]:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
  return current_user

def manager_required(current_user: User = Depends(get_current_user)):
  if current_user.role not in ["admin","manager"]:
    raise HTTPException(
      status_code=status.HTTP_403_FORBIDDEN,
      detail="You do not have permission to perform this action"
    )
  return current_user

def member_required(current_user: User = Depends(get_current_user)):
  if current_user.role not in ["admin","manager","member"]:
    raise HTTPException(
      status_code=status.HTTP_403_FORBIDDEN,
      detail="You do not have permission to perform this action"
    )
  return current_user

