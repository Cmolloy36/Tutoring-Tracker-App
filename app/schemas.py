import datetime
import sqlalchemy as sa
from pydantic import BaseModel
from typing import Optional, List, Literal

# Users

class UserBase(BaseModel):
    name: str
    email: str
    type: str

class UserCreate(UserBase): # What happens if I specify a field here?
    pass

class UserUpdate(UserBase):
    name: Optional[str]
    email: Optional[str]

class User(UserBase):
    id:int
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        from_attributes = True

# Students

class StudentCreate(UserCreate):
    pass

class StudentUpdate(UserUpdate):
    tutor_id: Optional[int] = None

class Student(User):
    type: Literal["student"] = "student"  # Ensure type is always "student"
    tutor_id: Optional[int] = None  # Make this optional to match the model

    class Config:
        from_attributes = True

# Tutors

class TutorCreate(UserCreate):
    pass

class TutorUpdate(UserUpdate):
    pass

class Tutor(User):
    type: Literal["tutor"] = "tutor"  # Ensure type is always "tutor"
    students: Optional[List[Student]] = []

    class Config:
        from_attributes = True