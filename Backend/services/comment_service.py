from fastapi import HTTPException
from sqlalchemy.orm import Session
from schemas.comment_schemas import CommentCreate
from models.comment_model import Comment
from models.task_model import Task
from models.user_model import User
from common.utils import check_comment_permission


def create_comment(task_id: int, comment_in: CommentCreate, db: Session, current_user: User) -> Comment:
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
    return db.query(Comment).filter(Comment.task_id == task_id).all()


def delete_comment(comment_id: int, db: Session, current_user: User) -> None:
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    check_comment_permission(comment, current_user)
    db.delete(comment)
    db.commit()


def update_comment(comment_id: int, updated: CommentCreate, db: Session, current_user: User) -> Comment:
    comment = db.query(Comment).filter(Comment.id == comment_id).first()

    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if comment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed to edit this comment")

    comment.content = updated.content
    db.commit()
    db.refresh(comment)
    return comment
