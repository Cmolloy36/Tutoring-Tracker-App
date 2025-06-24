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
    print(user)
    if user is None:
        err = f"User with user_id: {user_id} does not exist"
    elif user.type != "student":
        err = f"User {user_id} is not student (type {user.type})"

    return err

def validate_is_tutor(session: sa.orm.Session, user_id: int):
    err = None
    user = session.query(models.User).filter_by(id=user_id).first()
    print(user)
    if user is None:
        err = f"User with user_id: {user_id} does not exist"
    if user.type != "tutor":
        err = f"User {user_id} is not tutor (type {user.type})"

    return err

def validate_is_user(session: sa.orm.Session, user_id: int):
    err = None
    user = session.query(models.User).filter_by(id=user_id).first()
    if user is None:
        err = f"User {user_id} does not exist"
    return err

# def validate_user_type(session: sa.orm.Session, user_id: int, user_type: str):
#     err = None
#     user = session.query(models.User).filter_by(id=user_id).first()
#     if user.type is not user_type:
#         err = f"User {user_id} is type {user.type}, not {user_type}"

#     return err