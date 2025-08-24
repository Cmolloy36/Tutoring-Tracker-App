import datetime
from datetime import timezone
import sqlalchemy as sa
from sqlalchemy.orm import Session
from . import models, schemas
from .helper_functions import *
from .helper_classes import *

# Tests

def post_test(session: Session, test: schemas.TestCreate):
    err = validate_is_student(session=session, user_id=test.student_id)
    if err is not None:
        return None, err

    test = models.Test(
        name=test.name,
        date_completed=test.date_completed,
        test_notes=test.test_notes,
        type=test_type,
        student_id=test.student_id,
        english_score=test.english_score,
        math_score=test.math_score
    )

    session.add(test)
    session.commit()
    session.refresh(test)
    return test, None

def get_test(session: Session, test_id: int):
    statement = sa.select(models.Test).where(models.Test.id==test_id)
    return session.scalars(statement).first()

def get_tests(session: Session, test_type: TestType, skip: int = 0, limit: int = 10):
    if test_type is None:
        statement = sa.select(models.Test).offset(skip).limit(limit)
    else:
        statement = sa.select(models.Test).where(models.Test.type==test_type).offset(skip).limit(limit)
    return session.scalars(statement).all()

def get_tests_for_student(session: Session, student_id: int, test_type: TestType, skip: int = 0, limit: int = 10):
    if test_type is None:
        statement = sa.select(models.Test).where(models.Test.student_id==student_id).offset(skip).limit(limit)
    else:
        statement = sa.select(models.Test).where(models.Test.student_id==student_id,models.Test.type==test_type).offset(skip).limit(limit)
    return session.scalars(statement).all()

def update_test(session: Session, test_id: int, test_data: schemas.TestUpdate) -> tuple[models.Test, str]:
    err = validate_is_test(session=session, test_id=test_id)
    if err is not None:
        return None, err
    
    test_to_update = session.query(models.Test).filter_by(id=test_id).first()
    
    if test_data.student_id is not None:
        err = validate_is_student(session=session, user_id=test_data.student_id)
        if err is not None:
            return None, err
    
    update_data = test_data.model_dump(exclude_unset=True)
    update_data["updated_at"] = datetime.datetime.now(tz=timezone.utc)
    # print(update_data)

    for key, val in update_data.items():
        setattr(test_to_update,key,val)

    session.commit()
    updated_test = get_test(session=session,tutor_id=test_id)
    return updated_test, err

def delete_test(session: Session, test_id: int):
    err = validate_is_test(session=session, test_id=test_id)
    if err is not None:
        return None, err

    statement = sa.delete(models.Test).where(models.Test.id==test_id).returning(models.Test.id, models.Test.name, models.Test.fk_students)
    result = session.execute(statement)
    session.commit()
    return result.id, err

# SATs



def get_sat(session: Session, sat_id : int):
    statement = sa.select(models.SAT).where(models.SAT.id==sat_id)
    return session.scalars(statement).first()

def get_sats(session: Session, skip: int = 0, limit: int = 10):
    statement = sa.select(models.SAT).offset(skip).limit(limit)
    return session.scalars(statement).all()

