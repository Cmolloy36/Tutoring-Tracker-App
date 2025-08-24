import datetime
import sqlalchemy as sa
from pydantic import BaseModel, Field
from typing import Optional, Annotated, Literal, Union

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
    name: Optional[str]
    email: Optional[str]
    tutor_id: Optional[int]

class Student(User):
    tutor_id: int

    class Config:
        from_attributes = True

# Tutors

class TutorCreate(UserCreate):
    pass

class TutorUpdate(BaseModel):
    name: Optional[str]
    email: Optional[str]

class Tutor(User):
    student_ids: list[int]

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
    name: Optional[str]
    date_completed: Optional[datetime.date]
    test_notes: Optional[str]
    student_id: Optional[int]
    
class Test(TestBase):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    type: str
    student_id: int
    student_name: str
    test_notes: str
    #consider adding a get_score() method to get score of any test

    class Config:
        from_attributes = True

# SATs

class SATCreate(TestCreate):
    test_type: Literal["SAT"] = "SAT"
    english_score: int
    math_score: int

class SATUpdate(BaseModel):
    name: Optional[str]
    date_completed: Optional[datetime.date]
    test_notes: Optional[str]
    student_id: Optional[int]
    english_score: Optional[int]
    math_score: Optional[int]
    
class SAT(Test):
    total_score: int
    english_score: int
    math_score: int

    class Config:
        from_attributes = True

# PSATs

class PSATCreate(TestCreate):
    test_type: Literal["PSAT"] = "PSAT"
    english_score: int
    math_score: int

class PSATUpdate(BaseModel):
    name: Optional[str]
    date_completed: Optional[datetime.date]
    test_notes: Optional[str]
    student_id: Optional[int]
    english_score: Optional[int]
    math_score: Optional[int]
    
class PSAT(Test):
    total_score: int
    english_score: int
    math_score: int

    class Config:
        from_attributes = True

# ACTs

class ACTCreate(TestCreate):
    test_type: Literal["ACT"] = "ACT"
    english_score: int
    math_score: int
    reading_score: int
    science_score: int

class ACTUpdate(BaseModel):
    name: Optional[str]
    date_completed: Optional[datetime.date]
    test_notes: Optional[str]
    student_id: Optional[int]
    english_score: Optional[int]
    math_score: Optional[int]
    reading_score: Optional[int]
    science_score: Optional[int]
    
class ACT(Test):
    total_score: int
    english_score: int
    math_score: int
    reading_score: int
    science_score: int

    class Config:
        from_attributes = True

TestCreate = Union[SATCreate, PSATCreate, ACTCreate]

# Tutoring Sessions

class TutoringSessionBase(BaseModel):
    date_completed: Optional[datetime.date]
    payment_amount: Optional[int]
    session_notes: str
    student_id: int
    tutor_id: int
    test_id: int

class TutoringSessionCreate(TutoringSessionBase):
    pass

class TutoringSessionUpdate(BaseModel):
    date_completed: Optional[datetime.date]
    payment_amount: Optional[int]
    session_notes: Optional[str]
    student_id: Optional[int]
    tutor_id: Optional[int]
    test_id: int

class TutoringSession(BaseModel):
    date_completed: datetime.date
    payment_amount: int
    session_notes: str
    student_id: int # Include name?
    tutor_id: int # Include name?
    test_id: int

    class Config:
        from_attributes = True