from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    role: str = Field(default="USER")

class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    order: int = Field(default=0)
    
    courses: List["Course"] = Relationship(back_populates="category")

class Course(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = None
    thumbnail_url: Optional[str] = None
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")
    
    category: Optional[Category] = Relationship(back_populates="courses")
    lessons: List["Lesson"] = Relationship(back_populates="course", cascade_delete=True)

class Lesson(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    order: int = Field(default=0)
    course_id: Optional[int] = Field(default=None, foreign_key="course.id")
    
    course: Optional[Course] = Relationship(back_populates="lessons")
