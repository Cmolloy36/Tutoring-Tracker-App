from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager

from . import models
from .config import Settings
from .routers import router_users, router_tests, router_tutoringsessions
from .database import *

# Initialization

#define means to add dummy initial data here
@asynccontextmanager
def lifespan(session: Session = Depends(get_session)):
    pass 

settings = Settings()
app = FastAPI()
# app = FastAPI(lifespan=lifespan)

app.include_router(router_users.router)
app.include_router(router_tests.router)
app.include_router(router_tutoringsessions.router)

@app.get("/")
async def root():
    return {"message": "Tutoring Tracker is ready to rock 'n roll!"}