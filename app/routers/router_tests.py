from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from .. import crud_tests, schemas
from ..database import *
from ..helper_classes import TestType


# User-related endpoints
router = APIRouter()


# Tests

@router.post("/students/{student_id}/tests")
def post_test(student_id: int, 
              test: schemas.TestCreate, 
              session: Session = Depends(get_session)
              ):
    
    # How does it know if the input data fits the SAT create? If it checks against the format, how would PSAT ever be reached?
    if isinstance(test, schemas.SATCreate):
        test_type = TestType.SAT
    elif isinstance(test, schemas.PSATCreate):
        test_type = TestType.PSAT
    elif isinstance(test, schemas.ACTCreate):
        test_type = TestType.ACT
    else:
        raise HTTPException(status_code=404, detail=f"unable to add test: this test type does not exist")

    test, err = crud_tests.post_test(session=session, student_id=student_id, test_type=test_type, test=test)
    if err is not None:
        raise HTTPException(status_code=404, detail=f"unable to add test: {err}")
    return test

@router.get("/students/{student_id}/tests", response_model=list[schemas.TestResponse])
def get_tests_for_student(student_id: int, 
        test_type: Optional[TestType] = None, 
        session: Session = Depends(get_session)
        ):
    tests = crud_tests.get_tests_for_student(session=session, test_type=test_type, student_id=student_id)
    if tests is None:
        raise HTTPException(status_code=204, detail=f"this student has no tests") # is this the right way to return?
    return tests

@router.get("/tests/{test_id}",response_model=schemas.TestResponse)
def get_test(
        test_id: int, 
        session: Session = Depends(get_session)
        ):
    tests = crud_tests.get_test(session=session, test_id=test_id)
    if tests is None:
        raise HTTPException(status_code=404, detail=f"test {test_id} does not exist") # is this the right way to return?
    return tests

@router.get("/tests", response_model=list[schemas.Test])
def get_tests(
        test_type: Optional[TestType] = None, 
        session: Session = Depends(get_session)
        ):
    tests = crud_tests.get_tests(session=session, test_type=test_type)
    if tests is None:
        raise HTTPException(status_code=404, detail=f"no such tests exist") # is this the right way to return?
    return tests

@router.put("/tests/{test_id}", response_model=schemas.Test)
def update_test(test_id: int, test: schemas.TestUpdate, session: Session = Depends(get_session)):
    student, err = crud_tests.update_test(session=session, test_id=test_id, test=test)
    if err is not None:
        raise HTTPException(status_code=404, detail=f"error: {err}")
    return student

@router.delete("/tests/{test_id}", response_model=str)
def delete_test(test_id: int, session: Session = Depends(get_session)):
    test_id, err = crud_tests.delete_test(session=session, test_id=test_id)
    if err is not None:
        raise HTTPException(status_code=404, detail=f"error: {err}")
    return f"Test ID: {test_id} has been deleted"

# TODO: identify appropriate convention for posting tests. Should this be done at the students endpoint?