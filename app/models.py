import sqlalchemy as sa
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from typing import List, Optional

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
    }

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id}, name={self.name}, email={self.email}, type={self.type})"

class Student(User):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(sa.ForeignKey("users.id"), primary_key=True)
    tutor_id: Mapped[Optional[int]] = mapped_column(sa.ForeignKey("users.id"), nullable=True)
    parent_name: Mapped[Optional[str]] = mapped_column(sa.String,nullable=True)

    # Relationship to access the tutor object
    tutor = relationship("Tutor", back_populates="students")

    __mapper_args__ = {
        "polymorphic_identity": "student",
        "inherit_condition": id == User.id,
    }

    # def __repr__(self):
    #     return f"{self.__class__.__name__}(id={self.id}, name={self.name}, email={self.email}, tutor_id={self.tutor_id})"
        
class Tutor(User):
    __tablename__ = "tutors"

    id: Mapped[int] = mapped_column(sa.ForeignKey("users.id"), primary_key=True)
    # favorite_color: Mapped[Optional[str]] = mapped_column(sa.String,nullable=True)
    students = relationship("Student", back_populates="tutor")

    __mapper_args__ = {
        "polymorphic_identity": "tutor",
    }

    # def __repr__(self):
    #     return f"{self.__class__.__name__}(id={self.id}, name={self.name}, email={self.email})"

class TutoringSession(Base):
    __tablename__ = 'sessions_table'

    # This creates an __init__ method with each param as an optional input
    id: Mapped[int] = mapped_column(sa.Sequence('id_seq'), primary_key=True)
    created_at = sa.Column(sa.TIMESTAMP,default=sa.func.now())
    updated_at = sa.Column(sa.TIMESTAMP,default=sa.func.now())
    date_completed = sa.Column(sa.TIMESTAMP,nullable=True) # how to input the date?
    session_notes: Mapped[str] = mapped_column(nullable=True)
    fk_students: Mapped[int] = mapped_column(sa.ForeignKey(Student.id))
    # fk_tests: Mapped[int] = mapped_column(sa.ForeignKey(Test.id))

    def __repr__(self) -> str:
        return (
    f"Session(id={self.id!r}, student_id={self.fk_students!r}, "
    f"created_at={self.created_at}, updated_at={self.updated_at}, "
    f"session_notes={self.session_notes}")