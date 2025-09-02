from enum import Enum

class TestType(str, Enum):
    SAT = "SAT"
    ACT = "ACT" 
    PSAT = "PSAT"

class UserType(str, Enum):
    tutor = "tutor"
    student = "student"
    parent = "parent"