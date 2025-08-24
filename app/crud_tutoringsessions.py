import datetime
from datetime import timezone
import sqlalchemy as sa
from sqlalchemy.orm import Session
from . import models, schemas
from .helper_functions import *

# TutoringSessions

def get_tutoring_session(session: Session, tutoring_session_id: int):
    statement = sa.select(models.TutoringSession).where(models.TutoringSession.id==tutoring_session_id)
    return session.scalars(statement).first()

def get_tutoring_sessions(session: Session, skip: int = 0, limit: int = 10):
    statement = sa.select(models.TutoringSession).offset(skip).limit(limit)
    return session.scalars(statement).all()

def get_tutoring_sessions_for_student(session: Session, student_id: int, skip: int = 0, limit: int = 10):
    err = validate_is_student(session=session, user_id=student_id)
    if err is not None:
        return None, err

    statement = sa.select(models.TutoringSession).where(models.TutoringSession.student_id==student_id).offset(skip).limit(limit)
    return session.scalars(statement).all()

def get_tutoring_sessions_for_tutor(session: Session, tutor_id: int, skip: int = 0, limit: int = 10):
    err = validate_is_tutor(session=session, user_id=tutor_id)
    if err is not None:
        return None, err

    statement = sa.select(models.TutoringSession).where(models.TutoringSession.student_id==tutor_id).offset(skip).limit(limit)
    return session.scalars(statement).all()

def delete_tutoring_session(session: Session, tutoring_session_id: int):
    err = validate_is_tutoring_session(session=session, tutoring_session_id=tutoring_session_id)
    if err is not None:
        return None, None, err

    statement = sa.delete(models.TutoringSession).where(models.TutoringSession.id==tutoring_session_id).returning(models.TutoringSession.id, models.TutoringSession.name, models.TutoringSession.fk_students)
    result = session.execute(statement)
    session.commit()
    return result.id, result.name, result.fk_students, err

# TutoringSessions

def post_tutoring_session(session: Session, tutoring_session: schemas.TutoringSessionCreate) -> tuple[models.TutoringSession, str]:
    err = validate_is_student(session=session, user_id=tutoring_session.student_id)
    if err is not None:
        return None, err

    tutoring_session = models.TutoringSession(
        date_completed=tutoring_session.date_completed,
        tutoring_session_notes=tutoring_session.session_notes,
        student_id=tutoring_session.student_id,
        tutor_id=tutoring_session.tutor_id,
        test_id=tutoring_session.test_id,
    )

    session.add(tutoring_session)
    session.commit()
    session.refresh(tutoring_session)
    return tutoring_session, None

def get_tutoring_session(session: Session, tutoring_session_id : int):
    statement = sa.select(models.TutoringSession).where(models.TutoringSession.id==tutoring_session_id)
    return session.scalars(statement).first()

def get_tutoring_sessions(session: Session, skip: int = 0, limit: int = 10):
    statement = sa.select(models.TutoringSession).offset(skip).limit(limit)
    return session.scalars(statement).all()

def update_tutoring_session(session: Session, tutoring_session_id : int, tutoring_session_data: schemas.TutoringSessionUpdate) -> tuple[models.TutoringSession, str]:
    tutoring_session_to_update = session.query(models.TutoringSession).filter_by(id=tutoring_session_id).first()
    
    if tutoring_session_data.student_id is not None:
        err = validate_is_student(session=session, user_id=tutoring_session_data.student_id)
        if err is not None:
            return None, err
    
    update_data = tutoring_session_data.model_dump(exclude_unset=True)
    update_data["updated_at"] = datetime.datetime.now(tz=timezone.utc)
    print(update_data)

    for key, val in update_data.items():
        setattr(tutoring_session_to_update,key,val)

    session.commit()
    updated_tutoring_session = get_tutoring_session(session=session,tutor_id=tutoring_session_id)
    return updated_tutoring_session, err