"""
Comment API Routes
------------------
Defines endpoints for creating, retrieving, updating, and deleting comments on tasks.

Routes:
- /task/{task_id} (POST): Create a comment for a task
- /task/{task_id} (GET): Get all comments for a task
- /{comment_id} (DELETE): Delete a comment
- /comments/{comment_id} (PUT): Update a comment

Each route delegates business logic to the comment_service module.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.database import get_db
from common.utils import get_current_user
from schemas.comment_schemas import CommentCreate, CommentOut
from models.user_model import User
from services import comment_service

router = APIRouter()

@router.post("/task/{task_id}", response_model=CommentOut)
def create_comment(task_id: int, comment: CommentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Creates a new comment for a specific task.
    
    Args:
        task_id: ID of the task to comment on.
        comment: CommentCreate schema with comment details.
        db: Database session.
        current_user: User creating the comment.
    Returns:
        The created CommentOut schema.
    """
    return comment_service.create_comment(task_id, comment, db, current_user)


@router.get("/task/{task_id}", response_model=list[CommentOut])
def get_comments(task_id: int, db: Session = Depends(get_db)):
    """
    Retrieves all comments for a specific task.
    
    Args:
        task_id: ID of the task.
        db: Database session.
    Returns:
        List of CommentOut schemas.
    """
    return comment_service.get_comments_by_task(task_id, db)


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(comment_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Deletes a comment by its ID.
    
    Args:
        comment_id: ID of the comment to delete.
        db: Database session.
        current_user: User performing the deletion.
    Returns:
        None (204 No Content)
    """
    comment_service.delete_comment(comment_id, db, current_user)


@router.put("/comments/{comment_id}", response_model=CommentOut)
def update_comment(comment_id: int, updated: CommentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Updates an existing comment.
    
    Args:
        comment_id: ID of the comment to update.
        updated: CommentCreate schema with updated content.
        db: Database session.
        current_user: User performing the update.
    Returns:
        The updated CommentOut schema.
    """
    return comment_service.update_comment(comment_id, updated, db, current_user)
