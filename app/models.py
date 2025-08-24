import sqlalchemy as sa
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from typing import Optional

class Base(sa.orm.DeclarativeBase):
    pass

class User(Base):
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

    id = mapped_column(sa.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    # tutor_id: Mapped[Optional[int]] = mapped_column(nullable=True)
    parent_name: Mapped[Optional[str]] = mapped_column(sa.String,nullable=True)
    tutor_id: Mapped[int] = mapped_column(sa.ForeignKey("tutors.id"))
    tests: Mapped[list["Test"]] = relationship(back_populates="student")
    tutoring_sessions: Mapped[list["TutoringSession"]] = relationship(back_populates="student")
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

    id = mapped_column(sa.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    # favorite_color: Mapped[Optional[str]] = mapped_column(sa.String,nullable=True)
    students: Mapped[list["Student"]] = relationship(back_populates="tutor")
    tutoring_sessions: Mapped[list["TutoringSession"]] = relationship(back_populates="tutor")

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
    test_notes: Mapped[str] = mapped_column(nullable=False)
    student_id: Mapped[int] = mapped_column(sa.ForeignKey("students.id"))
    student: Mapped["Student"] = relationship(back_populates="tests")
    tutoring_sessions: Mapped[list["TutoringSession"]] = relationship(back_populates="test")

    __mapper_args__ = {
        "polymorphic_identity": "test",
        "polymorphic_on": "type",
        "with_polymorphic": "*",
    }

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id}, name={self.name}, email={self.email}, type={self.type})"
    
class SAT(Test):
    __tablename__ = "SATs"

    id = mapped_column(sa.ForeignKey("tests.id", ondelete="CASCADE"), primary_key=True)
    english_score: Mapped[int] = mapped_column(nullable=False)
    math_score: Mapped[int] = mapped_column(nullable=False)
    
    __mapper_args__ = {
        "polymorphic_identity": "SAT",
        "inherit_condition": id == Test.id,
    }

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(id={self.id}, score={self.english_score + self.math_score}," 
            f"english_score={self.english_score}, math_score={self.math_score})"
        )
    
class PSAT(Test):
    __tablename__ = "PSATs"

    id = mapped_column(sa.ForeignKey("tests.id", ondelete="CASCADE"), primary_key=True)
    english_score: Mapped[int] = mapped_column(nullable=False)
    math_score: Mapped[int] = mapped_column(nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "PSAT",
        "inherit_condition": id == Test.id,
    }

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(id={self.id}, score={self.english_score + self.math_score}," 
            f"english_score={self.english_score}, math_score={self.math_score})"
        )
    
class ACT(Test):
    __tablename__ = "ACTs"

    id = mapped_column(sa.ForeignKey("tests.id", ondelete="CASCADE"), primary_key=True)
    english_score: Mapped[int] = mapped_column(nullable=False)
    math_score: Mapped[int] = mapped_column(nullable=False)
    reading_score: Mapped[int] = mapped_column(nullable=False)
    science_score: Mapped[int] = mapped_column(nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "ACT",
        "inherit_condition": id == Test.id,
    }

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(id={self.id}, score={(self.english_score + self.math_score + self.reading_score + self.science_score) / 4},"
            f"english_score={self.english_score}, math_score={self.math_score})"
        )


class TutoringSession(Base):
    __tablename__ = 'tutoring_sessions'

    id: Mapped[int] = mapped_column(sa.Sequence('id_seq'), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(sa.TIMESTAMP, default=sa.func.now())
    updated_at: Mapped[datetime] = mapped_column(sa.TIMESTAMP, default=sa.func.now())
    date_completed: Mapped[datetime] = mapped_column(sa.TIMESTAMP,nullable=True)
    payment_amount: Mapped[int] = mapped_column(nullable=True,default=60)
    session_notes: Mapped[str] = mapped_column(nullable=True)
    student_id: Mapped[int] = mapped_column(sa.ForeignKey("students.id"))
    student: Mapped["Student"] = relationship(back_populates="tutoring_sessions")
    tutor_id: Mapped[int] = mapped_column(sa.ForeignKey("tutors.id"))
    tutor: Mapped["Tutor"] = relationship(back_populates="tutoring_sessions")
    test_id: Mapped[int] = mapped_column(sa.ForeignKey("tests.id"))
    tutor: Mapped["Test"] = relationship(back_populates="tutoring_sessions")

    def __repr__(self) -> str:
        return (
    f"{self.__class__.__name__}(id={self.id!r},"
    f"created_at={self.created_at}, updated_at={self.updated_at}, "
    f"session_notes={self.session_notes}")