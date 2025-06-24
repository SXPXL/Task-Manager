from sqlalchemy import Column,Integer, String, Date
from sqlalchemy.orm import relationship
from database.database import Base


class Project(Base):
  '''
  Represents a project entity.

  Attributes:
    id (int): Unique identifier for the project.
    title (str): Title of the project.
    description (str): Description of the project.
    tasks (relationship): List of tasks under the project.
    tools (relationship): List of toold under the project.
  '''
  __tablename__= "projects"
  id = Column(Integer, primary_key=True,index=True,autoincrement=True)
  title = Column(String,index=True)
  description = Column(String,nullable=False)
  tasks = relationship("Task", back_populates="project", cascade="all,delete")
  tools = relationship("Tool",back_populates="project", cascade="all,delete")
  start_date = Column(Date, nullable=False)
  due_date = Column(Date, nullable=False)