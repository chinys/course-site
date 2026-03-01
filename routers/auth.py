import bcrypt
import jwt
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Request, HTTPException, status

SECRET_KEY = "my_super_secret_key_for_course_site"  # In production, use env variable
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 days

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def get_password_hash(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

class NotAuthenticatedException(Exception):
    pass

def get_current_user_id(request: Request) -> Optional[int]:
    token = request.cookies.get("session_token")
    if not token:
        raise NotAuthenticatedException("Not authenticated")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise NotAuthenticatedException("Invalid token")
        return int(user_id)
    except jwt.PyJWTError:
        raise NotAuthenticatedException("Invalid token")

from fastapi import APIRouter, Depends, Form, Response
from fastapi.responses import RedirectResponse
from sqlmodel import Session, select
from core.database import get_session
from models import User

router = APIRouter(prefix="/auth", tags=["auth"])

def get_current_admin_user(
    request: Request,
    user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session)
) -> User:
    user = session.get(User, user_id)
    if not user or user.role != "ADMIN":
        raise NotAuthenticatedException("Not an admin")
    return user

@router.post("/login")
def login(
    response: Response,
    email: str = Form(...),
    password: str = Form(...),
    remember_id: Optional[str] = Form(None),
    auto_login: Optional[str] = Form(None),
    session: Session = Depends(get_session)
):
    user = session.exec(select(User).where(User.email == email)).first()
    if not user or not verify_password(password, user.hashed_password):
        # Redirect back with error
        return RedirectResponse(url="/admin/login?error=Invalid+credentials", status_code=303)
    
    if auto_login:
        expires_delta = timedelta(days=30)
        max_age_val = int(expires_delta.total_seconds())
    else:
        expires_delta = timedelta(days=1)
        max_age_val = None # Expires on browser close

    access_token = create_access_token(data={"sub": str(user.id)}, expires_delta=expires_delta)
    
    response = RedirectResponse(url="/admin", status_code=303)
    if max_age_val is not None:
        response.set_cookie(
            key="session_token", value=access_token, httponly=True, max_age=max_age_val, samesite="lax"
        )
    else:
        response.set_cookie(
            key="session_token", value=access_token, httponly=True, samesite="lax"
        )
        
    if remember_id:
        response.set_cookie(
            key="saved_email", value=email, max_age=30*24*60*60, samesite="lax"
        )
    else:
        response.delete_cookie("saved_email")
        
    return response

@router.get("/logout")
def logout():
    response = RedirectResponse(url="/admin/login", status_code=303)
    response.delete_cookie("session_token")
    return response
