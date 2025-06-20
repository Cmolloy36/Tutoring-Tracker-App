import datetime
import sqlalchemy as sa
from pydantic import BaseModel
from typing import Optional, List, Literal

# Users

class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase): # What happens if I specify a field here?
    password: str

class UserUpdate(BaseModel):
    name: Optional[str]
    email: Optional[str]

class User(UserBase): # how can i do calculations? for example, "time since user was added?"
    id:int
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        from_attributes = True

# Students

class StudentCreate(UserCreate):
    pass

class StudentUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    tutor_id: Optional[int] = None

class Student(User):
    type: Literal["student"] = "student"  # Ensure type is always "student"
    tutor_id: Optional[int] = None  # Make this optional to match the model

    class Config:
        from_attributes = True

# Tutors

class TutorCreate(UserCreate):
    pass

class TutorUpdate(BaseModel):
    pass

class Tutor(User):
    type: Literal["tutor"] = "tutor"  # Ensure type is always "tutor"

    class Config:
        from_attributes = True