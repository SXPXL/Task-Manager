from fastapi import APIRouter, Depends, HTTPException,File, UploadFile
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse
from models import Project, Task, Attachment
from schemas import TaskCreate, TaskUpdate, TaskOut, ProjectCreate, ProjectOut, AttachmentOut
from database import get_db
from typing import List
from permissions import manager_required
from io import BytesIO

router = APIRouter()

@router.post("/create-projects",dependencies=[Depends(manager_required)])
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    new_project = Project(**project.dict())
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project

@router.get("/get-projects", response_model=List[ProjectOut])
def get_projects(db: Session = Depends(get_db)):
    projects = db.query(Project).all()
    return projects

@router.post("/create-tasks", dependencies=[Depends(manager_required)])
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
   project = db.query(Project).filter(Project.id==task.project_id).first()
   if not project:
        raise HTTPException(status_code=404, detail="Project not found")
   if task.due_date < task.start_date:
        raise HTTPException(status_code=400, detail="Due date cannot be before start date")
   new_task = Task(**task.dict())
   db.add(new_task)
   db.commit()
   db.refresh(new_task)
   return new_task

@router.get("/{project_id}/tasks", response_model=List[TaskOut])
def get_tasks(project_id: int,db:Session = Depends(get_db)):
    tasks = db.query(Task).filter(Task.project_id==project_id).all()  
    return tasks

@router.delete("/delete-task/{task_id}",dependencies=[Depends(manager_required)])
def delete_task(task_id:int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully"}


@router.delete("/delete-project/{project_id}",dependencies=[Depends(manager_required)])
def delete_project(project_id:int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id==project_id).first()
    if not project:
        raise HTTPException(status_code=404,detail="Project not found")
    db.delete(project)
    db.commit()
    return {"message":"Project has bee deleted successfully"}
  

@router.put("/update-task/{task_id}", response_model=TaskOut)
def update_task(task_id:int, task: TaskUpdate, db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in task.dict(exclude_unset=True).items():
        setattr(db_task, key, value)
    db.commit()
    db.refresh(db_task)
    return db_task

#22/5/2025
@router.post("/tasks/{task_id}/attachments/")
async def upload_attachment(
    task_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if not file.filename.lower().endswith('.eml'):
        raise HTTPException(status_code=400, detail='Only .eml files are allowed')
       
    content = await file.read()

    attachment = Attachment(
        filename=file.filename,
        content_type=file.content_type,
        file_data=content,
        task_id=task_id
    )
    db.add(attachment)
    db.commit()
    db.refresh(attachment)
    return {"filename": attachment.filename, "id": attachment.id}


@router.get("/tasks/{task_id}/attachments/",response_model=List[AttachmentOut])
def get_attachments(task_id: int, db: Session = Depends(get_db)):
    emails = db.query(Attachment).filter(Attachment.task_id == task_id).order_by(Attachment.created_at.desc()).all()
    return emails
    

@router.get("/attachments/download/{attachment_id}")
def download_attachment(attachment_id: int, db: Session = Depends(get_db)):
    attachment = db.query(Attachment).filter(Attachment.id == attachment_id).first()
    
    if not attachment:
        raise HTTPException(status_code=404, detail="Attachment not found")
    
    return StreamingResponse(
        BytesIO(attachment.file_data),
        media_type="message/rfc822",  # MIME type for .eml
        headers={"Content-Disposition": f"attachment; filename={attachment.filename}"}
    )
