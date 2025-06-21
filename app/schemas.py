import datetime
import sqlalchemy as sa
from pydantic import BaseModel
from typing import Optional, List, Literal

## I can define whatever models I want derived from the BaseModel to provide different fields for different endpoints

# Users

class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: Optional[str]
    email: Optional[str]

class UserPasswordUpdate(BaseModel):
    password: str
    new_password: str

class User(UserBase): # how can i do calculations? for example, "time since user was added?"
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    type: str

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
    # type: Literal["student"] = "student"  # Ensure type is always "student"
    tutor_id: Optional[int] = None

    class Config:
        from_attributes = True

# Tutors

class TutorCreate(UserCreate):
    pass

class TutorUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None

class Tutor(User):
    # type: Literal["tutor"] = "tutor"  # Ensure type is always "tutor"

    class Config:
        from_attributes = True