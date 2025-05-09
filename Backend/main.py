from fastapi import FastAPI
from auth import router as auth_router
from database import Base, engine

app=FastAPI()

# creating database tables
Base.metadata.create_all(bind=engine)


# Including routes for authentication
app.include_router(auth_router,prefix="/auth")





