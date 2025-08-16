import re
import sqlalchemy as sa

from . import models

global student_type, tutor_type, sat_type, psat_type, act_type
student_type = "student"
tutor_type = "tutor"
sat_type = "SAT"
psat_type = "PSAT"
act_type = "ACT"

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

# consider making these into one function with passable type input
def validate_is_student(session: sa.orm.Session, user_id: int):
    err = None
    user = session.query(models.User).filter_by(id=user_id).first()
    if user is None:
        err = f"User with user_id: {user_id} does not exist"
    elif user.type != student_type:
        err = f"User {user_id} is not {student_type} (type {user.type})"

    return err

def validate_is_tutor(session: sa.orm.Session, user_id: int):
    err = None
    user = session.query(models.User).filter_by(id=user_id).first()
    if user is None:
        err = f"User with user_id: {user_id} does not exist"
    if user.type != tutor_type:
        err = f"User {user_id} is not {tutor_type} (type {user.type})"

    return err

def validate_is_user(session: sa.orm.Session, user_id: int):
    err = None
    user = session.query(models.User).filter_by(id=user_id).first()
    if user is None:
        err = f"User {user_id} does not exist"
    return err

# TODO: Consolidate these into one function

def validate_is_test(session: sa.orm.Session, test_id: int):
    err = None
    test = session.query(models.Test).filter_by(id=test_id).first()
    if test is None:
        err = f"Test {test_id} does not exist"
    return err

def validate_is_sat(session: sa.orm.Session, test_id: int):
    err = None
    test = session.query(models.Test).filter_by(id=test_id).first()
    if test is None:
        err = f"Test with test_id: {test_id} does not exist"
    elif test.type != sat_type:
        err = f"Test {test_id} is not {sat_type} (type {test.type})"

    return err

def validate_is_psat(session: sa.orm.Session, test_id: int):
    err = None
    test = session.query(models.Test).filter_by(id=test_id).first()
    if test is None:
        err = f"Test with test_id: {test_id} does not exist"
    elif test.type != sat_type:
        err = f"Test {test_id} is not {psat_type} (type {test.type})"

    return err

def validate_is_act(session: sa.orm.Session, test_id: int):
    err = None
    test = session.query(models.Test).filter_by(id=test_id).first()
    if test is None:
        err = f"Test with test_id: {test_id} does not exist"
    elif test.type != sat_type:
        err = f"Test {test_id} is not {act_type} (type {test.type})"

    return err


# Tutoring sessions

def validate_is_tutoring_session(session: sa.orm.Session, tutoring_session_id: int):
    err = None
    tutoring_session = session.query(models.TutoringSession).filter_by(id=tutoring_session_id).first()
    if tutoring_session is None:
        err = f"Tutoring_session {tutoring_session_id} does not exist"
    return err