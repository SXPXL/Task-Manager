from sqlalchemy import Column, Integer, String,ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base

class Tool(Base):
  """
  Represent all the tools available in a task
  
  Attributes:
  id (int): Unique identifier for the tool.
  name (string): Name of the tool.
  project_id (int): The ID of the project where the tool is added.
  project (relationship): A relation between tool and project.
  tasks (relationship): A relation between tool and tasks.
  """
  __tablename__ = 'tools'
  id = Column(Integer,primary_key=True,index=True)
  name = Column(String,nullable=False)
  project_id = Column(Integer,ForeignKey('projects.id'))
  project = relationship("Project", back_populates="tools")
  tasks = relationship("Task", back_populates="tool",cascade="all,delete")