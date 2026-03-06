from fastapi import APIRouter, Depends, Request, Form, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlmodel import Session, select
from core.database import get_session
from routers.auth import get_current_admin_user
from models import User, Notice
from datetime import datetime
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

router = APIRouter(prefix="/admin/notices", tags=["admin-notices"])
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))


@router.get("/")
def admin_notices_list(
    request: Request,
    user: User = Depends(get_current_admin_user),
    session: Session = Depends(get_session)
):
    """관리자 공지사항 목록"""
    notices = session.exec(
        select(Notice).order_by(Notice.is_pinned.desc(), Notice.created_at.desc())
    ).all()
    return templates.TemplateResponse(
        request=request,
        name="admin/notice_list.html",
        context={"user": user, "notices": notices}
    )


@router.get("/new")
def admin_notice_new(
    request: Request,
    user: User = Depends(get_current_admin_user),
    session: Session = Depends(get_session)
):
    """새 공지사항 작성 폼"""
    return templates.TemplateResponse(
        request=request,
        name="admin/notice_form.html",
        context={"user": user, "notice": None}
    )


@router.post("/new")
def admin_notice_create(
    request: Request,
    title: str = Form(...),
    content: str = Form(...),
    is_pinned: str = Form("false"),
    is_active: str = Form("false"),
    user: User = Depends(get_current_admin_user),
    session: Session = Depends(get_session)
):
    """새 공지사항 생성"""
    notice = Notice(
        title=title,
        content=content,
        is_pinned=is_pinned == "true",
        is_active=is_active == "true"
    )
    session.add(notice)
    session.commit()
    return RedirectResponse(url="/admin/notices", status_code=303)


@router.get("/{notice_id}")
def admin_notice_detail(
    request: Request,
    notice_id: int,
    user: User = Depends(get_current_admin_user),
    session: Session = Depends(get_session)
):
    """공지사항 상세"""
    notice = session.get(Notice, notice_id)
    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")
    return templates.TemplateResponse(
        request=request,
        name="admin/notice_detail.html",
        context={"user": user, "notice": notice}
    )


@router.get("/{notice_id}/edit")
def admin_notice_edit(
    request: Request,
    notice_id: int,
    user: User = Depends(get_current_admin_user),
    session: Session = Depends(get_session)
):
    """공지사항 수정 폼"""
    notice = session.get(Notice, notice_id)
    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")
    return templates.TemplateResponse(
        request=request,
        name="admin/notice_form.html",
        context={"user": user, "notice": notice}
    )


@router.post("/{notice_id}/edit")
def admin_notice_update(
    request: Request,
    notice_id: int,
    title: str = Form(...),
    content: str = Form(...),
    is_pinned: str = Form("false"),
    is_active: str = Form("false"),
    user: User = Depends(get_current_admin_user),
    session: Session = Depends(get_session)
):
    """공지사항 수정"""
    notice = session.get(Notice, notice_id)
    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")

    notice.title = title
    notice.content = content
    notice.is_pinned = is_pinned == "true"
    notice.is_active = is_active == "true"
    notice.updated_at = datetime.utcnow()

    session.add(notice)
    session.commit()
    return RedirectResponse(url="/admin/notices", status_code=303)


@router.post("/{notice_id}/delete")
def admin_notice_delete(
    request: Request,
    notice_id: int,
    user: User = Depends(get_current_admin_user),
    session: Session = Depends(get_session)
):
    """공지사항 삭제"""
    notice = session.get(Notice, notice_id)
    if not notice:
        raise HTTPException(status_code=404, detail="Notice not found")
    
    session.delete(notice)
    session.commit()
    return RedirectResponse(url="/admin/notices", status_code=303)
