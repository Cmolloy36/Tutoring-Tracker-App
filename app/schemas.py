import datetime
from pydantic import BaseModel
from typing import Optional, Literal, Union


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
    tutor_id: Optional[int]

    class Config:
        from_attributes = True

# Tutors

class TutorCreate(UserCreate):
    pass

class TutorUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None

class Tutor(User):
    student_ids: Optional[list[int]]

    class Config:
        from_attributes = True

# UserCreate = Union[SATCreate, PSATCreate, ACTCreate]

UserResponse = Union[Student, Tutor]

# Tests

class TestBase(BaseModel):
    name: str
    date_completed: datetime.date #how do i input date in the json payload ?
    test_notes: str
    student_id: Optional[int] = None

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
    test_type: str
    #consider adding a get_score() method to get score of any test

    class Config:
        from_attributes = True

# SATs

class SATTestBase(TestBase):
    english_score: int
    math_score: int

class SATCreate(SATTestBase):
    test_type: Literal["SAT"] = "SAT"

class SATUpdate(BaseModel):
    name: Optional[str] = None
    date_completed: Optional[datetime.date] = None
    test_notes: Optional[str] = None
    student_id: Optional[int] = None
    english_score: Optional[int] = None
    math_score: Optional[int] = None
    
class SAT(Test):
    # total_score: int # How do i calculate this here?
    english_score: int
    math_score: int

    class Config:
        from_attributes = True

# PSATs

class PSATCreate(SATTestBase):
    test_type: Literal["PSAT"] = "PSAT"

class PSATUpdate(BaseModel):
    name: Optional[str] = None
    date_completed: Optional[datetime.date] = None
    test_notes: Optional[str] = None
    student_id: Optional[int] = None
    english_score: Optional[int] = None
    math_score: Optional[int] = None
    
class PSAT(Test):
    # total_score: int
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
    name: Optional[str] = None
    date_completed: Optional[datetime.date] = None
    test_notes: Optional[str] = None
    student_id: Optional[int] = None
    english_score: Optional[int] = None
    math_score: Optional[int] = None
    reading_score: Optional[int] = None
    science_score: Optional[int] = None
    
class ACT(Test):
    # total_score: int
    english_score: int
    math_score: int
    reading_score: int
    science_score: int

    class Config:
        from_attributes = True

TestCreate = Union[SATCreate, PSATCreate, ACTCreate]

TestResponse = Union[SAT, PSAT, ACT]

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
    date_completed: Optional[datetime.date] = None
    payment_amount: Optional[int] = None
    session_notes: Optional[str] = None
    student_id: Optional[int] = None
    tutor_id: Optional[int] = None
    test_id: int = None

class TutoringSession(BaseModel):
    date_completed: datetime.date
    payment_amount: int
    session_notes: str
    student_id: int # Include name?
    tutor_id: int # Include name?
    test_id: int

    class Config:
        from_attributes = True