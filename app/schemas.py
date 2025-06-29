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
    # TODO: Return students associated with tutor

    class Config:
        from_attributes = True

# Tests

class TestBase(BaseModel):
    name: str
    date_completed: datetime.date #how do i input date in the json payload ?
    test_notes: str
    student_id: int

class TestCreate(TestBase):
    pass

class TestUpdate(BaseModel):
    name: Optional[str] = None
    date_completed: Optional[datetime.date] = None
    test_notes: Optional[str] = None
    student_id: Optional[int] = None
    
class Test(TestBase):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    type: str
    student_id: int
    # student_name: str # get student method from id
    test_notes: str
    #consider adding a get_score() method to get score of any test

    class Config:
        from_attributes = True

# SATs

class SATCreate(TestCreate):
    english_score: int
    math_score: int

class SATUpdate(BaseModel):
    name: Optional[str] = None
    date_completed: Optional[datetime.date] = None
    test_notes: Optional[str] = None
    student_id: Optional[int] = None
    english_score: Optional[int] = None
    math_score: Optional[int] = None
    
class SAT(Test):
    total_score: int
    english_score: int
    math_score: int

    class Config:
        from_attributes = True

# PSATs

class PSATCreate(TestCreate):
    english_score: int
    math_score: int

class PSATUpdate(BaseModel):
    name: Optional[str] = None
    date_completed: Optional[datetime.date] = None
    test_notes: Optional[str] = None
    student_id: Optional[int] = None
    english_score: Optional[int] = None
    math_score: Optional[int] = None
    
class PSAT(Test):
    total_score: int
    english_score: int
    math_score: int

    class Config:
        from_attributes = True

# ACTs

class ACTCreate(TestCreate):
    english_score: int
    math_score: int
    reading_score: int
    science_score: int

class ACTUpdate(BaseModel):
    name: Optional[str] = None
    date_completed: Optional[datetime.date] = None
    test_notes: Optional[str] = None
    student_id: Optional[int] = None
    english_score: Optional[int] = None
    math_score: Optional[int] = None
    reading_score: Optional[int] = None
    science_score: Optional[int] = None
    
class ACT(Test):
    total_score: int
    english_score: int
    math_score: int
    reading_score: int
    science_score: int

    class Config:
        from_attributes = True