import sqlalchemy as sa
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from typing import List, Optional

class Base(sa.orm.DeclarativeBase):
    pass

class User(Base): # TODO: add delete cascade for students and tutors tables (if not automatic)
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(sa.String, unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(sa.TIMESTAMP, default=sa.func.now())
    updated_at: Mapped[datetime] = mapped_column(sa.TIMESTAMP, default=sa.func.now())
    type: Mapped[str] = mapped_column(nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "user",
        "polymorphic_on": "type",
        "with_polymorphic": "*",
    }

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id}, name={self.name}, email={self.email}, type={self.type})"

class Student(User):
    __tablename__ = "students"

    # check below relationship is necessary

    # tests = relationship(
    #     "Test",
    #     backref="students",
    #     cascade="all, delete-orphan",
    #     single_parent=True  # Ensures a test can belong to only one student
    # )

    id = mapped_column(sa.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    tutor_id: Mapped[Optional[int]] = mapped_column(nullable=True)
    parent_name: Mapped[Optional[str]] = mapped_column(sa.String,nullable=True)
    # parent_email: Mapped[Optional[str]] = mapped_column(sa.String,nullable=True)
    # completed_exit_survey: Mapped[bool] = mapped_column(sa.Boolean,default=False)

    __mapper_args__ = {
        "polymorphic_identity": "student",
        "inherit_condition": id == User.id,
    }

    # def __repr__(self):
    #     return f"{self.__class__.__name__}(id={self.id}, name={self.name}, email={self.email}, tutor_id={self.tutor_id})"
        
class Tutor(User):
    __tablename__ = "tutors"

    # check below relationship is necessary
    
    # tests = relationship(
    #     "Test",
    #     backref="tutors",
    #     cascade="all, delete-orphan",
    #     single_parent=True  # Ensures a test can belong to only one student
    # )


    id = mapped_column(sa.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    # favorite_color: Mapped[Optional[str]] = mapped_column(sa.String,nullable=True)
    # students = relationship("Student", back_populates="tutor")

    __mapper_args__ = {
        "polymorphic_identity": "tutor",
        "inherit_condition": id == User.id,
    }

    # def __repr__(self):
    #     return f"{self.__class__.__name__}(id={self.id}, name={self.name}, email={self.email})"

class Test(Base): 
    __tablename__ = "tests"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    date_completed: Mapped[datetime] = mapped_column(sa.TIMESTAMP, nullable=True) 
    created_at: Mapped[datetime] = mapped_column(sa.TIMESTAMP, default=sa.func.now())
    updated_at: Mapped[datetime] = mapped_column(sa.TIMESTAMP, default=sa.func.now())
    type: Mapped[str] = mapped_column(nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "test",
        "polymorphic_on": "type",
    }

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id}, name={self.name}, email={self.email}, type={self.type})"


class TutoringSession(Base):
    __tablename__ = 'sessions'

    # This creates an __init__ method with each param as an optional input
    id: Mapped[int] = mapped_column(sa.Sequence('id_seq'), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(sa.TIMESTAMP, default=sa.func.now())
    updated_at: Mapped[datetime] = mapped_column(sa.TIMESTAMP, default=sa.func.now())
    date_completed = sa.Column(sa.TIMESTAMP,nullable=True) # how to input the date? -can be done in pydantic model
    payment_amount: Mapped[Optional[int]] = mapped_column(nullable=True)
    session_notes: Mapped[str] = mapped_column(nullable=True)
    fk_students: Mapped[int] = mapped_column(sa.ForeignKey(Student.id)) # can i use 2 fks to the users table now? are fks even appropriate?
    fk_tutors: Mapped[int] = mapped_column(sa.ForeignKey(Tutor.id))
    fk_tests: Mapped[int] = mapped_column(sa.ForeignKey(Test.id), nullable=True)

    def __repr__(self) -> str:
        return (
    f"{self.__class__.__name__}(id={self.id!r}, student_id={self.fk_students!r}, "
    f"created_at={self.created_at}, updated_at={self.updated_at}, "
    f"session_notes={self.session_notes}")