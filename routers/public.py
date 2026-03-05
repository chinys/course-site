from fastapi import APIRouter, Request, HTTPException
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select
from fastapi import Depends
from core.database import get_session
from models import Course, Lesson, Category

import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

router = APIRouter(tags=["public"])
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

@router.get("/")
def home(request: Request, session: Session = Depends(get_session)):
    courses = session.exec(select(Course)).all()
    categories = session.exec(select(Category).order_by(Category.order)).all()
    return templates.TemplateResponse(
        request=request, name="public/index.html", context={"categories": categories, "courses": courses}
    )

@router.get("/courses/{course_id}")
def course_detail(request: Request, course_id: int, session: Session = Depends(get_session)):
    course = session.get(Course, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    categories = session.exec(select(Category).order_by(Category.order)).all()
    lessons = session.exec(select(Lesson).where(Lesson.course_id == course_id).order_by(Lesson.order)).all()
    return templates.TemplateResponse(
        request=request, name="public/course.html", context={"categories": categories, "course": course, "lessons": lessons}
    )

@router.get("/courses/{course_id}/lessons/{lesson_id}")
def lesson_detail(request: Request, course_id: int, lesson_id: int, session: Session = Depends(get_session)):
    course = session.get(Course, course_id)
    lesson = session.get(Lesson, lesson_id)
    if not course or not lesson or lesson.course_id != course_id:
        raise HTTPException(status_code=404, detail="Lesson not found")
        
    categories = session.exec(select(Category).order_by(Category.order)).all()
    all_lessons = session.exec(select(Lesson).where(Lesson.course_id == course_id).order_by(Lesson.order)).all()
    
    # Calculate previous and next lessons
    prev_lesson = None
    next_lesson = None
    for i, l in enumerate(all_lessons):
        if l.id == lesson_id:
            if i > 0:
                prev_lesson = all_lessons[i-1]
            if i < len(all_lessons) - 1:
                next_lesson = all_lessons[i+1]
            break
            
    return templates.TemplateResponse(
        request=request, 
        name="public/lesson.html", 
        context={
            "categories": categories,
            "course": course, 
            "lesson": lesson, 
            "prev_lesson": prev_lesson, 
            "next_lesson": next_lesson,
            "all_lessons": all_lessons
        }
    )
