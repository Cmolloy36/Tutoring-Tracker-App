from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager

from . import crud, models, schemas
from .database import *

app = FastAPI()

models.Base.metadata.create_all(engine)

# Initialization

@asynccontextmanager
def add_base_data(session: Session = Depends(get_session)):
    pass #define means to add dummy initial data here


# Users

@app.get("/api/users/{user_id}", response_model=schemas.User)
def get_user(user_id: int, session: Session = Depends(get_session)):
    user = crud.get_user(session=session, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail=f"a user with this id does not exist")
    return user

@app.get("/api/users", response_model=list[schemas.User])
def get_users(skip: int = 0, limit: int = 10, session: Session = Depends(get_session)):
    users = crud.get_users(session=session, skip=skip, limit=limit)
    # if users is []:
    #     ...
    return users

@app.delete("/api/users/{user_id}", response_model=str)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    user_name = crud.delete_user(session=session, user_id=user_id)
    if user_name is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user_name

# Students

@app.post("/api/students",response_model=schemas.Student)
def post_student(student: schemas.StudentCreate, session: Session = Depends(get_session)):
    student, err = crud.post_student(session=session, student=student)
    if err is not None:
        raise HTTPException(status_code=404, detail=f"unable to add student: {err}")
    return student

@app.get("/api/students/{student_id}", response_model=schemas.Student)
def get_student(student_id: int, session: Session = Depends(get_session)):
    student = crud.get_student(session=session, student_id=student_id)
    if student is None:
        raise HTTPException(status_code=404, detail=f"a student with this id does not exist")
    return student

@app.get("/api/students", response_model=list[schemas.Student])
def get_students(skip: int = 0, limit: int = 10, session: Session = Depends(get_session)):
    students = crud.get_students(session=session, skip=skip, limit=limit)
    # if students is []:
    #     ...
    return students

@app.put("/api/students/{student_id}", response_model=schemas.Student)
def update_student(student_id: int, student_data: schemas.StudentUpdate, session: Session = Depends(get_session)):
    student, err = crud.update_student(session=session, student_id=student_id, student_data=student_data)
    if student is None:
        raise HTTPException(status_code=404, detail=f"a student with this id does not exist")
    return student

# Consider a delete endpoint at students as well

# Tutors

@app.post("/api/tutors",response_model=schemas.Tutor)
def post_tutor(tutor: schemas.TutorCreate, session: Session = Depends(get_session)):
    tutor, err = crud.post_tutor(session=session, tutor=tutor)
    if err is not None:
        raise HTTPException(status_code=404, detail=f"unable to add tutor: {err}")
    return tutor

@app.get("/api/tutors/{tutor_id}", response_model=schemas.Tutor)
def get_tutor(tutor_id: int, session: Session = Depends(get_session)):
    tutor = crud.get_tutor(session=session, tutor_id=tutor_id)
    if tutor is None:
        raise HTTPException(status_code=404, detail=f"a tutor with this id does not exist")
    return tutor

@app.get("/api/tutors", response_model=list[schemas.Tutor])
def get_tutors(skip: int = 0, limit: int = 10, session: Session = Depends(get_session)):
    tutors = crud.get_tutors(session=session, skip=skip, limit=limit)
    # if tutors is []:
    #     ...
    return tutors

@app.put("/api/tutors/{tutor_id}", response_model=schemas.Tutor)
def update_tutor(tutor_id: int, tutor_data: schemas.TutorUpdate, session: Session = Depends(get_session)):
    tutor, err = crud.update_tutor(session=session, tutor_id=tutor_id, tutor_data=tutor_data)
    if tutor is None:
        raise HTTPException(status_code=404, detail=f"a tutor with this id does not exist")
    return tutor

# Consider a delete endpoint at tutors as well.