import os
import sys

# 프로젝트 루트 경로를 로드
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from sqlmodel import Session, select
from core.database import engine
from models import Course, Lesson

def expand_course_content():
    with Session(engine) as session:
        statement = select(Course).where(Course.title == "FastAPI 실무 마스터: 실전 레벨의 백엔드 구축하기")
        course = session.exec(statement).first()
        
        if not course:
            print("강좌를 찾을 수 없습니다. 다시 추가 스크립트를 실행해주세요.")
            return

        lessons = session.exec(select(Lesson).where(Lesson.course_id == course.id).order_by(Lesson.order)).all()
        
        if len(lessons) < 6:
            print("레슨 수가 6개 미만입니다.")
            return

        # 1. Dependency Injection 100배 보완
        lessons[0].content = """# FastAPI 실무: 한계 없는 의존성 주입 (Dependency Injection)

FastAPI가 다른 파이썬 웹 프레임워크와 차별화되는 가장 큰 무기는 강력한 **의존성 주입(Dependency Injection, DI) 시스템**입니다. 
초급 강의에서는 데이터베이스 세션을 주입받거나 현재 로그인한 유저를 가져오는 등 단순한 패턴만 배우지만, 실무 환경에서는 그보다 훨씬 복잡한 상황들을 마주하게 됩니다.

## 1. 제어의 역전(Inversion of Control)과 DI 체인 구축하기

현업에서는 API 엔드포인트(라우터)에 비즈니스 로직을 모두 때려 넣으면 스파게티 코드가 됩니다.
단일 책임 원칙(SRP)을 지키기 위해 여러 클래스와 함수로 로직을 쪼개다 보면 자연스럽게 클래스 간에 의존성이 생깁니다.

FastAPI의 DI는 **의존성의 의존성**을 무한으로 체인(Chain) 형태로 주입받을 수 있도록 설계되었습니다.

```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# 1. 가장 밑단의 DB 세션 의존성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 2. 레포지토리에 DB를 주입
class UserRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_user_by_id(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()

# 3. 서비스 레이어에 레포지토리를 주입
class UserService:
    def __init__(self, repo: UserRepository = Depends(UserRepository)):
        self.repo = repo
        
    def find_active_user(self, user_id: int):
        user = self.repo.get_user_by_id(user_id)
        if not user or not user.is_active:
            raise HTTPException(status_code=400, detail="Inactive user")
        return user

# 4. 엔드포인트에 서비스를 주입
@router.get("/users/{user_id}")
def read_user(user_id: int, service: UserService = Depends(UserService)):
    return service.find_active_user(user_id)
```

위의 예제처럼 `Depends`를 클래스 자체에 사용하면, FastAPI는 해당 클래스의 `__init__` 메서드 매개변수들을 분석하여 재귀적으로 의존성을 생성해 줍니다.
라우터 레이어에서는 `UserService`라는 완성된 객체 하나만 주입받아 사용하면 되므로 코드가 극도로 깔끔해지고 응집도(Cohesion)가 높아집니다.

---

## 2. Yield 기반 의존성: 리소스 관리의 정석

데이터베이스 연결 닫기, 임시 파일 삭제, 혹은 캐시 커넥션 반환과 같이 **사후 처리(Cleanup) 로직**이 필요한 경우 `yield` 예약어를 사용해야 합니다.
이 기능에 대한 완벽한 이해 없이 코딩하면 치명적인 메모리 누수(Memory Leak)와 커넥션 풀 고갈을 겪게 됩니다.

```python
import logging

logger = logging.getLogger(__name__)

async def get_redis_client():
    client = RedisClient.create()
    logger.info("Redis 연결 생성")
    
    try:
        # yield 전에는 요청 처리 전에 실행될 로직
        yield client
    except Exception as e:
        # FastAPI 과정에서 예외가 났을 때 처리할 곳
        logger.error(f"Redis 에러 발생: {e}")
        raise e
    finally:
        # 클라이언트에게 응답이 다 나간 직후 마지막으로 실행
        await client.close()
        logger.info("Redis 연결 안전하게 해제됨")
```

**실무 주의사항**: `yield`가 있는 의존성 블록 내부에 `BackgroundTasks`가 있다면, `finally` 블록의 해제가 완료된 **후에** 백그라운드 태스크가 실행됨을 명심하십시오. 만약 백그라운드에서 DB 의존성을 써야 한다면 `yield`로 생성된 세션 대신 **별도의 세션 팩토리**나 컨텍스트 관리자를 백그라운드 함수 안에서 직접 호출해야 안전합니다.

---

## 3. 의존성 캐싱 (Dependency Caching)

하나의 HTTP Request 라이프사이클 안에서 **동일한 의존성 함수가 여러 곳에서 호출될 때**, FastAPI는 기본적으로 해당 의존성을 단 1번만 실행하고 그 결과값을 메모리에 캐싱(Caching)합니다.

이 속성을 이용해 한 사이클에서 인증(Authentication) 로직을 중복 실행하지 않고 성능을 높일 수 있습니다.

```python
def verify_token(token: str = Header(...)):
    print("값비싼 토큰 검증 로직 수행 중...")  # 이 부분은 단 한 번만 찍힙니다.
    return decode(token)

def require_admin(user: dict = Depends(verify_token)):
    if not user.get("is_admin"):
        raise HTTPException(status_code=403, detail="Not an admin")
    return user

@router.get("/admin/dashboard")
def get_dashboard(
    token_data: dict = Depends(verify_token),  # 호출 1
    admin_data: dict = Depends(require_admin)  # 호출 2 (내부에서 다시 verify_token 호출)
):
    # 비록 verify_token이 의존성 트리에 2번 등장하지만
    # FastAPI는 캐싱되어 있는 첫 번째 결과값을 그대로 활용합니다.
    return {"message": "dashboard data"}
```
단, 매 호출마다 새로 계산된 값을 받고 싶다면 `Depends(dependency_func, use_cache=False)` 와 같이 캐시 플래그를 꺼주어야 합니다.
(예: 현재 시각 밀리초 단위 생성기, 난수 발생기 등).

---

## 4. 커스텀 컨텍스트와 다중 테넌시(Multi-tenancy)

단일 서버로 여러 고객사(Tenant)에게 SaaS 서비스를 제공하는 B2B 시스템을 구축한다고 가정합시다. 고객사마다 독립된 데이터베이스 스키마나 인스턴스를 바라봐야 한다면, 이를 `Depends` 안에서 분기 처리하는 것이 가장 깔끔한 방법입니다.

```python
from fastapi import Request

def get_tenant_id(request: Request) -> str:
    # 헤더나 서브도메인에서 테넌트 식별자를 추출
    tenant_id = request.headers.get("X-Tenant-ID")
    if not tenant_id:
        raise HTTPException(status_code=400, detail="Tenant ID is required")
    return tenant_id

# 요청을 보낸 테넌트의 DB 세션만을 생성하여 주입
def get_tenant_db(tenant_id: str = Depends(get_tenant_id)):
    engine = get_engine_for_tenant(tenant_id)
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()

@router.get("/companies/users")
def get_company_users(db: Session = Depends(get_tenant_db)):
    # 이 라우터는 100개의 테넌트가 각기 다른 DB를 사용하지만 
    # 코드는 전혀 수정할 필요가 없는 구조가 됩니다.
    return db.query(User).all()
```

이 패턴의 파괴적인 장점은 라우터 함수(`/companies/users`)가 "우리가 어떤 테넌트의 데이터베이스를 쓰고 있는가?" 에 대해 전혀 몰라도 상관이 없다는 점입니다. 완벽하게 비즈니스 로직과 컨텍스트 로직이 분리됩니다.

---

## 5. 실무 필수: 테스트 환경에서의 Dependency Override

시스템이 커지고 외부 API 연동이 포함되면서, 이를 모두 Mocking 하여 격리된(Unit) 환경에서 테스트하는 것이 매우 중요해집니다.
`app.dependency_overrides` 맵을 사용하면 FastAPI 애플리케이션의 의존성을 런타임에 동적으로 교체(Swap)할 수 있습니다.

**실제 코드(main.py)**:
```python
def fetch_weather_from_third_party():
    # 외부 유료 API 네트워크 호출
    return httpx.get("https://api.weather.com/v1/...").json()

@app.get("/weather/today")
def today_weather(data: dict = Depends(fetch_weather_from_third_party)):
    return {"weather": data}
```

**테스트 코드(test_main.py)**:
```python
from fastapi.testclient import TestClient
from main import app, fetch_weather_from_third_party

client = TestClient(app)

# 1. 목업(Mock) 함수 생성
def override_weather():
    return {"status": "sunny", "temp": 25}

# 2. 의존성 바꿔치기 (Override)
app.dependency_overrides[fetch_weather_from_third_party] = override_weather

def test_today_weather():
    # 3. 네트워크 통신 없이 순식간에 테스트 통과!
    response = client.get("/weather/today")
    assert response.status_code == 200
    assert response.json() == {"weather": {"status": "sunny", "temp": 25}}
    
# 4. 테스트 종료 후 초기화
app.dependency_overrides.clear()
```

위 5가지 DI의 핵심 활용법을 마스터한다면 어떤 규모의 복잡한 서비스라도 깔끔하고 확장 가능한 FastAPI 아키텍처를 설계할 수 있을 것입니다.
"""

        # 2. Async SQLAlchemy & Repository
        lessons[1].content = """# SQLAlchemy 2.0 비동기(Async) 처리와 Repository 패턴 심화 가이드

FastAPI와 궁합이 가장 좋은 ORM은 `SQLAlchemy 2.0` 입니다.
비동기 환경 위에서 만들어진 FastAPI의 장점을 100% 활용하려면 SQLAlchemy를 비동기(Async) 방식으로 튜닝해야만 합니다. 본 레슨에서는 단순히 데이터베이스를 연결하는 수준을 벗어나, 동시성 트래픽이 폭발했을 때 견뎌내는 커넥션 풀 작성법과 Repository 확장 패턴을 학습합니다.

---

## 1. Asyncpg 드라이버와 AsyncEngine 최적화

Python의 기본 `psycopg2`와 같은 동기적 드라이버를 쓰게 되면, 쿼리를 던지고 답변을 기다리는 수 밀리초(ms) 과정 내내 쓰레드가 차단(Block)됩니다. 
비동기 환경을 활용하려면 Postgres의 경우 `asyncpg` (또는 `psycopg` v3의 비동기 모드), MySQL은 `aiomysql` 등 비동기 지원용 드라이버를 설치해야 합니다.

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

# 비동기 드라이버 선언
DATABASE_URL = "postgresql+asyncpg://admin:pass@postgres_host:5432/my_db"

# 커넥션 풀(Pool)과 관련된 심화 설정
engine = create_async_engine(
    DATABASE_URL, 
    echo=False,  # 운영 환경에서는 반드시 False (디버깅용)
    pool_size=20,  # 기본 유지 커넥션 수
    max_overflow=10,  # 순간적인 트래픽 급증 시 추가 허용 커넥션 수
    pool_recycle=3600,  # 1시간마다 커넥션을 재생성하여 DB Time-out 방지
    pool_pre_ping=True  # 쿼리 던지기 전에 연결 유효성 테스트 (실무 필수 옵션)
)

# 세션 팩토리 생성 (expire_on_commit=False 필수)
AsyncSessionLocal = async_sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)
```

**왜 `expire_on_commit=False`가 필수인가요?**
비동기 세션에서는 트랜잭션을 commit 한 직후 세션에 묶여있던 객체들의 상태가 '만료(expired)' 처리됩니다. 이때 이 객체의 속성에 다시 접근하게 되면 내부적으로 쿼리를 새로 던지려(Lazy Load) 시도하는데, 이 I/O 행위가 비동기 래퍼 바깥에서 발생하여 무시무시한 `MissingGreenletException` 오류를 뿜어내고 서버가 죽는 현상이 흔히 발생합니다.
값을 메모리에 그대로 둔 채 안전하게 리턴하기 위한 방어 장치입니다.

---

## 2. 실전 Repository 패턴 (Generic Repository 방식)

실무에서 데이터 접근 객체(Data Access Object)를 만들 때, 매 모델마다 반복되는 `create`, `get`, `update`, `delete` CRUD 함수를 지루하게 짜는 것은 비효율적입니다.
이를 파이썬의 `Generic` 타입을 활용해 하나의 베이스 클래스로 통일하는 패턴이 현업에서 각광받습니다.

```python
from typing import Generic, TypeVar, Type, Optional, List
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel

ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=SQLModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=SQLModel)

class AsyncBaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType], db: AsyncSession):
        self.model = model
        self.db = db

    async def get_by_id(self, id: int) -> Optional[ModelType]:
        query = select(self.model).where(self.model.id == id)
        result = await self.db.execute(query)
        return result.scalars().first()
        
    async def get_multi(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        query = select(self.model).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def create(self, obj_in: CreateSchemaType) -> ModelType:
        # Pydantic dict 파싱 후 모델에 적재
        db_obj = self.model.model_validate(obj_in)
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj
```
이제 개발자는 단순히 상속만 받아서 아래처럼 극도의 생산성을 뽑아낼 수 있습니다.
```python
# User 모델을 위한 레포지토리가 3줄만에 탄생함
class UserRepository(AsyncBaseRepository[User, UserCreate, UserUpdate]):
    def __init__(self, db: AsyncSession):
        super().__init__(User, db)
        
    # User만의 특수한 쿼리만 추가 정의
    async def get_by_email(self, email: str):
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalars().first()
```

---

## 3. 마의 구간: 비동기 릴레이션십(Relationship) N+1 문제 해결

비동기 ORM을 쓴다면 레이지 로딩(Lazy Loading)의 시대는 끝났습니다. 연관된 릴레이션을 호출하는 순간 `await`를 걸지 못하기 때문에 (객체의 속성 접근 `post.user` 처럼 점(.)으로 접근하기 때문) 에러가 떨어집니다. 
이를 예방하기 위해 조인(Join) 로딩 전략을 쿼리 수준에서 확정 지어주어야 합니다.

### a. Selectin 로딩방식 (`selectinload`)
`1:N` 혹은 `N:M` 관계를 불러올 때 최고의 효율을 보여줍니다. `IN()` 조건문을 활용하므로 데이터 구조가 복잡해도 곱연산(Cartesian Product) 현상이 생기지 않습니다.
```python
from sqlalchemy.orm import selectinload

async def get_course_with_lessons(course_id: int, db: AsyncSession):
    # Course 안의 lessons 컬렉션을 사전에 끌어오도록 명시
    query = select(Course).options(selectinload(Course.lessons)).where(Course.id == course_id)
    result = await db.execute(query)
    # 이제 course.lessons 에 접근해도 에러가 나지 않고 메모리에 담겨있습니다!
    return result.scalars().first()
```

### b. Joined 로딩방식 (`joinedload`)
`1:1` 혹은 `N:1` 관계(예: 포스트와 작성자)에서 단일 조인으로 깔끔하게 데이터를 가져올 때 유리합니다.
```python
from sqlalchemy.orm import joinedload

async def get_lesson_with_course(lesson_id: int, db: AsyncSession):
    # LEFT OUTER JOIN 혹은 INNER JOIN이 쿼리에 포함되어 단 1번의 쿼리로 병합된 결과를 뱉음
    query = select(Lesson).options(joinedload(Lesson.course)).where(Lesson.id == lesson_id)
    result = await db.execute(query)
    return result.scalars().first()
```

---

## 4. Alembic 비동기 마이그레이션 셋업(Environment Setup)

비동기 DB 연결을 사용했다면 리비전 관리 도구인 `Alembic` 또한 비동기 셋업을 거쳐야 합니다.
`alembic.ini`와 `env.py` 파일을 수정해야 작동합니다. 핵심 로직인 `env.py`에서 비동기 컨텍스트(Coroutine)를 생성해주는 구조를 만듭니다.

`env.py`
```python
import asyncio
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context
from sqlmodel import SQLModel
# Models 안에 작성한 내 객체들 Import
import models 

target_metadata = SQLModel.metadata

def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations():
    # 비동기로 엔진 생성 후 마이그레이션 실행
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()

def run_migrations_online():
    # 비동기 루프 안에서 호출
    asyncio.run(run_async_migrations())
```
위처럼 세팅하면 `alembic revision --autogenerate`, `alembic upgrade head` 명령어가 비동기 엔진에서도 충돌 없이 아주 매끄럽게 동작합니다. 

"""

        # 3. OAuth2 & RBAC
        lessons[2].content = """# 심화 보안 아키텍처: JWT Access & Refresh Token과 인가 제어(RBAC)

사용자의 권한과 정보를 안전하게 인증(Authentication)하고 특정 동작을 인가(Authorization)하는 것은 모든 서비스의 근간입니다.
본 챕터에서는 FastAPI 프레임워크가 제공하는 강력한 보안 툴과 JWT(Jason Web Token)의 Lifecycle 관리법, 그리고 토큰 강제 만료(Revoke), 역할 기반 접근 통제(RBAC) 등 현업 보안 정책의 100%를 보여줍니다.

---

## 1. Access Token과 Refresh Token의 차별화

### 토큰 분리의 이유
토큰 하나로 로그인 시스템을 돌리게 되면 그 토큰의 만료 시간을 길게 설정할 수밖에 없습니다. (예: 2주) 문제는 만약 해커나 중간자(MITM) 공격으로 이 토큰이 탈취당한다면, 서버는 이를 감지할 수 없고 해커는 2주 내내 피해자의 계정을 마음대로 조작하게 됩니다.
따라서, **Access Token의 생명주기를 극도로 짧게 (15분 ~ 1시간)** 하고, **Refresh Token(수주~수개월)을 통해서 짧은 주기의 Access Token을 다시 재발급받게 하는 아키텍처**를 구성합니다. 

여기에 더해 Refresh Token은 자바스크립트 등에서 접근하지 못하도록 `httpOnly=True`, `secure=True`, `samesite="Strict"` 보안 쿠키 속성으로 내려주는 것이 대세입니다.

```python
# 토큰 생성 로직 예시
from datetime import datetime, timedelta
from jose import jwt

SECRET_KEY = "my_super_secret_high_entropy_key"
ALGORITHM = "HS256"

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=15)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(subject: str, expires_delta: timedelta = timedelta(days=14)):
    expire = datetime.utcnow() + expires_delta
    to_encode = {"sub": subject, "exp": expire, "type": "refresh"}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
```

`Login` 엔드포인트에서는 이 두 가지 토큰을 생성해 클라이언트에게 각각 적절한 매체(액세스는 JSON Body로, 리프레시는 Set-Cookie 헤더로)로 전달해야 합니다.

```python
@router.post("/login")
async def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    
    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token(str(user.id))
    
    # Refresh Token을 브라우저 보안 쿠키에 셋팅
    response.set_cookie(
        key="refresh_token", 
        value=refresh_token, 
        httponly=True, 
        secure=True, 
        samesite="lax",
        max_age=14 * 24 * 60 * 60 # 14일
    )
    
    return {"access_token": access_token, "token_type": "bearer"}
```

---

## 2. Redis 기반의 Blacklist (Token Revocation) 

기본적으로 JWT는 Stateless(상태 비저장형) 디자인이므로 서버는 한 번 발급된 토큰을 제어할 방법이 없습니다. 
- "사용자가 비밀번호를 변경하는 순간 기기에서 강제 로그아웃 시켜야 한다."
- "사용자가 자발적으로 로그아웃 버튼을 눌렀을 때 토큰을 무효로 만들어야 한다."

이를 구현하기 위해 **Redis (비동기 인메모리 DB)** 를 블랙리스트 저장소로 활용합니다. 로그아웃된(또는 만료되어야 할) 토큰의 ID(`jti` 혹은 `토큰 본문`)를 Redis에 저장하고, 모든 인증 미들웨어나 의존성에서 JWT 검증 시 먼저 Redis에 해당 토큰이 존재하는지 확인합니다.

```python
import redis.asyncio as redis

redis_client = redis.Redis(host='localhost', port=6379, db=0)

async def revoke_token(token: str, expiration_time_left: int):
    # 토큰의 남은 수명만큼만 Redis에 저장(EX 옵션) 후 시간이 지나면 자동 소멸
    await redis_client.setex(name=f"blacklist:{token}", time=expiration_time_left, value="revoked")

async def is_token_revoked(token: str) -> bool:
    is_revoked = await redis_client.exists(f"blacklist:{token}")
    return is_revoked == 1
```

```python
async def get_current_user(token: str = Depends(oauth2_scheme)):
    # 1. 블랙리스트 검사
    if await is_token_revoked(token):
        raise HTTPException(status_code=401, detail="Token has been revoked. Please log in again.")
        
    # 2. JWT Decode 검사
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    # ... 유저 조회 성공 로직
```
이 과정을 통해 토큰의 무결성+통제권 두 마리 토끼를 잡을 수 있습니다!

---

## 3. 강력한 역할 통제 체제 (Role-Based Access Control) 패턴

사용자가 확인되었으면 다음은 *"이 사용자가 이 행동을 할 권한이 있는지?"* 검사할 차례입니다.
FastAPI의 의존성 주입 계층도를 사용하면 놀라우리만치 깔끔하게 데코레이터식 권한 검사기를 생성할 수 있습니다.

**Role 검사기 클래스 작성**:
```python
from fastapi import Security

class RoleChecker:
    def __init__(self, allowed_roles: list[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, user: User = Depends(get_current_active_user)):
        # 유저 테이블의 role 속성("USER", "ADMIN", "SUPERADMIN" 등)
        if user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=403, 
                detail=f"Operation not permitted. Required roles: {self.allowed_roles}"
            )
        return user
```
이것이 전부입니다. 파이썬의 Magic Method 중 하나인 `__call__`을 구현해 두면, 이 클래스의 인스턴스 자체가 하나의 함수처럼 행동하기 때문에 의존성(Depends)에 곧바로 주입할 수 있습니다.

**적용 예시**:
```python
# 인스턴스화
allow_admin_only = RoleChecker(["ADMIN", "SUPERADMIN"])
allow_staff = RoleChecker(["STAFF", "ADMIN", "SUPERADMIN"])

# 엔드포인트에 초간단하게 적용
@router.post("/system/config")
async def update_config(data: ConfigData, current_user = Depends(allow_admin_only)):
    # 이 로직은 오직 ADMIN 이상 롤을 부여받은 사람만이 도달할 수 있습니다.
    return {"message": "Config updated successfully"}
    
@router.get("/reports/stats")
async def read_reports(current_user = Depends(allow_staff)):
    # 이 로직은 STAFF 이상 도달 가능
    return get_daily_reports()
```
비즈니스가 성장하여 복잡한 퍼미션(`"read:users"`, `"write:payments"` 등) 구조로 변모하더라도 저 `RoleChecker` 내부 로직만 변경하면 끝입니다.
"""

        # 4. WebSockets & SSE
        lessons[3].content = """# 실시간 양방향 데이터: WebSockets & Server-Sent Events 완벽 정복

기존 HTTP 프로토콜은 "요청을 해야만 응답이 온다"는 치명적인 한계(Stateless)를 갖고 있습니다.
주식 차트 갱신, 유저 간 채팅, 실시간 시스템 모니터링, 대용량 파일 가공 진척도(Progress bar) 표시 등은 클라이언트가 서버에 폴링(Polling)을 시도하면 서버 비용이 폭주하게 됩니다.
FastAPI는 파이썬 비동기 생태계인 `Starlette`의 코어를 활용하여 WebSockets와 SSE 처리를 매우 가볍고 직관적으로 지원합니다.

---

## 1. WebSocket 101: Connection Manager로 무리 짓기

FastAPI에서 단일 유저와 WebSocket을 맺는 것은 너무나 쉽습니다. (`@app.websocket("/ws")`)
하지만 실제 서비스에서는 브로드캐스팅(접속한 전원에게 메시지 전송), 혹은 특정 유저(Private Chat)에게 전송하는 커넥션 풀을 관리해야 합니다.

**강력한 커넥션 매니저 클래스 작성:**
```python
from fastapi import WebSocket
from typing import Dict, List

class ConnectionManager:
    def __init__(self):
        # 딕셔너리로 특정 user_id에 종속된 소켓 목록 통합 관리
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)

    def disconnect(self, websocket: WebSocket, user_id: str):
        if user_id in self.active_connections:
            self.active_connections[user_id].remove(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]

    async def send_personal_message(self, message: str, user_id: str):
        # 특정 유저가 여러 탭/디바이스를 띄웠을 수 있으므로 순회 발송
        if user_id in self.active_connections:
            for connection in self.active_connections[user_id]:
                await connection.send_text(message)

    async def broadcast(self, message: str):
        # 현재 연결된 모든 커넥션에게 알림
        for user_sockets in self.active_connections.values():
            for connection in user_sockets:
                await connection.send_text(message)

manager = ConnectionManager()
```

**라우터 적용 및 예외 처리:**
웹소켓 끊어짐은 정상 종료(Status 1000)뿐만 아니라 와이파이 단절, 크롬 탭 닫기 등으로 무자비하게 발생합니다. `WebSocketDisconnect` 예외를 반드시 잡아주어야 서버 크래시를 면합니다.
```python
from fastapi import WebSocketDisconnect

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await manager.connect(websocket, user_id)
    try:
        while True:
            # 1. 클라이언트가 보내는 메시지 수신 대기
            data = await websocket.receive_text()
            
            # 2. 개인 메시지 에코백
            await manager.send_personal_message(f"You wrote: {data}", user_id)
            
            # 3. 브로드캐스팅
            await manager.broadcast(f"User #{user_id} says: {data}")
            
    except WebSocketDisconnect:
        # 클라이언트 연결 해제 감지
        manager.disconnect(websocket, user_id)
        await manager.broadcast(f"User #{user_id} left the chat")
```

---

## 2. 서버 스케일 아웃(Scale-out) 시의 WebSocket 한계와 Redis Pub/Sub

Uvicorn이나 컨테이너(Docker) 기반 운영 환경에서는 여러 개의 작업자(Worker Process) 또는 서버 노드가 구동됩니다.
사용자 A는 Server 1에 붙어있고, 사용자 B는 Server 2에 연결되어 있다면, **위에서 만든 `manager.broadcast` 는 자신이 속한 프로세스 로컬의 파이썬 리스트에만 알림을 보냅니다.** (즉 사용자 B는 알림을 받지 못함)

이 거대한 장애물을 해결하는 디자인 패턴이 **Redis Pub/Sub (채널 구독 패턴)** 입니다.

1. 모든 백엔드 서버는 시작(Startup) 시점에 Redis 커넥션을 물고 특정 채널(예: `"chat_events"`)을 `Subscribe` 합니다.
2. 사용자 A가 웹소켓으로 메시지를 보냅니다.
3. Server 1은 이를 파이썬 리스트로 발송하는 대신 `redis.publish("chat_events", data)` 구문으로 Redis에 쏩니다.
4. 모든 Server (1번, 2번 ...) 가 Redis로부터 알람을 받고 이 이벤트를 청취해 자신들에게 연결된 로컬 클라이언트들에게 일제히 `websocket.send()` 릴레이를 펼칩니다.
이 패턴을 도입하면 서버가 1,000 대 모여 있더라도 끊김 없이 모든 글로벌 채팅이 실시간 동기화됩니다!

---

## 3. 오직 서버가 말할 때: Server-Sent Events (SSE) 도입하기

클라이언트가 주기적으로 정보를 던지는 것이 아니라 주식 실시간 가격, 크롤링 퍼센테이지, GPT 답변 스트리밍처럼 **오직 일방형으로 서버가 내려주는 역할만 필요하다면** WebSocket은 다소 무겁고 Overkill 이 될 수 있습니다.

HTTP 통신 위로 이벤트 스트림을 계속 밀어 넣는 SSE 아키텍처는 코드 구현이 놀라우리만치 단순합니다. `StreamingResponse`와 `async generator` 문법의 조합으로 완성됩니다.

```python
import asyncio
from fastapi.responses import StreamingResponse

async def event_generator():
    counter = 0
    while True:
        # 1초마다 지속적으로 처리 상태를 클라이언트에 던집니다.
        # SSE의 규격인 'data: [데이터텍스트]\\n\\n' 포맷을 유지해야 합니다.
        yield f"data: {{'status': 'Processing', 'progress': {counter}%}}\\n\\n"
        
        counter += 10
        await asyncio.sleep(1) # 블로킹 되지 않는 비동기 슬립
        
        if counter > 100:
            yield "data: {'status': 'Completed'}\\n\\n"
            break

@app.get("/stream-progress")
async def stream_progress():
    # Content-Type을 text/event-stream으로 고정해야만 
    # 브라우저의 EventSource 객체가 이를 스트림으로 인식합니다.
    return StreamingResponse(event_generator(), media_type="text/event-stream")
```
클라이언트 측 HTML 자바스크립트는 3 줄이면 충분합니다.
```javascript
const eventSource = new EventSource("/stream-progress");
eventSource.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log("Progress:", data.progress);
    if(data.status === 'Completed') eventSource.close();
};
```
목적에 따라 실시간 통신 도구(WebSocket vs SSE)를 지능적으로 선택해 고도화된 아키텍처를 설계하세요.
"""

        # 5. Middleware & Profiling
        lessons[4].content = """# 미들웨어의 정석과 애플리케이션 프로파일링(Profiling)

API로 수신된 HTTP 파장(Request)은 라우터 함수(기능 로직)가 처리하기 전에 반드시 애플리케이션의 문지기를 거치게 됩니다.
우리는 이를 **미들웨어(Middleware)** 라고 부르며, 로그 수집, 암호화 처리, IP 차단 등 횡단 관심사(Cross-cutting Concerns)를 해결하는 최적의 장소입니다.

단순하게 만들어진 미들웨어는 비동기 성능 병목의 원흉이 됩니다. 올바른 작성법과 병목을 찾아내는 기술을 습득합시다.

---

## 1. BaseHTTPMiddleware의 함정과 해결책

FastAPI 튜토리얼을 보면 보통 `@app.middleware("http")`를 이용해 미들웨어를 쉽게 작성하라고 합니다. 이 방식 내부에는 `BaseHTTPMiddleware`가 숨어있습니다.
하지만 이 방식은 FastAPI 애플리케이션이 파일 업로드(`MultipartForm`)처럼 바디(Body)를 스트리밍하는 구간에서 치명적인 버그(요청 멈춤)를 종종 일으킵니다.

가장 성능이 좋고 버그가 없는 현업 미들웨어는 Starlette 레이어의 기본 형태인 순수 **ASGI 미들웨어** 형태로 클래스를 제작하는 것입니다.

```python
# ASGI를 직접 다루는 최상위 미들웨어 골격
class RequestTimeMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        # HTTP 프로토콜이 아닌 경우 개입하지 않고 패스
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        import time
        start_time = time.time()
        
        # 내부 로직으로 진입(라우터 실행 등)
        await self.app(scope, receive, send)
        
        # 응답이 끝난 직후 로깅
        process_time = time.time() - start_time
        path = scope["path"]
        print(f"[{path}] 요청 처리 소요 시간: {process_time:.5f}초")
```
이 뼈대 위에 Correlation ID(에러 추적을 위한 UUID 헤더 발급) 등을 심어두면, MSA(Microservice Architecture)로 수많은 서버가 통신을 거칠 때 로그 파일 하나만 보면 요청의 흐름을 모두 연결(Tracing)해 볼 수 있게 됩니다.

---

## 2. 성능의 암살자(Bottleneck) 찾기: Pyinstrument 프로파일링

코드를 작성하고 로컬에서 돌려봤을 때 API가 응답하기까지 체감상 1~2초가 걸린다면? 감으로 "DB가 느리겠지?" 라고 의심하는 것은 엔지니어의 자세가 아닙니다.
`Pyinstrument`는 함수들의 Call Stack 구조를 실시간 스캐닝 한 후 멋진 퍼포먼스 트리로 보여줍니다.

**미들웨어를 활용해 나만의 프로파일링 트리 조회 기능 만들기:**
```python
from pyinstrument import Profiler
from fastapi.responses import HTMLResponse
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request

class ProfilerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 쿼리 파라미터에 '?profile=true' 가 달렸을 때만 프로파일러 가동!
        profile_flag = request.query_params.get("profile", "false") == "true"
        
        if profile_flag:
            profiler = Profiler(interval=0.001, async_mode="enabled")
            profiler.start()
            
        response = await call_next(request)
        
        if profile_flag:
            profiler.stop()
            # 프로파일링 기록을 멋진 HTML 리포트로 즉시 랜더링해서 브라우저로 리턴!
            return HTMLResponse(profiler.output_html())
            
        return response

# app 설정 파일에서
# app.add_middleware(ProfilerMiddleware)
```
놀라운 생산성 기술입니다! 프론트엔드에서 버튼을 눌렀는데 반응이 느리다고 리포트를 받으면, 엔지니어는 브라우저에 접속해 URL 뒤에 `?profile=true` 하나만 입력하면 **"어느 파일의 몇 번째 라인에서 0.5초를 소진하고 있는지"** 압도적인 그래픽으로 알 수 있습니다.

---

## 3. Rate Limiter (요청 횟수 제한기) 구현 전략의 정수

과도한 API 트래픽 공격(DDoS)이나 크롤링 봇들의 자원 고갈을 막기 위해 1분당 API 접근을 100회로 제한하는 등의 `Rate Limiting` 로직을 짜야 합니다.
파이썬 배열 메모리에 임시로 카운팅하는 짓은 워커가 2대 이상일 때 쓸모가 없어지므로 절대 해선 안됩니다. 

Redis의 `INCR`(증가) 과 `EXPIRE`(만료) 커맨드를 조합한 Sliding Window Counter나 단순히 시간 버킷을 만드는 알고리즘을 사용합니다. 
FastAPI 현업 진영에서는 **`slowapi`** 라이브러리를 많이 사용하지만, 개념 파악을 위해 코어 의존성을 만들어봅시다.

```python
import redis.asyncio as redis
from fastapi import HTTPException, Request, Depends

r = redis.Redis(host="localhost", port=6379, db=1)

# 특정 IP에 대해 60초당 5번만 허용하는 의존성 함수
async def rate_limit(request: Request):
    client_ip = request.client.host
    # 현재 분(Minute) 단위를 키로 생성 (예: limit:192.168.0.1:2026-03-02T10:45)
    import time
    current_minute = int(time.time() / 60)
    
    redis_key = f"rate_limit:{client_ip}:{current_minute}"
    
    # 요청 카운팅 (원자적 연산)
    current_requests = await r.incr(redis_key)
    
    # 새로운 키일 경우 60초 후 삭제되게 타이머 부착
    if current_requests == 1:
        await r.expire(redis_key, 60)
        
    if current_requests > 5:
        raise HTTPException(status_code=429, detail="Too Many Requests. Please try again later.")
        
@app.get("/premium-data", dependencies=[Depends(rate_limit)])
async def get_premium_data():
    return {"data": "This data is rate limited."}
```
복잡한 알고리즘을 수백 줄 짤 필요 없이 Redis의 원자적 접근 속성(Atomic Operation)을 지렛대 삼아 안정적이고 확장 가능한 Rate Limiter 아키텍처를 획득할 수 있습니다.
"""

        # 6. Production Deployment
        lessons[5].content = """# Gunicorn과 Docker 기반 무중단 롤링 배포 및 CI/CD 파이프라인

로컬 터미널에서 `uvicorn main:app --reload` 를 통해 개발을 아무리 훌륭하게 끝냈어도, 리눅스 프로덕션 서버에 그대로 띄우는 것은 재앙을 부릅니다.
단일 Uvicorn 프로세스는 Python의 특징인 GIL(Global Interpreter Lock)과 단일 코어 사용의 제약으로 트래픽이 몰리면 속절없이 뻗어버립니다. 
이를 전문적으로 방어하고 스케일링하는 방법, 도커 최적화, 그리고 자동화된 배포 과정을 모두 정리합니다.

---

## 1. Gunicorn (프로세스 매니저) + Uvicorn (ASGI 워커) 의 위대한 조합

`Uvicorn` 은 비동기 소켓을 빠릿하게 처리하는 데 탁월하지만, 서버 내 프로세스 라이프사이클 관리나 데몬화(Daemonizing), 여러 개의 코어 배분 능력이 약합니다.
반면 `Gunicorn`은 수십 년간 파이썬 WSGI 세계관을 지배해온 강력한 멀티 프로세스 매니저입니다. Gunicorn의 껍데기에 Uvicorn의 커널을 탑재해 펀치력을 100배 상승시킵니다.

**운영 서버 실행 스크립트:**
```bash
# 기본적으로 서버 CPU 코어 수가 4개일 때, Gunicorn 워커는 [코어 수 * 2 + 1]을 권장합니다. 즉 9개의 워커!
gunicorn main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --timeout 120 \
  --keep-alive 5 \
  --log-level info
```
만약 워커 1이 어떤 복잡한 연산을 하느라 일시 트래픽 블로킹에 빠져도 Gunicorn 마스터는 즉시 다른 워커 2,3,4 로 들어오는 요청들을 배분하기 때문에 서비스 지연을 막습니다.

---

## 2. Dockerfile 최적화와 멀티 스테이지 빌드 (Multi-stage Build)

컨테이너가 무거우면(예: 이미지 사이즈 1.5GB) 롤링 업데이트 시 다운로드 지연이 발생하고 인프라 비용과 보안 취약점 공격 면적이 늘어납니다. 
현업에서 사용하는 이상적인 Dockerfile은 **'빌드 결과물은 가볍게, 캐시 레이어는 적극적으로'** 철학을 따릅니다. 파이썬 최신 매니저인 `uv`나 `poetry`를 쓸 때 이상적인 형태는 아래와 같습니다.

**최적화된 Dockerfile.prod**
```dockerfile
# 스테이지 1: 패키지 빌더 (의존성 설치 등 무거운 작업 전용)
FROM python:3.11-slim as builder

WORKDIR /app
# 빌드에 필요한 C-컴파일 툴체인(gcc 등) 임시 설치
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# requirements 최적화, 가상환경(/venv) 통째로 구워내기
COPY requirements.txt .
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt

# 스테이지 2: 초경량 프로덕션 이미지 (위에서 만든 /venv 폴더만 쏙 빼본다)
FROM python:3.11-slim

WORKDIR /app
# 런타임에 필요한 초경량의 C 라이브러리만 설치 (gcc 제외로 용량 300MB 이상 다이어트)
RUN apt-get update && apt-get install -y --no-install-recommends libpq5 && rm -rf /var/lib/apt/lists/*

# 스테이지 1(builder)에서 생성된 가상 환경을 런타임 이미지로 복사해옵니다.
COPY --from=builder /venv /venv
ENV PATH="/venv/bin:$PATH"

# 소스코드 전체 복사 및 권한 세팅 (root 사용 금지)
COPY . .
RUN useradd -m fastapi_user && chown -R fastapi_user:fastapi_user /app
USER fastapi_user

EXPOSE 8000

# Gunicorn+Uvicorn 조합으로 실행 명령
CMD ["gunicorn", "main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000"]
```

이 다이어트된 이미지는 무중단 CI 시스템 상에서 빛의 속도로 배포됩니다.

---

## 3. GitHub Actions를 이용한 무중단(CI/CD) 자동화

서버에 직접 SSH로 붙어서 `git pull` 치던 시대는 지났습니다. 개발자가 코드를 GitHub `main`에 머지(Merge)하는 순간, 자동으로 코드를 검사하고(CI), 이미지를 말아서, 상용 서버를 무중단 상태로 업데이트(CD) 하는 YAML 파이프라인의 핵심 구조를 공개합니다.

**.github/workflows/deploy.yml**
```yaml
name: FastAPI Production Deploy

on:
  push:
    branches:
      - main

jobs:
  test_and_build:
    name: Test and Build Docker Image
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies & Pytest
        run: |
          pip install -r requirements.txt
          pytest tests/ --cov=./ -v  # 코드가 깨진 상태라면 여기서 배포가 방어됩니다(매우 중요)

      - name: Build & Push Docker Image
        uses: docker/build-push-action@v4
        with:
          context: .
          file: ./Dockerfile.prod
          push: true  # AWS ECR, DockerHub 등 레지스트리에 이미지 푸시
          tags: ${{ secrets.DOCKER_USER }}/fastapi-app:latest

  deploy_to_server:
    name: Server Zero-Downtime Deploy
    needs: test_and_build  # 테스트와 빌드가 무사히 끝난 뒤에만 도달
    runs-on: ubuntu-latest
    steps:
      - name: Execute Remote SSH Command
        uses: appleboy/ssh-action@v0.1.7
        with:
          host: ${{ secrets.SERVER_IP }}
          username: ${{ secrets.SERVER_USER }}
          key: ${{ secrets.SERVER_SSH_KEY }}
          script: |
            # 무중단을 위한 Blue/Green 배포 스크립트 또는 docker-compose 롤링 업데이트 기법 삽입
            docker pull ${{ secrets.DOCKER_USER }}/fastapi-app:latest
            # 1. 새 컨테이너 띄우기
            docker run -d --name fastapi_new -p 8001:8000 ${{ secrets.DOCKER_USER }}/fastapi-app:latest
            # 2. 로드밸런서(Nginx)가 8001로 트래픽 방향 전환 (NGINX Reload)
            sudo bash reload_nginx_to_new_port.sh
            # 3. 엣지 테스트 통과하면 기존 구버전 컨테이너 삭제
            docker stop fastapi_old || true && docker rm fastapi_old || true
```

초록 불이 켜지며 성공적인 Actions 라벨이 붙는 순간, 개발자의 고된 밤샘은 끝나고 마이크로서비스 확장이 가능해집니다.
"""

        for lesson in lessons:
            session.add(lesson)

        session.commit()
        print("훌륭합니다! 6개의 레슨이 100배 보완된 심도 깊고 압도적인 콘텐츠로 업데이트 되었습니다.")

if __name__ == "__main__":
    expand_course_content()
