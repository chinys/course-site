# -*- coding: utf-8 -*-
"""
FastAPI 실무 마스터 강좌 업데이트 스크립트
- 기존 강좌/레슨을 삭제하지 않고 콘텐츠만 업데이트
- ID 를 유지하여 링크 깨짐 방지
"""
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from sqlmodel import Session, select
from core.database import engine, create_db_and_tables
from models import Category, Course, Lesson


def update_fastapi_course():
    """FastAPI 강좌 업데이트 (ID 유지)"""
    create_db_and_tables()
    
    with Session(engine) as session:
        # 1. 카테고리 확인
        statement = select(Category).where(Category.name == "프로그래밍")
        category = session.exec(statement).first()

        if not category:
            category = Category(name="프로그래밍", order=10)
            session.add(category)
            session.commit()
            session.refresh(category)
            print(f"'프로그래밍' 카테고리 생성됨 (ID: {category.id})")

        # 2. 기존 FastAPI 강좌 확인
        statement = select(Course).where(Course.title.like("%FastAPI%"))
        course = session.exec(statement).first()
        
        if not course:
            # 새 강좌 생성
            course = Course(
                title="FastAPI 실무 마스터",
                description="FastAPI 기초부터 비동기 DB, JWT 보안, 실시간 통신, 테스트, Docker 배포까지 현업 실무 기술을 배웁니다.",
                thumbnail_url="/static/uploads/fastapi_thumbnail.png",
                category_id=category.id
            )
            session.add(course)
            session.commit()
            session.refresh(course)
            print(f"FastAPI 강좌 생성됨 (ID: {course.id})")
        else:
            # 기존 강좌 정보 업데이트
            course.title = "FastAPI 실무 마스터"
            course.description = "FastAPI 기초부터 비동기 DB, JWT 보안, 실시간 통신, 테스트, Docker 배포까지 현업 실무 기술을 배웁니다."
            course.thumbnail_url = "/static/uploads/fastapi_thumbnail.png"
            session.add(course)
            session.commit()
            print(f"FastAPI 강좌 업데이트됨 (ID: {course.id})")

        # 3. 레슨 데이터 (10 개)
        lessons_data = [
            (1, "1. FastAPI 입문: 설치부터 Hello World 까지", get_lesson_1_content()),
            (2, "2. Path 와 Query 매개변수 (URL 로 데이터 받기)", get_lesson_2_content()),
            (3, "3. Pydantic 으로 Request Body 다루기", get_lesson_3_content()),
            (4, "4. Response Model 과 HTTP 상태 코드", get_lesson_4_content()),
            (5, "5. 예외 처리 (HTTPException 완벽 가이드)", get_lesson_5_content()),
            (6, "6. 의존성 주입 (Dependency Injection) 정복", get_lesson_6_content()),
            (7, "7. SQLAlchemy 비동기 데이터베이스", get_lesson_7_content()),
            (8, "8. JWT 인증과 보안 (로그인부터 토큰 갱신까지)", get_lesson_8_content()),
            (9, "9. 실시간 통신 (WebSockets & SSE)", get_lesson_9_content()),
            (10, "10. 테스트 작성법 (Pytest 완전 가이드)", get_lesson_10_content()),
        ]

        # 4. 레슨 업데이트 또는 생성
        for order, title, content in lessons_data:
            # 기존 레슨 확인 (order 로 찾기)
            statement = select(Lesson).where(
                (Lesson.course_id == course.id) & (Lesson.order == order)
            )
            lesson = session.exec(statement).first()
            
            if lesson:
                # 기존 레슨 업데이트 (ID 유지!)
                lesson.title = title
                lesson.content = content
                session.add(lesson)
                print(f"  [UPDATE] Lesson {lesson.id}: {title[:30]}...")
            else:
                # 새 레슨 생성
                lesson = Lesson(
                    title=title,
                    content=content,
                    order=order,
                    course_id=course.id
                )
                session.add(lesson)
                session.commit()
                session.refresh(lesson)
                print(f"  [CREATE] Lesson {lesson.id}: {title[:30]}...")
        
        session.commit()
        print(f"\n✅ FastAPI 강좌 업데이트 완료! (총 {len(lessons_data)}개 레슨)")
        print(f"   Course ID: {course.id}")
        print(f"   URL: /courses/{course.id}/")


# ============================================================
# 레슨 콘텐츠 함수들 (간소화)
# ============================================================

def get_lesson_1_content():
    return '''# 1 강. FastAPI 입문: 설치부터 Hello World 까지

## 🎯 학습 목표
- FastAPI 의 특징과 장점 이해
- FastAPI 설치와 첫 애플리케이션 작성
- Swagger UI 자동 문서화 활용

---

## 1. FastAPI 란?

**FastAPI**는 현대적인 파이썬 웹 프레임워크로, 다음과 같은 특징이 있습니다:

### 주요 장점

| 특징 | 설명 |
|------|------|
| 🚀 **매우 빠름** | Node.js, Go 와 대등한 성능 |
| 📝 **자동 문서화** | Swagger UI, ReDoc 자동 생성 |
| ✅ **타입 검증** | Python 타입 힌트 기반 자동 검증 |
| 🛠️ **IDE 지원** | VSCode, PyCharm 에서 자동완성 |

---

## 2. 설치하기

```bash
# FastAPI 와 서버 (uvicorn) 설치
pip install fastapi "uvicorn[standard]"
```

---

## 3. 첫 FastAPI 애플리케이션

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI World!"}
```

---

## 4. 서버 실행

```bash
uvicorn main:app --reload --port 8000
```

---

## 5. 자동 생성 API 문서

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc
- **OpenAPI JSON**: http://127.0.0.1:8000/openapi.json
'''


def get_lesson_2_content():
    return '''# 2 강. Path 와 Query 매개변수

## 🎯 학습 목표
- 경로 매개변수 (Path Parameter) 사용법
- 쿼리 스트링 (Query String) 활용법
- 타입 검증과 유효성 검사

---

## 1. 경로 매개변수 (Path Parameter)

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}
```

### 타입 변환의 마법

FastAPI 는 **타입 힌트를 보고 자동으로 변환**합니다!

```python
@app.get("/items/{item_id}")
def get_item(item_id: int):
    return {"item_id": item_id}
```

---

## 2. 쿼리 매개변수 (Query Parameter)

```python
@app.get("/items")
def read_items(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}
```

**URL 예시:**
- `/items` → skip=0, limit=10
- `/items?skip=20&limit=5` → skip=20, limit=5

---

## 3. Path() 와 Query() 고급 옵션

```python
from fastapi import FastAPI, Path, Query
from typing import Annotated

app = FastAPI()

@app.get("/articles/{article_id}")
def read_article(
    article_id: Annotated[int, Path(ge=1, le=10000)],
    q: Annotated[str | None, Query(max_length=50)] = None
):
    return {"id": article_id, "query": q}
```
'''


def get_lesson_3_content():
    return '''# 3 강. Pydantic 으로 Request Body 다루기

## 🎯 학습 목표
- Pydantic 모델 정의하기
- JSON Request Body 수신하기
- 자동 유효성 검사

---

## 1. Pydantic 모델 정의

```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float
    description: str | None = None
```

---

## 2. 사용법

```python
from fastapi import FastAPI

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float

@app.post("/items/")
def create_item(item: Item):
    return item
```

**요청 예시:**
```json
{
    "name": "Laptop",
    "price": 999.99
}
```

---

## 3. Field() 로 상세 검증

```python
from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    email: str = Field(..., pattern="^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$")
    password: str = Field(..., min_length=8)
    age: int = Field(..., ge=1, le=150)
```
'''


def get_lesson_4_content():
    return '''# 4 강. Response Model 과 HTTP 상태 코드

## 🎯 학습 목표
- Response Model 로 응답 데이터 제어
- HTTP 상태 코드 설정
- 민감 정보 필터링

---

## 1. Response Model

```python
class UserCreate(BaseModel):
    username: str
    password: str  # 입력용

class UserResponse(BaseModel):
    id: int
    username: str
    # password 없음! ✅

@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate):
    return user  # ✅ password 자동 필터링
```

---

## 2. HTTP 상태 코드

```python
from fastapi import FastAPI, status

app = FastAPI()

# 201 Created
@app.post("/items", status_code=status.HTTP_201_CREATED)
def create_item(name: str):
    return {"name": name}

# 204 No Content
@app.delete("/items/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(id: int):
    return None
```
'''


def get_lesson_5_content():
    return '''# 5 강. 예외 처리 (HTTPException)

## 🎯 학습 목표
- HTTPException 기본 사용법
- 커스텀 예외 클래스
- 전역 예외 처리기

---

## 1. HTTPException 기본

```python
from fastapi import HTTPException

@app.get("/items/{id}")
def get_item(id: int):
    if id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": items_db[id]}
```

---

## 2. 커스텀 예외 클래스

```python
class NotFoundException(HTTPException):
    def __init__(self, resource: str, id: int):
        super().__init__(
            status_code=404,
            detail=f"{resource} {id} not found"
        )

@app.get("/users/{id}")
def get_user(id: int):
    user = db.get(id)
    if not user:
        raise NotFoundException("User", id)
    return user
```
'''


def get_lesson_6_content():
    return '''# 6 강. 의존성 주입 (Dependency Injection)

## 🎯 학습 목표
- 의존성 주입 (DI) 개념 이해
- Depends() 활용법
- 의존성 체인과 캐싱

---

## 1. 의존성 주입이란?

```python
# ❌ 반복되는 인증 로직
@app.get("/users/me")
def read_user():
    token = get_token()
    user = verify_token(token)
    return user

# ✅ 의존성 주입
def get_current_user(token: str = Header(...)) -> User:
    return verify_token(token)

@app.get("/users/me")
def read_user(user: User = Depends(get_current_user)):
    return user
```

---

## 2. 의존성 체인

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user_by_id(user_id: int, db = Depends(get_db)):
    return db.query(User).filter(User.id == user_id).first()

def require_admin(user = Depends(get_user_by_id)):
    if user.role != "admin":
        raise HTTPException(403, "Not enough permissions")
    return user
```
'''


def get_lesson_7_content():
    return '''# 7 강. SQLAlchemy 비동기 데이터베이스

## 🎯 학습 목표
- AsyncEngine 과 AsyncSession 설정
- 비동기 CRUD 연산
- N+1 문제 해결

---

## 1. AsyncEngine 설정

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

DATABASE_URL = "postgresql+asyncpg://user:pass@localhost/dbname"

engine = create_async_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)
```

---

## 2. 비동기 CRUD

```python
@app.post("/users", response_model=User)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = User(**user.model_dump())
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user
```

---

## 3. N+1 문제 해결

```python
from sqlalchemy.orm import selectinload

# ✅ selectinload 로 2 번 쿼리
result = await db.execute(
    select(User).options(selectinload(User.posts))
)
users = result.scalars().unique().all()
```
'''


def get_lesson_8_content():
    return '''# 8 강. JWT 인증과 보안

## 🎯 학습 목표
- JWT 토큰 구조 이해
- Access/Refresh Token 구현
- 비밀번호 해싱

---

## 1. 비밀번호 해싱

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"])

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)
```

---

## 2. JWT 토큰 생성

```python
from jose import jwt

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
```

---

## 3. 인증 의존성

```python
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user_id = payload.get("sub")
    return await db.get(User, int(user_id))
```
'''


def get_lesson_9_content():
    return '''# 9 강. 실시간 통신 (WebSockets & SSE)

## 🎯 학습 목표
- WebSocket 기본 사용법
- Connection Manager 구현
- Server-Sent Events (SSE)

---

## 1. WebSocket 기본

```python
from fastapi import WebSocket

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"You said: {data}")
```

---

## 2. Connection Manager

```python
class ConnectionManager:
    def __init__(self):
        self.connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)
    
    async def broadcast(self, message: str):
        for conn in self.connections:
            await conn.send_text(message)
```

---

## 3. SSE (Server-Sent Events)

```python
from fastapi.responses import StreamingResponse

async def event_generator():
    while True:
        yield f"data: {count}\\n\\n"
        await asyncio.sleep(1)

@app.get("/events")
async def stream_events():
    return StreamingResponse(event_generator(), media_type="text/event-stream")
```
'''


def get_lesson_10_content():
    return '''# 10 강. 테스트 작성법 (Pytest)

## 🎯 학습 목표
- Pytest 기본 사용법
- FastAPI TestClient
- 의존성 오버라이드

---

## 1. 첫 테스트

```python
# tests/test_basic.py
def test_addition():
    assert 1 + 1 == 2
```

실행:
```bash
pytest
```

---

## 2. FastAPI 테스트

```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
```

---

## 3. 의존성 오버라이드

```python
@app.get("/users/me")
def read_me(current_user = Depends(get_current_user)):
    return current_user

# 테스트에서
async def override_get_current_user():
    return {"id": 1, "email": "test@example.com"}

app.dependency_overrides[get_current_user] = override_get_current_user
```
'''


if __name__ == "__main__":
    update_fastapi_course()
