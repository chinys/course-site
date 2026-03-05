import os
import sys

# 프로젝트 루트 경로를 sys.path에 추가하여 core, models 모듈을 로드할 수 있게 함
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from sqlmodel import Session, select
from core.database import engine
from models import Category, Course, Lesson

def seed_fastapi_course():
    with Session(engine) as session:
        # '프로그래밍' 카테고리 확인 또는 생성
        statement = select(Category).where(Category.name == "프로그래밍")
        category = session.exec(statement).first()
        
        if not category:
            category = Category(name="프로그래밍", order=10)
            session.add(category)
            session.commit()
            session.refresh(category)
            print(f"'프로그래밍' 카테고리가 새로 생성되었습니다. (ID: {category.id})")
        else:
            print(f"'프로그래밍' 카테고리가 이미 존재합니다. (ID: {category.id})")

        # 기존 FastAPI 강좌 확인
        statement = select(Course).where(Course.title == "FastAPI 실무 마스터: 실전 레벨의 백엔드 구축하기")
        existing_course = session.exec(statement).first()
        if existing_course:
            print("FastAPI 실무 마스터 강좌가 이미 존재합니다. 업데이트를 위해 기존 강좌를 삭제합니다.")
            session.delete(existing_course)
            session.commit()
        
        # FastAPI 실무 강좌 생성
        course = Course(
            title="FastAPI 실무 마스터: 실전 레벨의 백엔드 구축하기",
            description="파이썬 기초 이론을 넘어서, 현업에서 실제로 쓰이는 FastAPI의 고급 기능, 비동기 데이터베이스 처리, 보안, 웹소켓, 및 배포 전략을 아우르는 수준 높은 실무 중심 강좌입니다.",
            thumbnail_url="/static/images/fastapi_thumbnail.png",
            category_id=category.id
        )
        session.add(course)
        session.commit()
        session.refresh(course)
        print(f"강좌 생성 완료: {course.title} (ID: {course.id})")

        # 레슨 데이터 (실무 중심의 상세한 컨텐츠)
        lessons_data = [
            {
                "title": "1. FastAPI 고급 의존성 주입(Dependency Injection)과 제어 역전",
                "content": """# FastAPI 고급 의존성 주입 (Dependency Injection)

의존성 주입(DI)은 FastAPI의 핵심 기능 중 하나입니다. 이번 레슨에서는 단순한 의존성을 넘어 실무에서 자주 발생하는 복잡한 상황들을 다룹니다.

## 1. Context에 따른 의존성 관리
실무에서는 요청(Request)의 상태나 유저의 역할에 따라 다른 의존성을 주입해야 할 때가 많습니다. 예를 들어, 다중 테넌트(Multi-tenant) 환경에서 어떤 테넌트의 DB에 접근해야 하는지를 의존성 주입 단계에서 동적으로 결정할 수 있습니다.

```python
from fastapi import Request, Depends

async def get_tenant_db(request: Request):
    tenant_id = request.headers.get("X-Tenant-ID")
    if not tenant_id:
        raise HTTPException(status_code=400, detail="Tenant ID is required")
    # 테넌트에 맞는 데이터베이스 세션을 반환하는 로직
    return setup_tenant_db(tenant_id)
```

## 2. 의존성 격리 (Dependency Isolation)
애플리케이션이 커질수록 계층(Layer)간 의존성을 어떻게 분리할지가 가장 중요해집니다. 라우터(Router) 계층은 서비스(Service) 계층에만 의존하게 하고, 서비스 계층은 저장소(Repository) 계층에만 의존하게 설정하는 방법을 설명합니다.

## 3. 테스트 환경에서의 의존성 오버라이드 (Override)
`app.dependency_overrides`를 활용하면 테스트 시 실제 데이터베이스 연결이나 외부 API 호출을 모의(Mock) 객체로 쉽게 대체할 수 있습니다. 테스트 격리성과 속도를 높이는 현업 필수 스킬입니다.
"""
            },
            {
                "title": "2. SQLAlchemy 2.0 비동기(Async) 처리와 Repository 패턴",
                "content": """# SQLAlchemy 2.0 비동기 데이터베이스 접근

FastAPI를 사용할 때 비동기 로직이 멈추는(Bocking) 현상을 방지하는 것은 웹서버 성능에 치명적일 정도로 중요합니다.

## 1. AsyncEngine과 AsyncSession 설정
기존 동기화 방식(`create_engine`) 대신 비동기 드라이버(`asyncpg` 등)와 함께 `create_async_engine`을 설정하는 방법을 상세히 다룹니다. 또한 `sessionmaker`에 `AsyncSession` 클래스를 바인딩하여 안전한 세션 라이프사이클을 관리하는 패턴을 배웁니다.

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+asyncpg://user:password@localhost/dbname"
engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)
```

## 2. Repository 패턴 구현하기
SQLAlchemy 코드를 라우터 함수 안에 직접 쓰게 되면 코드가 지저분해지고 재사용성이 떨어집니다. `Repository` 기반으로 코드를 리팩토링하여 데이터 접근 로직을 분리하는 실무 패턴을 적용해봅니다.

## 3. 고급 쿼리와 N+1 문제 해결 (selectinload, joinedload)
비동기 환경에서 SQLAlchemy의 릴레이션십을 잘못 호출하면 `MissingGreenletException` 등의 에러가 발생합니다. `selectinload`와 `joinedload`를 사용해 N+1 문제를 방지하며 미리 연관된 데이터를 비동기로 불러오는 노하우를 소개합니다.
"""
            },
            {
                "title": "3. 심화 보안: OAuth2 JWT 갱신(Refresh) 흐름과 RBAC",
                "content": """# 보안과 인증 인가 로직 고도화

기본적인 JWT 로그인에서 한 발 더 나아가 운영 환경에 필수적인 토큰 관리 및 권한 관리 시스템을 구현합니다.

## 1. Access Token과 Refresh Token의 분리 전략
액세스 토큰의 만료 시간을 짧게(예: 15분) 가져가고, `HttpOnly` 속성을 가진 쿠키에 리프레시 토큰을 저장하여 외부 탈취 렌인 XSS(Cross-site Scripting)를 방어하는 모범 사례를 적용해봅니다.

## 2. Token Blacklist / Refresh Token 레디스(Redis) 관리
유저가 로그아웃 하거나 계정이 정지되었을 때 해당 토큰의 효력을 즉시 정지시키는 메커니즘이 필요합니다. Redis를 인메모리 DB로 사용하여 유효한 리프레시 토큰 목록을 관리하고 검증하는 로직을 다룹니다.

## 3. 역할 기반 중앙 권한 접근 제어 (RBAC)
Dependency Injection을 이용해 단 1줄의 코드로 엔드포인트의 접근 권한을 관리할 수 있습니다. 예를 들어, `dependencies=[Depends(RoleChecker(["admin", "manager"]))]` 와 같이 유연하고 확장성 있는 권한 검사기를 직접 만들어봅니다.
"""
            },
            {
                "title": "4. 실시간 통신 및 스트리밍 (WebSockets & SSE)",
                "content": """# 실시간 통신 (WebSockets 및 Server-Sent Events)

알림 전송, 채팅, 또는 실시간 대시보드 업데이트 등 최신 웹에서 필수적인 실시간 통신을 FastAPI에서 구현하는 법을 알아봅니다.

## 1. WebSocket 커넥션 매니저 구현
수많은 클라이언트가 동시에 접속하는 상황에서 WebSocket 연결들을 어떻게 관리하고, Broadcast 메시지와 Whisper(개인) 메시지를 정확히 타겟팅하여 보낼 수 있는지 `ConnectionManager` 클래스를 작성하여 해결합니다.

```python
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)
```

## 2. Server-Sent Events (SSE) 도입
클라이언트에서 서버로 메시지를 보낼 필요는 없고, 서버에서 클라이언트로만 푸시 알림(Event Stream)이 필요한 경우 WebSocket 대신 더 가볍고 HTTP 통신 친화적인 SSE를 사용하는 것을 권장합니다. `StreamingResponse`와 제너레이터를 조합해 SSE를 완벽히 구현하는 법을 설명합니다.
"""
            },
            {
                "title": "5. 미들웨어(Middleware)와 애플리케이션 프로파일링",
                "content": """# 미들웨어 설계와 성능 최적화

백엔드 요청의 첫 관문이자 마지막 관문인 미들웨어를 심층 분석합니다.

## 1. Custom BaseHTTPMiddleware 작성
모든 API 요청의 처리 시간을 측정하거나 고유한 Request ID(Correlation ID)를 헤더에 주입하여 모니터링 로그를 연결하는 미들웨어를 직접 만들어봅니다.

## 2. Pyinstrument를 이용한 애플리케이션 프로파일링
코드가 왜 느린지 감에만 의존할 수 없습니다. 비동기 환경에서도 완벽히 작동하는 프로파일링 도구들을 연동하여 함수별 소요 시간 트리(Call Tree)를 확인하고, 병목점(Bottleneck)이 데이터베이스인지, 로직인지 아니면 외부 I/O 인지 찾아내는 방법을 배웁니다.

## 3. 실무적인 Rate Limiting (속도 제한)
DDoS 공격 방어나 API 남용을 막기 위해 Redis를 활용하여 "IP 또는 유저 ID별 1분당 최대 50회 요청 가능" 과 같은 Rate Limiter 시스템을 슬라이딩 윈도우 알고리즘을 이용해 구현합니다.
"""
            },
            {
                "title": "6. 프로덕션 레벨 배포 및 무중단 CI/CD",
                "content": """# 현업 수준의 완성도 높은 배포 전략

FastAPI 애플리케이션을 단순 서버가 아닌, 프로덕션 등급의 안정성을 갖추도록 배포하는 단계입니다.

## 1. Gunicorn과 Uvicorn의 조화로운 워커(Worker) 관리
단일 Uvicorn만 띄우는 것이 왜 실무에서 위험한지 이유를 살펴보고, Gunicorn을 프로세스 매니저로 사용하여 Uvicorn 워커들을 여러 개 관리하여 다중 CPU 코어를 100% 활용하는 방법을 설정합니다.

## 2. 최적화된 Dockerfile 작성 모범 사례
멀티 스테이지 빌드(Multi-stage build)를 활용해 이미지를 경량화하고, `poetry`나 `uv`와 같은 최신 패키지 매니저의 캐시 메커니즘을 극대화시켜 빌드 속도를 2배 이상 높이는 Dockerfile을 작성합니다.

## 3. GitHub Actions를 이용한 CI/CD 파이프라인
코드가 `main` 브랜치에 푸시되었을 때 자동으로 `pytest` 테스트를 통과하고, 빌드된 이미지를 레지스트리에 푸시한 후 원격 서버에 무중단(Zero-downtime) 배포로 롤링 업데이트하는 CI/CD 스크립트 작성법을 익힙니다.
"""
            }
        ]

        order = 1
        for lesson_data in lessons_data:
            lesson = Lesson(
                title=lesson_data["title"],
                content=lesson_data["content"],
                order=order,
                course_id=course.id
            )
            session.add(lesson)
            order += 1
        
        session.commit()
        print(f"총 {len(lessons_data)}개의 레슨이 성공적으로 생성되었습니다.")

if __name__ == "__main__":
    seed_fastapi_course()
