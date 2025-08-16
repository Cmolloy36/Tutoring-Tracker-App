from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from .. import crud_tests, schemas
from ..database import *


# User-related endpoints
router = APIRouter()


# Tests

@router.get("/tests/{test_id}", response_model=schemas.Test)
def get_test(test_id: int, session: Session = Depends(get_session)):
    test = crud_tests.get_test(session=session, test_id=test_id)
    if test is None:
        raise HTTPException(status_code=404, detail=f"a test with id:{test_id} does not exist")
    return test

@router.get("/tests", response_model=list[schemas.Test])
def get_tests(skip: int = 0, limit: int = 10, session: Session = Depends(get_session)):
    tests = tests.get_tests(session=session, skip=skip, limit=limit)
    # if users is []:
    #     ...
    return tests

@router.delete("/tests/{test_id}", response_model=str)
def delete_test(test_id: int, session: Session = Depends(get_session)):
    test_id, test_name, user_id, err = crud_tests.delete_test(session=session, test_id=test_id)
    if err is not None:
        raise HTTPException(status_code=404, detail=f"error: {err}")
    return f"Test ID: {test_id}, {test_name} for user {user_id} has been deleted"

# SATs

# TODO: identify appropriate convention for posting tests. Should this be done at the students endpoint?
@router.post("/tests/sats",response_model=schemas.SAT)
def post_sat(sat: schemas.SATCreate, session: Session = Depends(get_session)):
    sat, err = crud_tests.post_sat(session=session, sat=sat)
    if err is not None:
        raise HTTPException(status_code=404, detail=f"unable to add sat: {err}")
    return sat

@router.get("/tests/sats/{sat_id}", response_model=schemas.Student)
def get_student(student_id: int, session: Session = Depends(get_session)):
    student = crud_tests.get_student(session=session, student_id=student_id)
    if student is None:
        raise HTTPException(status_code=404, detail=f"a student with this id does not exist")
    return student

@router.get("/students", response_model=list[schemas.Student])
def get_students(skip: int = 0, limit: int = 10, session: Session = Depends(get_session)):
    students = crud_tests.get_students(session=session, skip=skip, limit=limit)
    # if students is []:
    #     ...
    return students

@router.put("/students/{student_id}", response_model=schemas.Student)
def update_student(student_id: int, student_data: schemas.StudentUpdate, session: Session = Depends(get_session)):
    student, err = crud_tests.update_student(session=session, student_id=student_id, student_data=student_data)
    if err is not None:
        raise HTTPException(status_code=404, detail=f"error: {err}")
    return student