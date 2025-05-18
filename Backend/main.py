from fastapi import FastAPI
from auth import router as auth_router
from tasks import router as project_router
from database import Base, engine
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()

# creating database tables
Base.metadata.create_all(bind=engine)


# Including routes for authentication
app.include_router(auth_router,prefix="/auth")
app.include_router(project_router,prefix="/project")

app.add_middleware(
  CORSMiddleware,allow_origins=["http://localhost:3000"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"]
  )






