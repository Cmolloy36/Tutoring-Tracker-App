import datetime
from datetime import timezone
import sqlalchemy as sa
from sqlalchemy.orm import Session
from . import models, schemas
from .helper_functions import *

# Users

def get_user(session: Session, user_id : int):
    statement = sa.select(models.User).where(models.User.id==user_id)
    return session.scalars(statement).first()

def get_users(session: Session, skip: int = 0, limit: int = 10):
    statement = sa.select(models.User).offset(skip).limit(limit)
    return session.scalars(statement).all()

def delete_user(session: Session, user_id : int):
    statement = sa.delete(models.User).where(models.User.id==user_id).returning(models.User.name)
    user_name = session.scalars(statement).first()
    session.commit()
    return user_name

# Students

def post_student(session: Session, student: schemas.StudentCreate) -> tuple[models.Student, str]:
    err = validate_email(session=session, email=student.email)
    if err is not None:
        return None, err

    student = models.Student(
        name=student.name,
        email=student.email,
        type="student",
        password_hash=hash_password(student.password)
    )
    session.add(student)
    session.commit()
    session.refresh(student)
    return student, None

def get_student(session: Session, student_id: int):
    statement = sa.select(models.Student).where(models.Student.id==student_id)
    return session.scalars(statement).first()

def get_students(session: Session, skip: int = 0, limit: int = 10):
    statement = sa.select(models.Student).offset(skip).limit(limit)
    return session.scalars(statement).all()

def update_student(session: Session, student_id: int, student_data: schemas.StudentUpdate) -> tuple[models.Student, str]:
    err = validate_student(session=session, student_id=student_id)
    if err is not None:
        return None, err
    
    # If i can join users and student info, i can put everything in update_data payload.
    if student_data.email is not None:
        err = validate_email(session=session, email=student_data.email)
        if err is not None:
            return None, err
        
    if student_data.tutor_id is not None:
        err = validate_tutor(session=session, tutor_id=student_data.tutor_id)
        if err is not None:
            return None, err
        
    update_data = student_data.model_dump(exclude_unset=True)
    print(update_data)
    # update_data["updated_at"] = datetime.datetime.now(tz=timezone.utc) # TODO: write this s.t. users table is updated
    
    # getting unconsumed data for name and email here for the same reason as updated_at field
    statement = sa.update(models.Student).where(models.Student.id==student_id).values(update_data).returning(models.Student.tutor_id)
    new_tutor_id = session.scalars(statement).first()

    # if type(new_tutor_id) is int: # what is the returning behavior of the update statement?
    session.commit()

    updated_student = get_student(session=session, student_id=student_id)
    
    # print(f"\n\n\n{updated_student}\n\n\n") 
    return updated_student, None

# Tutors

def post_tutor(session: Session, tutor: schemas.TutorCreate) -> tuple[models.Tutor, str]:
    err = validate_email(session=session, email=tutor.email)
    if err is not None:
        return None, err

    tutor = models.Tutor(
        name=tutor.name,
        email=tutor.email,
        type="tutor",
        password_hash=hash_password(tutor.password)
    )
    session.add(tutor)
    session.commit()
    session.refresh(tutor)
    return tutor, None

def get_tutor(session: Session, tutor_id : int):
    statement = sa.select(models.Tutor).where(models.Tutor.id==tutor_id)
    return session.scalars(statement).first()

def get_tutors(session: Session, skip: int = 0, limit: int = 10):
    statement = sa.select(models.Tutor).offset(skip).limit(limit)
    return session.scalars(statement).all()

def get_students_of_tutor(session: Session, tutor_id : int):
    statement = sa.select(models.Student).where(models.Student.tutor_id==tutor_id)
    return session.scalars(statement).all() # can i specify a number here instead of all? purpose is to do "showing 10 of 21 results"

def update_tutor(session: Session, tutor_id : int, tutor_data: schemas.TutorUpdate) -> tuple[models.Tutor, str]:
    err = validate_tutor(session=session, tutor_id=tutor_id)
    if err is not None:
        return None, err
    
    # If i can join users and tutor info, i can put everything in update_data payload.
    if tutor_data.email is not None:
        err = validate_email(session=session, email=tutor_data.email)
        if err is not None:
            return None, err
    
    update_data = tutor_data.model_dump(exclude_unset=True)
    # update_data["updated_at"] = datetime.datetime.now(tz=timezone.utc) # see update_student above
    
    statement = sa.update(models.Tutor).where(models.Tutor.id==tutor_id).values(update_data).returning(models.Tutor.id)
    tutor_id = session.scalars(statement).first()
    session.commit()
    updated_tutor = get_tutor(session=session,tutor_id=tutor_id)
    return updated_tutor, err

