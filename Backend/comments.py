from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import models,schemas
from auth import get_current_user
from utils import check_comment_permission

router = APIRouter()

@router.post("/task/{task_id}", response_model=schemas.CommentOut)
def create_comment(task_id: int, comment: schemas.CommentCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    '''
    Create a new comment for a specific task.

    This function checks if the task exists, then creates a comment associated
    with the task and the currently logged-in user.

    Args:
        task_id (int): ID of the task to which the comment is added.
        comment (schemas.CommentCreate): Contains the content of the comment.
        db (Session): SQLAlchemy database session.
        current_user (User): User object extracted from the JWT token.

    Raises:
        HTTPException: 404 if the task does not exist.

    Returns:
        models.Comment: The newly created comment object.
    '''
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db_comment = models.Comment(
        content=comment.content,
        user_id=current_user.id,
        task_id=task_id
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

@router.get("/task/{task_id}", response_model=list[schemas.CommentOut])
def get_comments(task_id: int, db: Session = Depends(get_db)):
    '''
    Retrieve all comments associated with a specific task.

    Args:
        task_id (int): ID of the task whose comments are to be fetched.
        db (Session): SQLAlchemy database session.

    Returns:
        List[models.Comment]: A list of all comments under the given task.
    '''
    return db.query(models.Comment).filter(models.Comment.task_id == task_id).all()

@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(comment_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    '''
    Delete a specific comment if the user has permission.

    This function checks if the comment exists and whether the current user is
    allowed to delete it (usually the author or an admin).

    Args:
        comment_id (int): ID of the comment to delete.
        db (Session): SQLAlchemy database session.
        current_user (User): User object extracted from the JWT token.

    Raises:
        HTTPException: 404 if comment is not found.
        HTTPException: 403 if user lacks permission to delete.

    Returns:
        None
    '''
    comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    check_comment_permission(comment, current_user)

    db.delete(comment)
    db.commit()


@router.put("/comments/{comment_id}", response_model=schemas.CommentOut)
def update_comment(comment_id: int, updated: schemas.CommentCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    '''
    Update the content of an existing comment.

    This function ensures the comment exists and belongs to the current user before
    updating its content.

    Args:
        comment_id (int): ID of the comment to update.
        updated (schemas.CommentCreate): New content for the comment.
        db (Session): SQLAlchemy database session.
        current_user (User): User object extracted from the JWT token.

    Raises:
        HTTPException: 404 if comment is not found.
        HTTPException: 403 if the user is not the owner of the comment.

    Returns:
        models.Comment: The updated comment object.
    '''
    comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()

    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if comment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed to edit this comment")

    comment.content = updated.content
    db.commit()
    db.refresh(comment)
    return comment
