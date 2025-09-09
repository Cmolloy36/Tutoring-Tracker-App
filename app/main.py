import uvicorn

from fastapi import FastAPI, Depends
from fastapi.middleware.wsgi import WSGIMiddleware
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager

from .config import Settings
from .routers import router_users, router_tests, router_tutoringsessions
from .database import *
# from .students_dashboard import app as student_dashboard

# Initialization

#define means to add dummy initial data here
@asynccontextmanager
def lifespan(session: Session = Depends(get_session)):
    pass 

settings = Settings()
app = FastAPI()
# app.mount("/student_dashboard", WSGIMiddleware(student_dashboard.server))
# app = FastAPI(lifespan=lifespan)

app.include_router(router_users.router)
app.include_router(router_tests.router)
app.include_router(router_tutoringsessions.router)

@app.get("/")
async def root():
    return {"message": "Tutoring Tracker is ready to rock 'n roll!"}

# Start the FastAPI server
if __name__ == "__main__":
    uvicorn.run(app, host=f"127.0.0.1:{settings.fastapi_port}")