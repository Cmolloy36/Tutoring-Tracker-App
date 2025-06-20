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
    statement = sa.select(models.Student).where(models.Student.email==email)
    if session.scalars(statement).first() is None:
        return True
    return False

def hash_password(password: str): # What return type should the hash be? What lib do i use
    # ...
    return password
    
def validate_password(session: sa.orm.Session, password: str):
    # ...
    return True