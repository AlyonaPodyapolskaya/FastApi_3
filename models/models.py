from sqlalchemy import Column, Integer, String, ForeignKey, Identity
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Student(Base):
    __tablename__ = "student"

    id = Column(Integer, Identity(start=1), primary_key=True)
    lastname = Column(String, index=True, nullable=False)
    name = Column(String, nullable=False)
    group = Column(String, nullable=False)
    course = Column(Integer, nullable=False)
    faculty_id = Column(Integer, ForeignKey("faculty.id"))
    faculty = relationship("Faculty", back_populates="students")

class Faculty(Base):
    __tablename__ = "faculty"

    id = Column(Integer, Identity(start=1), primary_key=True)
    name = Column(String, index=True, nullable=False)
    director = Column(String, nullable=False)
    students = relationship("Student", back_populates="faculty")

class StudentCreate(BaseModel):
    lastname: str
    name: str
    group: str
    course: int
    faculty_id: int

class StudentUpdate(BaseModel):
    lastname: Optional[str] = None
    name: Optional[str] = None
    group: Optional[str] = None
    course: Optional[int] = None
    faculty_id: Optional[int] = None

class FacultyCreate(BaseModel):
    name: str
    director: str

class FacultyUpdate(BaseModel):
    name: Optional[str] = None
    director: Optional[str] = None

class StudentResponse(BaseModel):
    id: int
    lastname: str
    name: str
    group: str
    course: int
    faculty_id: Optional[int]

class FacultyResponse(BaseModel):
    id: int
    name: str
    director: str