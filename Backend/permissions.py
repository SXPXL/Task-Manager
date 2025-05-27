from fastapi import Depends, HTTPException, status
from auth import get_current_user
from models import User

def admin_required(current_user: User = Depends(get_current_user)):
  """
  Dependency that ensures the current user has an admin role.

  Args:
      current_user (User): The currently authenticated user obtained via dependency injection.

  Raises:
      HTTPException: If the current user's role is not 'admin', raises a 403 Forbidden error.

  Returns:
      current_user: The current user if they have admin privileges.
  """
  if current_user.role not in["admin"]:
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
  return current_user

def manager_required(current_user: User = Depends(get_current_user)):
  """
  Dependency that ensures the current user has either admin or manager role.

  Args:
      current_user (User): The currently authenticated user obtained via dependency injection.

  Raises:
      HTTPException: If the current user's role is not 'admin' or 'manager', raises a 403 Forbidden error.

  Returns:
      current_user: The current user if they have admin or manager privileges.
  """
  if current_user.role not in ["admin","manager"]:
    raise HTTPException(
      status_code=status.HTTP_403_FORBIDDEN,
      detail="You do not have permission to perform this action"
    )
  return current_user



