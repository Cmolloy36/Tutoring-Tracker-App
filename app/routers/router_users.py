from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from .. import crud_users, schemas
from ..database import *

# User-related endpoints
router = APIRouter()

@router.get("/users/{user_id}", response_model=schemas.User)
def get_user(user_id: int, session: Session = Depends(get_session)):
    user = crud_users.get_user(session=session, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail=f"a user with this id does not exist")
    return user

@router.get("/users", response_model=list[schemas.User])
def get_users(skip: int = 0, limit: int = 10, session: Session = Depends(get_session)):
    users = crud_users.get_users(session=session, skip=skip, limit=limit)
    # if users is []:
    #     ...
    return users

@router.delete("/users/{user_id}", response_model=str)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    user_name, user_id, err = crud_users.delete_user(session=session, user_id=user_id)
    if err is not None:
        raise HTTPException(status_code=404, detail=f"error: {err}")
    return f"{user_name} (user_id: {user_id}) has been deleted"

# Students

@router.post("/students",response_model=schemas.Student)
def post_student(student: schemas.StudentCreate, session: Session = Depends(get_session)):
    student, err = crud_users.post_student(session=session, student=student)
    if err is not None:
        raise HTTPException(status_code=404, detail=f"unable to add student: {err}")
    return student

@router.get("/students/{student_id}", response_model=schemas.Student)
def get_student(student_id: int, session: Session = Depends(get_session)):
    student = crud_users.get_student(session=session, student_id=student_id)
    if student is None:
        raise HTTPException(status_code=404, detail=f"a student with this id does not exist")
    return student

@router.get("/students", response_model=list[schemas.Student])
def get_students(skip: int = 0, limit: int = 10, session: Session = Depends(get_session)):
    students = crud_users.get_students(session=session, skip=skip, limit=limit)
    # if students is []:
    #     ...
    return students

@router.put("/students/{student_id}", response_model=schemas.Student)
def update_student(student_id: int, student_data: schemas.StudentUpdate, session: Session = Depends(get_session)):
    student, err = crud_users.update_student(session=session, student_id=student_id, student_data=student_data)
    if err is not None:
        raise HTTPException(status_code=404, detail=f"error: {err}")
    return student

# Consider a delete endpoint at students as well

# Tutors

@router.post("/tutors",response_model=schemas.Tutor)
def post_tutor(tutor: schemas.TutorCreate, session: Session = Depends(get_session)):
    tutor, err = crud_users.post_tutor(session=session, tutor=tutor)
    if err is not None: 
        raise HTTPException(status_code=404, detail=f"unable to add tutor: {err}")
    return tutor

@router.get("/tutors/{tutor_id}", response_model=schemas.Tutor)
def get_tutor(tutor_id: int, session: Session = Depends(get_session)):
    tutor = crud_users.get_tutor(session=session, tutor_id=tutor_id)
    if tutor is None:
        raise HTTPException(status_code=404, detail=f"a tutor with this id does not exist")
    return tutor

@router.get("/tutors", response_model=list[schemas.Tutor])
def get_tutors(skip: int = 0, limit: int = 10, session: Session = Depends(get_session)):
    tutors = crud_users.get_tutors(session=session, skip=skip, limit=limit)
    # if tutors is []:
    #     ...
    return tutors

@router.get("/tutors/{tutor_id}/students", response_model=list[schemas.Student])
def get_students_of_tutor(tutor_id: int, session: Session = Depends(get_session)):
    students = crud_users.get_students_of_tutor(session=session, tutor_id=tutor_id)
    # if students is None:
    #     raise HTTPException(status_code=404, detail=f"a tutor with this id does not exist")
    return students

@router.put("/tutors/{tutor_id}", response_model=schemas.Tutor)
def update_tutor(tutor_id: int, tutor_data: schemas.TutorUpdate, session: Session = Depends(get_session)):
    tutor, err = crud_users.update_tutor(session=session, tutor_id=tutor_id, tutor_data=tutor_data)
    if err is not None:
        raise HTTPException(status_code=404, detail=f"a tutor with this id does not exist")
    return tutor

# Consider a delete endpoint at tutors as well.