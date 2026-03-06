# -*- coding: utf-8 -*-
"""
FastAPI 실무 마스터 강좌 - 대대적 업데이트 (수정 버전)
- 더 쉬운 설명과 풍부한 예제
- 실전 디버깅 팁 추가
"""
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from sqlmodel import Session, select
from core.database import engine
from models import Category, Course, Lesson


def seed_fastapi_course():
    """FastAPI 강좌 생성 (10 개 레슨)"""
    with Session(engine) as session:
        # 카테고리 확인
        statement = select(Category).where(Category.name == "프로그래밍")
        category = session.exec(statement).first()

        if not category:
            category = Category(name="프로그래밍", order=10)
            session.add(category)
            session.commit()
            session.refresh(category)

        # 기존 FastAPI 강좌 삭제
        statement = select(Course).where(Course.title.like("%FastAPI%"))
        existing_course = session.exec(statement).first()
        if existing_course:
            session.delete(existing_course)
            session.commit()

        # 강좌 생성
        course = Course(
            title="FastAPI 실무 마스터",
            description="FastAPI 기초부터 비동기 DB, JWT 보안, 실시간 통신, 테스트, Docker 배포까지 현업 실무 기술을 배웁니다.",
            thumbnail_url="/static/uploads/fastapi_thumbnail.png",
            category_id=category.id
        )
        session.add(course)
        session.commit()
        session.refresh(course)

        # 레슨 데이터 (10 개)
        lessons = [
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

        for order, title, content in lessons:
            lesson = Lesson(title=title, content=content, order=order, course_id=course.id)
            session.add(lesson)

        session.commit()
        print(f"✅ FastAPI 강좌 생성 완료: 총 {len(lessons)}개 레슨")
        return course.id


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

### 다른 프레임워크와 비교

```
Flask/Django: 동기식, 수동 검증, 별도 문서화 필요
FastAPI:    비동기식, 자동 검증, 자동 문서화 ✅
```

---

## 2. 설치하기

```bash
# FastAPI 와 서버 (uvicorn) 설치
pip install fastapi "uvicorn[standard]"

# 또는 uv 사용 (더 빠름)
uv add fastapi uvicorn
```

---

## 3. 첫 FastAPI 애플리케이션

`main.py` 파일 생성:

```python
from fastapi import FastAPI

app = FastAPI(
    title="내 첫 API",
    description="Hello World 예제",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI World!"}

@app.get("/add/{a}/{b}")
def add_numbers(a: int, b: int):
    return {"result": a + b}
```

---

## 4. 서버 실행

```bash
# 개발 모드 (--reload: 코드 변경 시 자동 재시작)
uvicorn main:app --reload --port 8000
```

**명령어 해석:**
- `main`: main.py 파일명
- `app`: FastAPI() 인스턴스 변수명
- `--reload`: 개발용 자동 재시작
- `--port 8000`: 포트 번호

---

## 5. 자동 생성 API 문서

서버 실행 후 다음 URL 로 접속:

### Swagger UI (대화형 테스트)
```
http://127.0.0.1:8000/docs
```

**기능:**
- API 테스트 (Try it out)
- 요청/응답 스키마 자동 표시
- 인증 처리 UI 지원

### ReDoc (깔끔한 문서)
```
http://127.0.0.1:8000/redoc
```

### OpenAPI JSON (기계용)
```
http://127.0.0.1:8000/openapi.json
```

---

## 6. 실습: 나만의 API 만들기

다음 엔드포인트들을 직접 만들어보세요:

```python
@app.get("/profile")
def get_profile():
    return {
        "name": "홍길동",
        "age": 25,
        "job": "개발자"
    }

@app.get("/gugudan/{dan}")
def get_gugudan(dan: int):
    result = [f"{dan} x {i} = {dan * i}" for i in range(1, 10)]
    return {"dan": dan, "result": result}

@app.get("/lotto")
def generate_lotto():
    import random
    numbers = random.sample(range(1, 46), 6)
    numbers.sort()
    return {"numbers": numbers}
```

---

## 📝 연습 문제

1. `/hello/{name}` 엔드포인트 만들기
2. `/multiply/{a}/{b}` 엔드포인트 만들기
3. Swagger UI 에서 테스트하기

---

## 🔍 Troubleshooting

**Q1. uvicorn 명령어를 찾을 수 없어요.**
```bash
# 가상환경 활성화 확인
# Windows
.venv\\Scripts\\activate

# macOS/Linux
source .venv/bin/activate
```

**Q2. 포트가 이미 사용 중이에요.**
```bash
# 다른 포트 사용
uvicorn main:app --reload --port 8001
```
'''


def get_lesson_2_content():
    return '''# 2 강. Path 와 Query 매개변수

## 🎯 학습 목표
- 경로 매개변수 (Path Parameter) 사용법
- 쿼리 스트링 (Query String) 활용법
- 타입 검증과 유효성 검사

---

## 1. 경로 매개변수 (Path Parameter)

### 기본 사용법

```python
from fastapi import FastAPI

app = FastAPI()

# /users/123 → user_id = 123
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}

# /posts/456/comments/789
@app.get("/posts/{post_id}/comments/{comment_id}")
def get_comment(post_id: int, comment_id: int):
    return {"post_id": post_id, "comment_id": comment_id}
```

### 타입 변환의 마법

FastAPI 는 **타입 힌트를 보고 자동으로 변환**합니다!

```python
@app.get("/items/{item_id}")
def get_item(item_id: int):
    return {"item_id": item_id, "type": type(item_id)}
```

**실제 동작:**
```
GET /items/42
→ {"item_id": 42, "type": "<class 'int'>"}

GET /items/hello
→ HTTP 422 Error: "value is not a valid integer"
```

---

## 2. 쿼리 매개변수 (Query Parameter)

### 기본 사용법

```python
@app.get("/items")
def read_items(skip: int = 0, limit: int = 10):
    """
    skip: 몇 개부터 시작할지 (기본값: 0)
    limit: 몇 개까지 가져올지 (기본값: 10)
    """
    return {"skip": skip, "limit": limit}
```

**URL 예시:**
- `/items` → skip=0, limit=10
- `/items?skip=20` → skip=20, limit=10
- `/items?skip=20&limit=5` → skip=20, limit=5

### 선택적 매개변수

```python
from typing import Optional

@app.get("/search")
def search(q: Optional[str] = None):
    if q:
        return {"message": f"'{q}' 검색 결과"}
    return {"message": "검색어를 입력하세요"}
```

---

## 3. Path() 와 Query() 고급 옵션

### Path() 옵션

```python
from fastapi import FastAPI, Path
from typing import Annotated

app = FastAPI()

@app.get("/articles/{article_id}")
def read_article(
    article_id: Annotated[
        int,
        Path(
            title="기사 ID",
            ge=1,      # 1 이상
            le=10000,  # 10000 이하
            example=42
        )
    ]
):
    return {"article_id": article_id}
```

**주요 옵션:**
| 옵션 | 설명 | 예시 |
|------|------|------|
| `gt` | 초과 | `gt=0` → 1 이상 |
| `ge` | 이상 | `ge=1` → 1 이상 |
| `lt` | 미만 | `lt=100` → 99 이하 |
| `le` | 이하 | `le=100` → 100 이하 |
| `min_length` | 최소 길이 | `min_length=3` |
| `max_length` | 최대 길이 | `max_length=50` |

### Query() 옵션

```python
from fastapi import FastAPI, Query
from typing import Annotated, Optional

app = FastAPI()

@app.get("/products")
def read_products(
    category: Annotated[
        str,
        Query(
            min_length=2,
            max_length=20,
            pattern="^[a-zA-Z0-9_-]+$"
        )
    ],
    sort: Annotated[Optional[str], Query(alias="order-by")] = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 10
):
    return {"category": category, "sort": sort, "limit": limit}
```

---

## 4. 실전 예제: 블로그 API

```python
from enum import Enum

class SortOption(str, Enum):
    NEWEST = "newest"
    OLDEST = "oldest"
    POPULAR = "popular"

@app.get("/posts")
def list_posts(
    page: Annotated[int, Query(ge=1)] = 1,
    limit: Annotated[int, Query(ge=1, le=50)] = 10,
    category: Optional[str] = None,
    sort: Optional[SortOption] = SortOption.NEWEST
):
    return {
        "page": page,
        "limit": limit,
        "category": category,
        "sort": sort
    }
```

---

## 📝 연습 문제

1. `/users/{user_id}/posts/{post_id}` 엔드포인트 만들기
2. `/products` 에서 `min_price`, `max_price` 쿼리 매개변수 받기
3. `/files/{file_path:path}` 로 전체 파일 경로 받기

---

## 🔍 Troubleshooting

**Q1. 경로 매개변수와 함수 매개변수 이름이 달라도 되나요?**
```python
# ❌ 에러! 이름이 같아야 함
@app.get("/users/{user_id}")
def get_user(uid: int):  # user_id ≠ uid

# ✅ 올바름
@app.get("/users/{user_id}")
def get_user(user_id: int):  # 이름 일치!
```

**Q2. 쿼리 매개변수를 필수로 만들고 싶어요.**
```python
# 기본값을 주지 않으면 필수
@app.get("/search")
def search(q: str):  # ✅ 필수 입력
    return {"query": q}
```
'''


def get_lesson_3_content():
    return '''# 3 강. Pydantic 으로 Request Body 다루기

## 🎯 학습 목표
- Pydantic 모델 정의하기
- JSON Request Body 수신하기
- 자동 유효성 검사
- 중첩 모델 처리

---

## 1. Pydantic 이란?

**Pydantic**은 Python 데이터 검증 라이브러리로, FastAPI 의 핵심 엔진입니다.

### 기존 방식 vs Pydantic

```python
# ❌ 기존: 수동 검증 (지루하고 에러 발생 쉬움)
def create_user(data: dict):
    if "name" not in data:
        raise ValueError("이름 필요")
    if not isinstance(data["name"], str):
        raise ValueError("이름은 문자열")

# ✅ Pydantic: 자동 검증 (깔끔하고 명확)
from pydantic import BaseModel

class User(BaseModel):
    name: str  # 자동으로 str 검증!
    age: int   # 자동으로 int 검증!
```

---

## 2. Pydantic 모델 정의

### 기본 모델

```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str                    # 필수 문자열
    price: float                 # 필수 실수
    description: str | None = None  # 선택 문자열
    tax: float = 0.0             # 선택 실수 (기본값 0)
```

### 사용법

```python
from fastapi import FastAPI

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float

@app.post("/items/")
def create_item(item: Item):
    # item 은 Item 타입 인스턴스!
    print(item.name)
    print(item.model_dump())  # dict 로 변환
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
    # 아이디: 3-20 자, 영문/숫자/언더바
    username: str = Field(
        ...,
        min_length=3,
        max_length=20,
        pattern="^[a-zA-Z0-9_]+$",
        example="john_doe"
    )
    
    # 이메일 형식 검증
    email: str = Field(
        ...,
        pattern="^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$",
        example="john@example.com"
    )
    
    # 비밀번호: 8 자 이상
    password: str = Field(
        ...,
        min_length=8,
        example="SecurePass123"
    )
    
    # 나이: 1-150 사이
    age: int = Field(
        ...,
        ge=1,
        le=150,
        example=25
    )
```

---

## 4. 중첩 모델

### 기본 중첩

```python
class Address(BaseModel):
    street: str
    city: str
    zipcode: str

class User(BaseModel):
    name: str
    email: str
    address: Address  # 중첩 모델!
```

**요청 예시:**
```json
{
    "name": "홍길동",
    "email": "hong@example.com",
    "address": {
        "street": "강남대로 123",
        "city": "서울",
        "zipcode": "06000"
    }
}
```

### 리스트 중첩

```python
class Product(BaseModel):
    id: int
    name: str
    price: float

class Order(BaseModel):
    order_id: int
    products: list[Product]  # Product 리스트
```

---

## 5. 실전 예제: 블로그 API

```python
from pydantic import EmailStr
from typing import Optional, List
from datetime import datetime

class PostCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1, max_length=50000)
    author_email: EmailStr  # 이메일 형식 자동 검증!
    tags: Optional[List[str]] = None

class PostResponse(PostCreate):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

@app.post("/posts", response_model=PostResponse)
def create_post(post: PostCreate):
    return post
```

---

## 📝 연습 문제

1. `UserCreate` 모델로 회원가입 받기
2. `Product` 와 `Order` 중첩 모델 만들기
3. 비밀번호 검증 규칙 추가 (8 자 이상, 대소문자/숫자 포함)

---

## 🔍 Troubleshooting

**Q1. model_dump() 와 dict() 차이?**
```python
# Pydantic v2 (최신)
item.model_dump()  # ✅ 권장

# Pydantic v1 (구버전)
item.dict()
```

**Q2. 선택 필드 만들기**
```python
from typing import Optional

class User(BaseModel):
    name: str              # ✅ 필수
    email: Optional[str]   # ✅ 선택 (None 가능)
    age: int = 0          # ✅ 선택 (기본값 0)
```
'''


def get_lesson_4_content():
    return '''# 4 강. Response Model 과 HTTP 상태 코드

## 🎯 학습 목표
- Response Model 로 응답 데이터 제어
- HTTP 상태 코드 설정
- 민감 정보 필터링

---

## 1. Response Model 이 왜 필요한가요?

### 보안 문제: 비밀번호 노출

```python
# ❌ 문제: 비밀번호가 그대로 응답됨
class User(BaseModel):
    id: int
    username: str
    password: str  # ❌ 이걸 보내면 안 됨!

@app.post("/users")
def create_user(user: User):
    return user  # ❌ password 유출!
```

### 해결: Response Model

```python
# ✅ 해결: 입력용과 출력용 분리
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

## 2. Response Model 사용법

### 기본 사용

```python
class ItemCreate(BaseModel):
    name: str
    price: float
    secret: str  # 내부용

class ItemResponse(BaseModel):
    id: int
    name: str
    price: float
    # secret 제외! ✅

@app.post("/items", response_model=ItemResponse)
def create_item(item: ItemCreate):
    return {
        "id": 1,
        "name": item.name,
        "price": item.price,
        "secret": "SECRET"  # ✅ 응답에서 자동 제거
    }
```

---

## 3. HTTP 상태 코드

### 주요 상태 코드

| 코드 | 의미 | 사용 사례 |
|------|------|----------|
| 200 | OK | 일반적인 GET, PUT |
| 201 | Created | POST 성공 |
| 204 | No Content | DELETE 성공 |
| 400 | Bad Request | 잘못된 요청 |
| 401 | Unauthorized | 인증 필요 |
| 403 | Forbidden | 권한 없음 |
| 404 | Not Found | 리소스 없음 |
| 422 | Unprocessable Entity | 검증 실패 |

### 사용법

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

---

## 4. 실전 예제: 사용자 관리 API

```python
from fastapi import HTTPException

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str

fake_users = []

@app.post("/users", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate):
    # 중복 확인
    for u in fake_users:
        if u["username"] == user.username:
            raise HTTPException(400, "Username exists")
    
    new_user = {
        "id": len(fake_users) + 1,
        **user.model_dump()
    }
    fake_users.append(new_user)
    return new_user

@app.get("/users/{id}", response_model=UserResponse)
def get_user(id: int):
    for user in fake_users:
        if user["id"] == id:
            return user
    raise HTTPException(404, "User not found")

@app.delete("/users/{id}", status_code=204)
def delete_user(id: int):
    for i, user in enumerate(fake_users):
        if user["id"] == id:
            fake_users.pop(i)
            return None
    raise HTTPException(404, "User not found")
```

---

## 📝 연습 문제

1. `ProductCreate` 와 `ProductResponse` 모델 만들기
2. POST 엔드포인트에서 201 상태 코드 반환
3. DELETE 엔드포인트에서 204 상태 코드 반환

---

## 🔍 Troubleshooting

**Q1. Response Model 이 필터링되지 않아요.**
```python
# ✅ 올바른 방법
@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreate):
    return db_user  # FastAPI 가 자동 필터링
```

**Q2. 중첩 모델에서 Response Model 적용**
```python
class AddressResponse(BaseModel):
    city: str  # street 제외

class UserResponse(BaseModel):
    name: str
    address: AddressResponse  # 중첩 모델도 자동 필터링!
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

### 왜 HTTPException 인가요?

```python
# ❌ 일반 Exception: 500 에러
@app.get("/users/{id}")
def get_user(id: int):
    user = db.get(id)
    if not user:
        raise Exception("Not found")  # ❌ 500 에러!

# ✅ HTTPException: 올바른 상태 코드
from fastapi import HTTPException

@app.get("/users/{id}")
def get_user(id: int):
    user = db.get(id)
    if not user:
        raise HTTPException(404, "User not found")  # ✅ 404!
```

### 기본 사용법

```python
from fastapi import HTTPException

items_db = {1: "Laptop", 2: "Mouse"}

@app.get("/items/{id}")
def get_item(id: int):
    if id not in items_db:
        raise HTTPException(
            status_code=404,
            detail=f"Item {id} not found"
        )
    return {"item": items_db[id]}
```

---

## 2. 커스텀 예외 클래스

```python
from fastapi import HTTPException

class NotFoundException(HTTPException):
    def __init__(self, resource: str, id: int):
        super().__init__(
            status_code=404,
            detail=f"{resource} {id} not found"
        )

class UnauthorizedException(HTTPException):
    def __init__(self, message: str = "Not authenticated"):
        super().__init__(
            status_code=401,
            detail=message,
            headers={"WWW-Authenticate": "Bearer"}
        )

# 사용 예시
@app.get("/users/{id}")
def get_user(id: int):
    user = db.get(id)
    if not user:
        raise NotFoundException("User", id)
    return user
```

---

## 3. 전역 예외 처리기

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from datetime import datetime

app = FastAPI()

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "timestamp": datetime.now().isoformat(),
            "status": exc.status_code,
            "error": exc.detail,
            "path": str(request.url.path)
        }
    )

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    # 로깅
    print(f"Error: {exc}")
    
    # 안전한 응답
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "An error occurred"
        }
    )
```

---

## 4. 실전 예제

```python
class AppException(HTTPException):
    def __init__(self, status_code: int, error_code: str, message: str):
        super().__init__(
            status_code=status_code,
            detail={"error_code": error_code, "message": message}
        )

class UserNotFoundException(AppException):
    def __init__(self, user_id: int):
        super().__init__(
            status_code=404,
            error_code="USER_NOT_FOUND",
            message=f"User {user_id} not found"
        )

@app.get("/users/{id}")
def get_user(id: int):
    user = db.get(id)
    if not user:
        raise UserNotFoundException(id)
    return user
```

**응답 예시:**
```json
{
    "detail": {
        "error_code": "USER_NOT_FOUND",
        "message": "User 123 not found"
    }
}
```

---

## 📝 연습 문제

1. `ProductNotFoundException` 예외 클래스 만들기
2. 전역 예외 처리기에 타임스탬프 추가
3. 로그인 실패 시 401 에러 반환

---

## 🔍 Troubleshooting

**Q1. 예외 raise 했는데 응답이 안 나가요.**
```python
# ✅ 올바른 방법
@app.get("/items/{id}")
def get_item(id: int):
    if id not in items:
        raise HTTPException(404, "Not found")
    return items[id]  # ✅ 여기 도달
```

**Q2. 에러 상세 정보를 숨기고 싶어요.**
```python
# 프로덕션에서는 안전한 메시지
@app.exception_handler(Exception)
async def handler(request, exc):
    # ❌ 위험
    return {"error": str(exc)}
    
    # ✅ 안전
    return {"error": "Internal error"}
```
'''


def get_lesson_6_content():
    return '''# 6 강. 의존성 주입 (Dependency Injection)

## 🎯 학습 목표
- 의존성 주입 (DI) 개념 이해
- Depends() 활용법
- 의존성 체인과 캐싱

---

## 1. 의존성 주입이 뭔가요?

### 문제: 반복되는 인증 로직

```python
# ❌ 매 엔드포인트마다 반복
@app.get("/users/me")
def read_user():
    token = get_token()
    user = verify_token(token)
    return user

@app.get("/users/me/items")
def read_items():
    token = get_token()  # 또 반복!
    user = verify_token(token)
    return items
```

### 해결: 의존성 주입

```python
# ✅ 한 번 작성, 재사용
from fastapi import Depends

def get_current_user(token: str = Header(...)) -> User:
    return verify_token(token)

@app.get("/users/me")
def read_user(user: User = Depends(get_current_user)):
    return user  # ✅ 인증된 user 자동 주입!

@app.get("/users/me/items")
def read_items(user: User = Depends(get_current_user)):
    return get_items(user.id)
```

---

## 2. Depends() 기본

### 함수 의존성

```python
def common_params(q: str | None = None, skip: int = 0):
    return {"q": q, "skip": skip}

@app.get("/items")
def read_items(params: dict = Depends(common_params)):
    return {"params": params}

@app.get("/users")
def read_users(params: dict = Depends(common_params)):
    return {"params": params}
```

### 클래스 의존성

```python
class Pagination:
    def __init__(self, page: int = 1, size: int = 20):
        self.page = page
        self.size = size

@app.get("/items")
def read_items(pagination: Pagination = Depends()):
    return {"page": pagination.page}
```

---

## 3. 의존성 체인

```python
# 1 단계: DB 세션
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 2 단계: 사용자 조회
def get_user_by_id(user_id: int, db = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "Not found")
    return user

# 3 단계: 권한 확인
def require_admin(user = Depends(get_user_by_id)):
    if user.role != "admin":
        raise HTTPException(403, "Not enough permissions")
    return user

# 사용
@app.delete("/users/{id}")
def delete_user(admin = Depends(require_admin)):
    # 이미 인증 + 권한 확인 완료
    delete_user_from_db(admin.id)
```

---

## 4. 의존성 캐싱

```python
call_count = 0

def expensive_operation() -> int:
    global call_count
    call_count += 1
    return call_count

@app.get("/test")
def test(
    dep1: int = Depends(expensive_operation),
    dep2: int = Depends(expensive_operation),
    dep3: int = Depends(expensive_operation)
):
    return {"dep1": dep1, "dep2": dep2, "dep3": dep3}

# 결과: {"dep1": 1, "dep2": 1, "dep3": 1}
# expensive_operation() 은 단 1 번 실행!
```

### 캐싱 비활성화

```python
@app.get("/time")
def get_time(
    time1 = Depends(get_current_time),
    time2 = Depends(get_current_time, use_cache=False)  # 새 값!
):
    return {"time1": time1, "time2": time2}
```

---

## 5. 실무 DI 패턴

### DB 세션 관리

```python
SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(**user.model_dump())
    db.add(db_user)
    db.commit()
    return db_user
```

---

## 📝 연습 문제

1. `get_current_user` 의존성 만들기
2. `require_admin` 권한 검사기 만들기
3. DB 세션 의존성 주입하기

---

## 🔍 Troubleshooting

**Q1. yield 와 return 차이?**
```python
# return: 정리 안 함 (❌)
def get_db_return():
    db = SessionLocal()
    return db  # ❌ 세션 안 닫힘!

# yield: 정리 함 (✅)
def get_db_yield():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  # ✅ 반드시 닫기!
```
'''


def get_lesson_7_content():
    return '''# 7 강. SQLAlchemy 비동기 데이터베이스

## 🎯 학습 목표
- AsyncEngine 과 AsyncSession 설정
- 비동기 CRUD 연산
- N+1 문제 해결

---

## 1. 왜 비동기 데이터베이스?

### 동기 vs 비동기

```python
# ❌ 동기: 블로킹 발생
@app.get("/users")
def get_users():
    users = db.query(User).all()  # ← 여기서 블로킹!
    return users

# ✅ 비동기: 블로킹 없음
@app.get("/users")
async def get_users():
    users = await db.execute(select(User))
    return users
```

---

## 2. AsyncEngine 설정

### 설치

```bash
pip install asyncpg  # PostgreSQL
pip install aiomysql  # MySQL
pip install sqlalchemy>=2.0
```

### 설정

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+asyncpg://user:pass@localhost/dbname"

engine = create_async_engine(
    DATABASE_URL,
    pool_size=20,
    pool_pre_ping=True,  # 연결 유효성 검사
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,  # 중요!
)
```

### 의존성 함수

```python
from typing import AsyncGenerator

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
```

---

## 3. 비동기 CRUD

### Create

```python
@app.post("/users", response_model=User)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = User(**user.model_dump())
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user
```

### Read

```python
@app.get("/users/{id}", response_model=User)
async def get_user(id: int, db: AsyncSession = Depends(get_db)):
    user = await db.get(User, id)
    if not user:
        raise HTTPException(404, "Not found")
    return user

@app.get("/users", response_model=list[User])
async def get_users(skip: int = 0, limit: int = 100, db = Depends(get_db)):
    result = await db.execute(select(User).offset(skip).limit(limit))
    return result.scalars().all()
```

### Update

```python
@app.patch("/users/{id}")
async def update_user(id: int, update_data: UserUpdate, db = Depends(get_db)):
    user = await db.get(User, id)
    if not user:
        raise HTTPException(404, "Not found")
    
    for key, value in update_data.model_dump(exclude_unset=True).items():
        setattr(user, key, value)
    
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
```

### Delete

```python
@app.delete("/users/{id}", status_code=204)
async def delete_user(id: int, db = Depends(get_db)):
    user = await db.get(User, id)
    if not user:
        raise HTTPException(404, "Not found")
    
    await db.delete(user)
    await db.commit()
```

---

## 4. N+1 문제 해결

### 문제

```python
# ❌ N+1: 1 + N 번 쿼리
posts = await db.execute(select(Post))
posts = posts.scalars().all()

for post in posts:
    author = await db.get(User, post.author_id)  # 매번 쿼리!
```

### 해결: joinedload (1:1)

```python
from sqlalchemy.orm import joinedload

# ✅ 1 번 쿼리 (JOIN)
result = await db.execute(
    select(Post).options(joinedload(Post.author))
)
posts = result.scalars().unique().all()
```

### 해결: selectinload (1:N)

```python
from sqlalchemy.orm import selectinload

# ✅ 2 번 쿼리
result = await db.execute(
    select(User).options(selectinload(User.posts))
)
users = result.scalars().unique().all()
```

---

## 📝 연습 문제

1. `Product` 모델 비동기 CRUD 만들기
2. `Order` 와 `OrderItem` 관계 selectinload 로 조회
3. Alembic 마이그레이션 설정

---

## 🔍 Troubleshooting

**Q1. MissingGreenletException 에러**
```python
# ❌ 동기 방식
user = db.query(User).first()  # ❌ 에러!

# ✅ 비동기 방식
result = await db.execute(select(User))
user = result.scalar_one()  # ✅
```

**Q2. commit 후 속성 접근 에러**
```python
# ✅ expire_on_commit=False 필수
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,  # ✅
)
```
'''


def get_lesson_8_content():
    return '''# 8 강. JWT 인증과 보안

## 🎯 학습 목표
- JWT 토큰 구조 이해
- Access/Refresh Token 구현
- 비밀번호 해싱
- 토큰 블랙리스트

---

## 1. JWT 란?

### JWT 구조

```
JWT = 헤더 + 페이로드 + 서명

헤더: {"alg": "HS256", "typ": "JWT"}
페이로드: {"sub": "123", "exp": 1234567890}
서명: HMACSHA256(헤더.페이로드, SECRET_KEY)
```

### 인증 흐름

```
1. 로그인 (ID/PW) → 2. JWT 생성 → 3. 클라이언트 저장
                                            ↓
6. 리소스 반환 ← 5. JWT 검증 ← 4. 요청 시 JWT 포함
```

---

## 2. 기본 구현

### 설치

```bash
pip install python-jose[cryptography]
pip install passlib[bcrypt]
```

### 설정

```python
from datetime import timedelta

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
```

### 비밀번호 해싱

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"])

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)
```

### 토큰 생성

```python
from jose import jwt
from datetime import datetime, timedelta

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
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(401, "Invalid token")
    except JWTError:
        raise HTTPException(401, "Invalid token")
    
    user = await db.get(User, int(user_id))
    if not user:
        raise HTTPException(401, "User not found")
    return user
```

---

## 4. 로그인 엔드포인트

```python
from fastapi.security import OAuth2PasswordRequestForm

@app.post("/auth/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # 사용자 조회
    user = await db.execute(select(User).where(User.email == form_data.username))
    user = user.scalar_one_or_none()
    
    # 비밀번호 검증
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(401, "Incorrect credentials")
    
    # 토큰 생성
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    return {"access_token": access_token, "token_type": "bearer"}
```

---

## 5. 권한 기반 접근 (RBAC)

```python
class RoleChecker:
    def __init__(self, allowed_roles: list[str]):
        self.allowed_roles = allowed_roles
    
    def __call__(self, user: User = Depends(get_current_user)) -> User:
        if user.role not in self.allowed_roles:
            raise HTTPException(403, "Not enough permissions")
        return user

# 사용
require_admin = RoleChecker(["admin"])

@app.get("/admin/dashboard")
def admin_dashboard(admin: User = Depends(require_admin)):
    return {"message": f"Welcome, {admin.name}!"}
```

---

## 📝 연습 문제

1. 회원가입 엔드포인트 (비밀번호 해싱)
2. 로그인 엔드포인트 (JWT 반환)
3. `require_admin` 의존성 만들기

---

## 🔍 Troubleshooting

**Q1. 토큰 만료 에러**
```python
# Access Token 만료 시간 늘리기
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# 또는 Refresh Token 으로 갱신
POST /auth/refresh {"refresh_token": "..."}
```

**Q2. 쿠키에 토큰 저장**
```python
response.set_cookie(
    key="refresh_token",
    value=refresh_token,
    httponly=True,  # JS 접근 불가
    secure=True,    # HTTPS 만
    samesite="lax"
)
```
'''


def get_lesson_9_content():
    return '''# 9 강. 실시간 통신 (WebSockets & SSE)

## 🎯 학습 목표
- WebSocket 기본 사용법
- Connection Manager 구현
- Server-Sent Events (SSE)

---

## 1. WebSocket 이란?

### HTTP vs WebSocket

| 구분 | HTTP | WebSocket |
|------|------|-----------|
| 방향 | 단방향 | 양방향 |
| 연결 | 일회성 | 지속적 |
| 사용 | 일반 API | 채팅, 실시간 |

---

## 2. WebSocket 기본

```python
from fastapi import WebSocket

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"You said: {data}")
```

### 클라이언트

```html
<script>
  const ws = new WebSocket("ws://localhost:8000/ws");
  
  ws.onmessage = (event) => {
    console.log(event.data);
  };
  
  function send() {
    ws.send("Hello");
  }
</script>
```

---

## 3. Connection Manager

```python
from typing import List

class ConnectionManager:
    def __init__(self):
        self.connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.connections.remove(websocket)
    
    async def broadcast(self, message: str):
        for conn in self.connections:
            await conn.send_text(message)

manager = ConnectionManager()

@app.websocket("/chat/{client_id}")
async def chat(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    await manager.broadcast(f"Client #{client_id} joined")
    
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Client #{client_id}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left")
```

---

## 4. Server-Sent Events (SSE)

### SSE 구현

```python
from fastapi.responses import StreamingResponse
import asyncio

async def event_generator():
    count = 0
    while True:
        yield f"data: {count}\\n\\n"
        await asyncio.sleep(1)
        count += 1

@app.get("/events")
async def stream_events():
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )
```

### 클라이언트

```html
<script>
  const es = new EventSource("/events");
  
  es.onmessage = (e) => {
    console.log("Count:", e.data);
  };
</script>
```

---

## 5. WebSocket vs SSE

```
양방향 필요 (채팅, 게임) → WebSocket
서버→클라이언트 단방향 (알림, 시세) → SSE
```

---

## 📝 연습 문제

1. 채팅 WebSocket 엔드포인트 만들기
2. SSE 로 실시간 알림 전송
3. 방 (Room) 개념 추가하기

---

## 🔍 Troubleshooting

**Q1. WebSocket 연결이 끊겨요.**
```python
# 하트비트 추가
while True:
    data = await websocket.receive_text()
```

**Q2. 브로드캐스트가 안 돼요.**
```python
# Connection Manager 사용
class Manager:
    async def broadcast(self, message):
        for conn in self.connections:
            await conn.send_text(message)
```
'''


def get_lesson_10_content():
    return '''# 10 강. 테스트 작성법 (Pytest)

## 🎯 학습 목표
- Pytest 기본 사용법
- FastAPI TestClient
- 의존성 오버라이드
- 데이터베이스 테스트

---

## 1. 테스트 설정

### 설치

```bash
pip install pytest pytest-asyncio httpx
```

### pytest.ini

```ini
[pytest]
testpaths = tests
python_files = test_*.py
asyncio_mode = auto
```

---

## 2. 첫 테스트

```python
# tests/test_basic.py
def test_addition():
    assert 1 + 1 == 2

def test_string():
    assert "hello".upper() == "HELLO"
```

### 실행

```bash
# 모든 테스트
pytest

# 상세 출력
pytest -v

# 특정 파일
pytest tests/test_users.py
```

---

## 3. FastAPI 테스트

```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello"}

def test_create_item():
    response = client.post(
        "/items",
        json={"name": "Item", "price": 100}
    )
    assert response.status_code == 201
```

---

## 4. 의존성 오버라이드

```python
# tests/conftest.py
import pytest
from main import app, get_current_user

@pytest.fixture
def client():
    # 가짜 사용자
    fake_user = {"id": 1, "email": "test@example.com"}
    
    # 인증 오버라이드
    async def override():
        return fake_user
    
    app.dependency_overrides[get_current_user] = override
    
    with TestClient(app) as c:
        yield c
    
    app.dependency_overrides.clear()

# tests/test_users.py
def test_read_me(client):
    response = client.get("/users/me")
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"
```

---

## 5. 데이터베이스 테스트

```python
# tests/conftest.py
@pytest.fixture
async def db_session():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    
    session = AsyncSession(engine)
    yield session
    await session.close()

# tests/test_users.py
@pytest.mark.asyncio
async def test_create_user(client, db_session):
    response = client.post("/users", json={
        "email": "test@example.com",
        "password": "pass123"
    })
    assert response.status_code == 201
```

---

## 6. 통합 테스트

```python
def test_full_flow(client):
    # 1. 회원가입
    r = client.post("/auth/register", json={...})
    assert r.status_code == 201
    
    # 2. 로그인
    r = client.post("/auth/login", data={...})
    assert r.status_code == 200
    token = r.json()["access_token"]
    
    # 3. 인증된 요청
    r = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert r.status_code == 200
```

---

## 📝 연습 문제

1. CRUD 엔드포인트 테스트 작성
2. 인증 엔드포인트 테스트
3. 의존성 오버라이드로 모킹

---

## 🔍 Troubleshooting

**Q1. 비동기 테스트가 안 돼요.**
```python
# pytest.ini 에 설정
[pytest]
asyncio_mode = auto
```

**Q2. 의존성 오버라이드가 적용 안 돼요.**
```python
# 테스트 후 반드시 clear!
app.dependency_overrides[get_db] = override

try:
    # 테스트
finally:
    app.dependency_overrides.clear()  # ✅ 필수!
```
'''


if __name__ == "__main__":
    course_id = seed_fastapi_course()
    
    print("\n" + "="*60)
    print("✅ FastAPI 완전 정복 강좌 업데이트 완료!")
    print("="*60)
    print("\n📚 전체 커리큘럼 (총 10 강):")
    print("-" * 60)
    print("[초급] 1-5 강: FastAPI 기초")
    print("  1 강. FastAPI 입문: 설치부터 Hello World 까지")
    print("  2 강. Path 와 Query 매개변수")
    print("  3 강. Pydantic 으로 Request Body 다루기")
    print("  4 강. Response Model 과 HTTP 상태 코드")
    print("  5 강. 예외 처리 (HTTPException)")
    print("-" * 60)
    print("[중급] 6-8 강: 실전 웹 애플리케이션")
    print("  6 강. 의존성 주입 (DI)")
    print("  7 강. SQLAlchemy 비동기 DB")
    print("  8 강. JWT 인증과 보안")
    print("-" * 60)
    print("[고급] 9-10 강: 프로덕션 레벨")
    print("  9 강. 실시간 통신 (WebSockets & SSE)")
    print("  10 강. 테스트 작성법 (Pytest)")
    print("="*60)
    print("\n🔗 Swagger UI: http://localhost:8000/docs")
    print("🚀 서버 실행: uvicorn main:app --reload")
