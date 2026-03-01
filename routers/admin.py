from fastapi import APIRouter, Depends, Request, Form, UploadFile, File, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlmodel import Session, select
from core.database import get_session
from routers.auth import get_current_admin_user
from models import User, Course, Lesson, Category
import shutil
import os

router = APIRouter(prefix="/admin", tags=["admin"])
templates = Jinja2Templates(directory="templates")

@router.get("/login")
def login_page(request: Request, error: str = None):
    saved_email = request.cookies.get("saved_email", "")
    return templates.TemplateResponse(
        request=request, name="admin/login.html", context={"error": error, "saved_email": saved_email}
    )

@router.get("/")
def admin_dashboard(
    request: Request,
    user: User = Depends(get_current_admin_user),
    session: Session = Depends(get_session)
):
    courses = session.exec(select(Course)).all()
    return templates.TemplateResponse(
        request=request, name="admin/dashboard.html", context={"user": user, "courses": courses}
    )

@router.get("/courses/new")
def new_course_page(
    request: Request,
    user: User = Depends(get_current_admin_user),
    session: Session = Depends(get_session)
):
    categories = session.exec(select(Category).order_by(Category.order)).all()
    return templates.TemplateResponse(
        request=request, name="admin/course_form.html", context={"user": user, "categories": categories}
    )

@router.post("/courses/new")
def create_course(
    request: Request,
    title: str = Form(...),
    description: str = Form(""),
    category_id: int = Form(...),
    thumbnail: UploadFile = File(None),
    user: User = Depends(get_current_admin_user),
    session: Session = Depends(get_session)
):
    thumbnail_url = None
    if thumbnail and thumbnail.filename:
        # Save file to static/uploads
        os.makedirs("static/uploads", exist_ok=True)
        file_path = f"static/uploads/{thumbnail.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(thumbnail.file, buffer)
        thumbnail_url = f"/{file_path}"

    new_course = Course(title=title, description=description, thumbnail_url=thumbnail_url)
    session.add(new_course)
    session.commit()
    return RedirectResponse(url="/admin", status_code=303)

@router.get("/courses/{course_id}")
def course_details(
    request: Request,
    course_id: int,
    user: User = Depends(get_current_admin_user),
    session: Session = Depends(get_session)
):
    course = session.get(Course, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # Retrieve lessons ordered by their 'order' field
    lessons = session.exec(select(Lesson).where(Lesson.course_id == course_id).order_by(Lesson.order)).all()
    return templates.TemplateResponse(
        request=request, name="admin/course_detail.html", context={"user": user, "course": course, "lessons": lessons}
    )

@router.get("/courses/{course_id}/lessons/new")
def new_lesson_page(
    request: Request,
    course_id: int,
    user: User = Depends(get_current_admin_user),
    session: Session = Depends(get_session)
):
    course = session.get(Course, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    return templates.TemplateResponse(
        request=request, name="admin/lesson_form.html", context={"user": user, "course": course}
    )

@router.post("/courses/{course_id}/lessons/new")
def create_lesson(
    request: Request,
    course_id: int,
    title: str = Form(...),
    content: str = Form(""),
    order: int = Form(0),
    user: User = Depends(get_current_admin_user),
    session: Session = Depends(get_session)
):
    course = session.get(Course, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
        
    new_lesson = Lesson(title=title, content=content, order=order, course_id=course_id)
    session.add(new_lesson)
    session.commit()
    
    return RedirectResponse(url=f"/admin/courses/{course_id}", status_code=303)

@router.get("/courses/{course_id}/edit")
def edit_course_page(
    request: Request,
    course_id: int,
    user: User = Depends(get_current_admin_user),
    session: Session = Depends(get_session)
):
    course = session.get(Course, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    categories = session.exec(select(Category).order_by(Category.order)).all()
    return templates.TemplateResponse(
        request=request, name="admin/course_edit.html", context={"user": user, "course": course, "categories": categories}
    )

@router.post("/courses/{course_id}/edit")
def edit_course(
    request: Request,
    course_id: int,
    title: str = Form(...),
    description: str = Form(""),
    category_id: int = Form(...),
    thumbnail: UploadFile = File(None),
    user: User = Depends(get_current_admin_user),
    session: Session = Depends(get_session)
):
    course = session.get(Course, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
        
    course.title = title
    course.description = description
    course.category_id = category_id
    
    if thumbnail and thumbnail.filename:
        # Save file to static/uploads
        os.makedirs("static/uploads", exist_ok=True)
        file_path = f"static/uploads/{thumbnail.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(thumbnail.file, buffer)
        course.thumbnail_url = f"/{file_path}"
        
    session.add(course)
    session.commit()
    return RedirectResponse(url=f"/admin/courses/{course_id}", status_code=303)

@router.get("/courses/{course_id}/lessons/{lesson_id}/edit")
def edit_lesson_page(
    request: Request,
    course_id: int,
    lesson_id: int,
    user: User = Depends(get_current_admin_user),
    session: Session = Depends(get_session)
):
    course = session.get(Course, course_id)
    lesson = session.get(Lesson, lesson_id)
    if not course or not lesson or lesson.course_id != course_id:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    return templates.TemplateResponse(
        request=request, name="admin/lesson_edit.html", context={"user": user, "course": course, "lesson": lesson}
    )

@router.post("/courses/{course_id}/lessons/{lesson_id}/edit")
def edit_lesson(
    request: Request,
    course_id: int,
    lesson_id: int,
    title: str = Form(...),
    content: str = Form(""),
    order: int = Form(0),
    user: User = Depends(get_current_admin_user),
    session: Session = Depends(get_session)
):
    lesson = session.get(Lesson, lesson_id)
    if not lesson or lesson.course_id != course_id:
        raise HTTPException(status_code=404, detail="Lesson not found")
        
    lesson.title = title
    lesson.content = content
    lesson.order = order
    session.add(lesson)
    session.commit()
    
    return RedirectResponse(url=f"/admin/courses/{course_id}", status_code=303)
