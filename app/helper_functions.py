import re
import sqlalchemy as sa

from . import models



def validate_email(session: sa.orm.Session, email: str):
    err = None
    if not validate_email_regex(email):
        err = "invalid email format"

    if not validate_email_unique(session, email):
        err = "a user with this email already exists"

    return err

def validate_email_regex(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    if re.match(pattern,email):
        return True
    
    return False

def validate_email_unique(session: sa.orm.Session, email: str):
    # This is currently useless. There is an email constraint on the DB so a 
    statement = sa.select(models.User).where(models.User.email==email)
    if session.scalars(statement).first() is None:
        return True
    return False

def hash_password(password: str): # What return type should the hash be? What lib do i use
    # ...
    return password
    
def validate_password(session: sa.orm.Session, password: str):
    # ...
    return True

def validate_student(session: sa.orm.Session, student_id: int):
    err = None
    if not validate_student_exists(session=session, student_id=student_id):
        err = "Student does not exist"

    return err

def validate_student_exists(session: sa.orm.Session, student_id: int):
    statement = sa.select(models.Student).where(models.Student.id==student_id)
    if session.scalars(statement).first() is not None:
        return True
    return False

def validate_tutor(session: sa.orm.Session, tutor_id: int):
    err = None
    if not validate_tutor_exists(session=session, tutor_id=tutor_id):
        err = "Tutor does not exist"

    return err

def validate_tutor_exists(session: sa.orm.Session, tutor_id: int):
    statement = sa.select(models.Tutor).where(models.Tutor.id==tutor_id)
    if session.scalars(statement).first() is not None:
        return True
    return False