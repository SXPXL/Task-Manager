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
    return comment_service.create_comment(task_id, comment, db, current_user)


@router.get("/task/{task_id}", response_model=list[CommentOut])
def get_comments(task_id: int, db: Session = Depends(get_db)):
    return comment_service.get_comments_by_task(task_id, db)


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(comment_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    comment_service.delete_comment(comment_id, db, current_user)


@router.put("/comments/{comment_id}", response_model=CommentOut)
def update_comment(comment_id: int, updated: CommentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return comment_service.update_comment(comment_id, updated, db, current_user)
