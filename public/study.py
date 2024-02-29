from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from database import get_db
from typing import List
from models.models import Student, Faculty, StudentCreate, StudentUpdate, FacultyCreate, FacultyUpdate, StudentResponse, \
    FacultyResponse

router = APIRouter()

# Получить список студентов
@router.get("/students/", response_model=List[StudentResponse])
async def get_students(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    students = await db.execute(select(Student).offset(skip).limit(limit))
    return students.scalars().all()

# Поиск студента по идентификатору
@router.get("/students/{student_id}", response_model=StudentResponse)
async def get_student(student_id: int, db: Session = Depends(get_db)):
    student = await db.execute(select(Student).filter(Student.id == student_id))
    result = student.scalar()
    if not result:
        raise HTTPException(status_code=404, detail="Студент не найден")
    return result

# Добавить нового студента
@router.post("/students/", response_model=StudentResponse)
async def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    new_student = Student(**student.dict())
    db.add(new_student)
    await db.commit()
    await db.refresh(new_student)
    return new_student

# Обновление записи о студенте
@router.put("/students/{student_id}", response_model=StudentResponse)
async def update_student(student_id: int, student: StudentUpdate, db: Session = Depends(get_db)):
    db_student = await db.execute(select(Student).filter(Student.id == student_id))
    result = db_student.scalar()
    if not result:
        raise HTTPException(status_code=404, detail="Студент не найден")
    for var, value in student.dict().items():
        setattr(result, var, value)
    await db.commit()
    await db.refresh(result)
    return result

# Частично обновить запись
@router.patch("/students/{student_id}", response_model=StudentResponse)
async def update_student(student_id: int, lastname: str = None, name: str = None, group: str = None, course: int = None,
                         faculty_id: int = None, db: Session = Depends(get_db)):
    db_student = await db.get(Student, student_id)
    if not db_student:
        raise HTTPException(status_code=404, detail="Студент не найден")
    if lastname:
        db_student.lastname = lastname
    if name:
        db_student.name = name
    if group:
        db_student.group = group
    if course:
        db_student.course = course
    if faculty_id:
        db_student.faculty_id = faculty_id

    await db.commit()
    await db.refresh(db_student)
    return db_student

# Удалить запись о студенте
@router.delete("/students/{student_id}")
async def delete_student(student_id: int, db: Session = Depends(get_db)):
    db_student = await db.execute(select(Student).filter(Student.id == student_id))
    result = db_student.scalar()
    if not result:
        raise HTTPException(status_code=404, detail="Студент не найден")
    await db.delete(result)
    await db.commit()
    return {"message": "Студент удален"}

# Получить список факультетов
@router.get("/faculties/", response_model=List[FacultyResponse])
async def get_faculties(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    faculties = await db.execute(select(Faculty).offset(skip).limit(limit))
    return faculties.scalars().all()

# Найти факультет
@router.get("/faculties/{faculty_id}", response_model=FacultyResponse)
async def get_faculty(faculty_id: int, db: Session = Depends(get_db)):
    faculty = await db.execute(select(Faculty).filter(Faculty.id == faculty_id))
    result = faculty.scalar()
    if not result:
        raise HTTPException(status_code=404, detail="Факультет не найден")
    return result

# Добавить новый факультет
@router.post("/faculties/", response_model=FacultyResponse)
async def create_faculty(faculty: FacultyCreate, db: Session = Depends(get_db)):
    new_faculty = Faculty(**faculty.dict())
    db.add(new_faculty)
    await db.commit()
    await db.refresh(new_faculty)
    return new_faculty

# Обновить запись о факультете
@router.put("/faculties/{faculty_id}", response_model=FacultyResponse)
async def update_faculty(faculty_id: int, faculty: FacultyUpdate, db: Session = Depends(get_db)):
    db_faculty = await db.execute(select(Faculty).filter(Faculty.id == faculty_id))
    result = db_faculty.scalar()
    if not result:
        raise HTTPException(status_code=404, detail="Факультет не найден")
    for var, value in faculty.dict().items():
        setattr(result, var, value)
    await db.commit()
    await db.refresh(result)
    return result

# Частично обновить запись о факультете
@router.patch("/faculties/{faculty_id}", response_model=FacultyResponse)
async def update_faculty(faculty_id: int, name: str = None, director: str = None, db: Session = Depends(get_db)):
    db_faculty = await db.get(Faculty, faculty_id)
    if not db_faculty:
        raise HTTPException(status_code=404, detail="Факультет не найден")
    if name:
        db_faculty.name = name
    if director:
        db_faculty.director = director
    await db.commit()
    await db.refresh(db_faculty)
    return db_faculty

# Удалить факультет
@router.delete("/faculties/{faculty_id}")
async def delete_faculty(faculty_id: int, db: Session = Depends(get_db)):
    db_faculty = await db.execute(select(Faculty).filter(Faculty.id == faculty_id))
    result = db_faculty.scalar()
    if not result:
        raise HTTPException(status_code=404, detail="Факультет не найден")
    await db.delete(result)
    await db.commit()
    return {"message": "Факультет удален"}