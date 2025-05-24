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
    Function to create a comment and add it to the database.

    task: stores task object based on the task id.
    db_comment: stores all the details of the comment.
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
    # Function to fetch all the comments under a task.
    return db.query(models.Comment).filter(models.Comment.task_id == task_id).all()

@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(comment_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    '''
    Function to delete a comment from the database.

    comment: stores comment object based on the comment's id.    
    check_comment_permission(): checks if the user has the permission to delete the comment.
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
    Function to update a comment.

    comment: stores the comment object based on the comment's id.
    comment.content: stores the new values from updated.content.
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
