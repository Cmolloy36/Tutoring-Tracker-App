import datetime
from datetime import timezone
import sqlalchemy as sa
from sqlalchemy.orm import Session
from . import models, schemas
from .helper_functions import *

# Tests

def get_test(session: Session, test_id: int):
    statement = sa.select(models.Test).where(models.Test.id==test_id)
    return session.scalars(statement).first()

def get_tests(session: Session, skip: int = 0, limit: int = 10):
    statement = sa.select(models.Test).offset(skip).limit(limit)
    return session.scalars(statement).all()

def delete_test(session: Session, test_id: int):
    err = validate_is_test(session=session, test_id=test_id)
    if err is not None:
        return None, None, err

    statement = sa.delete(models.Test).where(models.Test.id==test_id).returning(models.Test.id, models.Test.name, models.Test.fk_students)
    result = session.execute(statement)
    session.commit()
    return result.id, result.name, result.fk_students, err

# SATs

def post_sat(session: Session, sat: schemas.SATCreate) -> tuple[models.SAT, str]:
    err = validate_is_student(session=session, user_id=sat.student_id)
    if err is not None:
        return None, err

    sat = models.SAT(
        name=sat.name,
        date_completed=sat.date_completed,
        test_notes=sat.test_notes,
        type=sat_type,
        student_id=sat.student_id,
        english_score=sat.english_score,
        math_score=sat.math_score
    )

    session.add(sat)
    session.commit()
    session.refresh(sat)
    return sat, None

def get_sat(session: Session, sat_id : int):
    statement = sa.select(models.SAT).where(models.SAT.id==sat_id)
    return session.scalars(statement).first()

def get_sats(session: Session, skip: int = 0, limit: int = 10):
    statement = sa.select(models.SAT).offset(skip).limit(limit)
    return session.scalars(statement).all()

def update_sat(session: Session, sat_id : int, sat_data: schemas.SATUpdate) -> tuple[models.SAT, str]:
    sat_to_update = session.query(models.SAT).filter_by(id=sat_id).first()
    
    if sat_data.student_id is not None:
        err = validate_is_student(session=session, user_id=sat_data.student_id)
        if err is not None:
            return None, err
    
    update_data = sat_data.model_dump(exclude_unset=True)
    update_data["updated_at"] = datetime.datetime.now(tz=timezone.utc)
    print(update_data)

    for key, val in update_data.items():
        setattr(sat_to_update,key,val)

    session.commit()
    updated_sat = get_sat(session=session,tutor_id=sat_id)
    return updated_sat, err