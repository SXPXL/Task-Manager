from sqlalchemy import Column,Date, Integer, String,ForeignKey, DateTime, LargeBinary
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime



class User(Base):
  '''
  Table for storing user details in the database

  id: stores the id of a user which can be later used for accessing a user.
  username: stores the name of the user.
  email: stores the user's email.
  hashed_password: it stores the password of the user after hashing it.
  role: stores the role assigned to a user.
  '''
  __tablename__ = "users"
  id = Column(Integer, primary_key=True,index=True,autoincrement=True)
  username =  Column(String,nullable=False)
  email  = Column(String,unique=True,nullable=False,index=True,)
  hashed_password = Column(String,nullable=False)
  role = Column(String,default="member")
  comments = relationship("Comment", back_populates="user", cascade="all,delete")
  



class Project(Base):
  '''
  Table for storing the details of a project.

  id: stores the project id.
  title: stores the title of the project.
  description: stores the description of the project.
  tasks: sets up a relation with the Task model.
  '''
  __tablename__= "projects"
  id = Column(Integer, primary_key=True,index=True,autoincrement=True)
  title = Column(String,index=True)
  description = Column(String,nullable=False)
  tasks = relationship("Task", back_populates="project", cascade="all,delete")


class Task(Base):
  '''
  Table for storing tasks.

  id: stores the task id.
  title: stores the title of the task.
  description: stores the description of the task.
  status: stores the progress of the task.
  start_date: stores the starting date of the task.
  due_date: stores the end date of the task.
  assigned_to: stores the id of the user who has been assigned with a task.
  project_id: stores the id of the project under which the task is created.
  assigned_User: sets up a relation with User model.
  comments: sets up a relation with Comment model.
  '''
  __tablename__= "tasks"
  id = Column(Integer, primary_key=True,index=True,autoincrement=True)
  title = Column(String,nullable=False)
  description = Column(String,nullable=False)
  status = Column(String,default="pending")
  due_date = Column(Date,nullable=False)
  start_date = Column(Date,nullable=False)
  assigned_to = Column(Integer,ForeignKey("users.id"),nullable=False)
  project_id = Column(Integer,ForeignKey("projects.id"))
  project = relationship("Project", back_populates="tasks")
  assigned_user = relationship("User")
  comments = relationship("Comment", back_populates="task", cascade="all,delete")
  attachments = relationship("Attachment", back_populates="task")



class Comment(Base):
  '''
  Table for storing comments.

  id: stores the comment id.
  content: stores the comment.
  created_at: stores the date of creation of the comment.
  user_id: stores the id of the user who added the comment.
  task_id: stores the id of the task under which the comment is added.
  user: sets up a relation with the User model.
  task: sets up a relation with the Task model.
  '''
  __tablename__ = "comments"

  id = Column(Integer, primary_key=True, index=True)
  content = Column(String, nullable=False)
  created_at = Column(DateTime, default=datetime.utcnow)
  user_id = Column(Integer, ForeignKey("users.id"))
  task_id = Column(Integer, ForeignKey("tasks.id"))
  user = relationship("User", back_populates="comments")
  task = relationship("Task", back_populates="comments")
  


class Attachment(Base):
  __tablename__ = "attachments"
  id = Column(Integer, primary_key=True, index=True)
  task_id = Column(Integer, ForeignKey("tasks.id"))
  filename = Column(String)
  file_data = Column(LargeBinary)  
  content_type = Column(String)
  task = relationship("Task", back_populates="attachments")
  created_at = Column(DateTime,default=datetime.utcnow)
  
  