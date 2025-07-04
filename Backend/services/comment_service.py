"""
Comment Service
---------------
Service layer for creating, retrieving, updating, and deleting comments on tasks.

Functions:
- create_comment: Adds a new comment to a task
- get_comments_by_task: Retrieves all comments for a task
- delete_comment: Deletes a comment by its ID
- update_comment: Updates a comment's content
"""

from fastapi import HTTPException
from sqlalchemy.orm import Session
from schemas.comment_schemas import CommentCreate
from models.comment_model import Comment
from models.task_model import Task
from models.user_model import User
from common.utils import check_comment_permission


def create_comment(task_id: int, comment_in: CommentCreate, db: Session, current_user: User) -> Comment:
    """
    Creates a new comment for a specific task.
    
    Args:
        task_id (int): ID of the task to comment on.
        comment_in (CommentCreate): Schema containing the comment content.
        db (Session): SQLAlchemy database session for DB operations.
        current_user (User): The user creating the comment.
    
    Variables:
        task: The Task object found by task_id.
        comment: The new Comment object to be added.
    Returns:
        The created Comment object.
    Raises:
        HTTPException: If the task is not found.
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    comment = Comment(
        content=comment_in.content,
        user_id=current_user.id,
        task_id=task_id
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


def get_comments_by_task(task_id: int, db: Session) -> list[Comment]:
    """
    Retrieves all comments for a specific task.
    
    Args:
        task_id (int): ID of the task.
        db (Session): SQLAlchemy database session for DB operations.
    Returns:
        List of Comment objects for the task.
    """
    return db.query(Comment).filter(Comment.task_id == task_id).all()


def delete_comment(comment_id: int, db: Session, current_user: User) -> None:
    """
    Deletes a comment by its ID after checking permissions.
    
    Args:
        comment_id (int): ID of the comment to delete.
        db (Session): SQLAlchemy database session for DB operations.
        current_user (User): The user performing the deletion.
    
    Variables:
        comment: The Comment object found by comment_id.
    Returns:
        None
    Raises:
        HTTPException: If the comment is not found or permission is denied.
    """
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    check_comment_permission(comment, current_user)
    db.delete(comment)
    db.commit()


def update_comment(comment_id: int, updated: CommentCreate, db: Session, current_user: User) -> Comment:
    """
    Updates the content of an existing comment.
    
    Args:
        comment_id (int): ID of the comment to update.
        updated (CommentCreate): Schema containing the new content.
        db (Session): SQLAlchemy database session for DB operations.
        current_user (User): The user performing the update.
    Returns:
        The updated Comment object.
    Raises:
        HTTPException: If the comment is not found or permission is denied.
    """
    comment = db.query(Comment).filter(Comment.id == comment_id).first()

    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if comment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed to edit this comment")

    comment.content = updated.content
    db.commit()
    db.refresh(comment)
    return comment
