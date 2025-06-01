"""
This is the main entry point of the FastAPI application.

Modules and Configuration:
- Imports route modules: Handles authentication, projects/tasks, comments, and statistics
- Sets up CORS middleware: Allows cross-origin requests from the frontend (e.g., React app at localhost:3000)
- Creates database tables using SQLAlchemy's Base metadata
- Registers routers with specific URL prefixes for modular route organization
"""



from fastapi import FastAPI
from auth import router as auth_router
from tasks import router as project_router
from comments import router as comment_router
from stats import router as summary_router
from tools import router as tool_router
from database import Base, engine
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()

# Integration with the frontend
app.add_middleware(
  CORSMiddleware,allow_origins=["http://localhost:3000"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"]
  )


# creating database tables
Base.metadata.create_all(bind=engine)


# Including routes for authentication
app.include_router(auth_router,prefix="/auth")
app.include_router(project_router,prefix="/project")
app.include_router(comment_router,prefix="/comment")
app.include_router(summary_router,prefix="/summary")
app.include_router(tool_router,prefix="/tool")







