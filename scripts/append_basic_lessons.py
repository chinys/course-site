import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from sqlmodel import Session, select
from core.database import engine
from models import Course, Lesson

def append_basic_lessons():
    with Session(engine) as session:
        statement = select(Course).where(Course.title.like("%FastAPI%"))
        course = session.exec(statement).first()
        
        if not course:
            print("강좌를 찾을 수 없습니다.")
            return

        # 기존 레슨들 가져오기
        existing_lessons = session.exec(
            select(Lesson).where(Lesson.course_id == course.id).order_by(Lesson.order)
        ).all()
        
        # 만약 기존 레슨이 6개라면, 이들의 순서(order)를 5씩 뒤로 다 밀어버린다.
        # (이미 11개가 넘어간다면 스크립트가 여러번 실행된 것이므로 중단)
        if len(existing_lessons) > 6:
            print("이미 기초 강좌가 추가되어 있거나 예상보다 레슨이 많습니다.")
            return
            
        print("기존 심화 레슨 6개의 목차 순서를 6~11강으로 1칸씩 미루는 중...")
        # 기존 제목도 "1. ~" 에서 "6. ~" 로 수정을 시도하거나, 혹은 번호를 붙이지 않고 그대로 둘 수 있다.
        # 심화 강좌들의 제목 앞에 붙은 "1. " 형태의 숫자를 +5 해 준다.
        for idx, lesson in enumerate(existing_lessons):
            lesson.order += 5
            # 예: "1. FastAPI 고급 의존성..." -> "6. FastAPI 고급 의존성..."
            import re
            new_title = re.sub(r"^\d+\.", f"{lesson.order}.", lesson.title)
            lesson.title = new_title
            session.add(lesson)
            
        session.commit()

        # 새로운 1~5 기초 레슨 데이터 준비
        basic_lessons_data = [
            {
                "title": "1. FastAPI 입문: ASGI와 프레임워크의 탄생 배경",
                "content": """# 1강. FastAPI 소개와 "Hello, World!" 만들기

본격적인 실무 아키텍처를 다루기 전에, FastAPI가 왜 현재 파이썬 생태계에서 가장 주목받는 웹 프레임워크인지, 그리고 가장 기초적인 뼈대를 어떻게 세우는지 학습합니다.

---

## FastAPI의 탄생 배경과 철학
기존 파이썬의 표준 웹 기술은 **WSGI (Web Server Gateway Interface)**를 따르고 있었습니다. Django와 Flask가 대표적입니다. 하지만 이들은 "동기(Synchronous)" 방식이었기 때문에 1개의 요청이 끝나기 전까지 쓰레드가 멈춰있어야 했고, 대규모 트래픽 앞에서는 Node.js나 Go 언어에 밀려 심각한 성능 저하를 겪었습니다.

이를 극복하기 위해 나타난 비동기 표준이 **ASGI (Asynchronous Server Gateway Interface)**입니다.
FastAPI는 이 ASGI 표준을 따르는 **Starlette**과 빠르고 정교한 데이터 검증 라이브러리인 **Pydantic**을 결합하여 탄생했습니다.

1. 파이썬 세계에서 가장 빠른 속도 중 하나 (Node.js/Go와 대등한 수준)
2. 버그의 40%를 줄이는 자동화된 타입 힌팅(Type Hinting)
3. Swagger / ReDoc API 문서 100% 자동 생성

이 3가지가 프레임워크의 핵심 철학입니다.

---

## 2. 첫 프로젝트 셋업과 uvicorn 실행

FastAPI는 파이썬 3.8 이상부터 지원하는 `Type Hints`를 cực대화합니다.
개발을 시작하려면 프레임워크와 비동기 웹서버(`uvicorn`)를 설치해야 합니다.

```bash
pip install fastapi "uvicorn[standard]"
```

그 후 `main.py`에 아주 단순한 라우터를 작성해 봅시다.

```python
from fastapi import FastAPI

# 1. FastAPI 인스턴스 생성
app = FastAPI(title="My First API", description="Hello World 예제입니다.")

# 2. 경로 연산(라우팅) 데코레이터
@app.get("/")
def read_root():
    # 파이썬 딕셔너리를 리턴하면 자동으로 JSON으로 변환해 줌
    return {"message": "Hello, FastAPI World!"}
```

이제 터미널에서 아래 명령어로 서버를 가동합니다.

```bash
uvicorn main:app --reload
```
* `main`: `main.py` 파일 이름
* `app`: `FastAPI()` 인스턴스 변수명
* `--reload`: 코드가 변경될 때마다 서버를 즉시 자동 재시작해주는 개발용 꿀 옵션 (운영에서는 절대 금지)

---

## 3. 자동 문서화의 마법 (Swagger UI)

서버가 켜졌다면 브라우저를 열고 다음 주소에 접속해 보십시오.
* **`http://127.0.0.1:8000/docs`**

Swagger UI가 등장하면서, 방금 만든 API를 클릭 한 번으로 테스트(Try it out) 해 볼 수 있는 대시보드가 자동으로 생겨났습니다!
이는 코드에 적은 데이터 타입(Type hints)을 기반으로 OpenAPI 스키마(JSON)를 FastAPI가 동적으로 렌더링해 둔 결과물입니다. 프론트엔드 개발자와 소통할 때 더이상 별도의 문서화 작업에 시간을 낭비할 필요가 없습니다. 
"""
            },
            {
                "title": "2. 경로 매개변수(Path)와 쿼리 스트링(Query)",
                "content": """# 2강. 사용자 입력을 주소창에서 받기 (Path & Query parameter)

클라이언트가 서버로 무언가를 요구(Request)할 때, 그 요구사항을 URL을 통해 전달하는 방식은 크게 두 가지가 있습니다. 
이번 레슨에서는 라우팅 심화 기법을 완벽히 정복합니다.

---

## 1. 경로 매개변수 (Path Parameter)

데이터베이스의 특정 자원(Resource) 하나를 콕 집어내고 싶을 때 사용합니다.
중괄호 `{ }` 문법을 사용해 경로에 변수를 지정합니다.

```python
from fastapi import FastAPI

app = FastAPI()

# URL 예시: /users/42
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"requested_user_id": user_id, "status": "active"}
```

**FastAPI의 진가: 자동 타입 변환 및 체킹**
위 코드에서 `user_id`를 파이썬 내장 타입인 `int`로 선언했습니다.
만약 사용자가 `http://127.0.0.1:8000/users/hello` 라고 문자열을 입력하면 어떻게 될까요?
여러분이 따로 검사 코드를 짜지 않아도, FastAPI가 즉각 알아채고 HTTP `422 Unprocessable Entity` 에러 메시지와 함께 `"input should be a valid integer"` 라는 친절한 안내를 자동으로 뱉어줍니다! 이것이 Pydantic 코어가 적용된 `Type Hinting`의 위력입니다.

---

## 2. 쿼리 매개변수 (Query Parameter)

URL의 끝에 `?` 마크 뒤에 붙어오는 `key=value` 쌍을 쿼리 매개변수라고 부릅니다. 보통 검색(Search), 정렬(Sort), 페이징(Pagination) 조건들을 전달할 때 사용합니다.

FastAPI에서는 라우터 경로(path) `{ }` 안에 포함되지 않은 함수의 매개변수는 무조건 **쿼리 매개변수**로 취급합니다.

```python
# URL 예시: /items?skip=20&limit=5
@app.get("/items")
def list_items(skip: int = 0, limit: int = 10, search_keyword: str | None = None):
    # skip과 limit은 기본값(Default)을 가졌으므로 선택 사항(Optional)입니다.
    return {
        "skip": skip,
        "limit": limit,
        "search": search_keyword
    }
```
만약 `/items` 라고만 입력하면, FastAPI는 알아서 `skip=0`, `limit=10`을 할당해 줍니다. 
반면 `search_keyword`는 사용자가 입력하지 않으면 파이썬의 `None` 값이 들어가도록 `| None` (파이썬 3.10+ 문법) 표기를 통해 **선택적 값**임을 명시했습니다.

---

## 3. Path() 와 Query() 를 통한 고급 유효성 검사

단순히 `int`냐 `str`이냐 구별하는 것만으로는 부족할 때가 있습니다. "검색어의 길이가 최대 50자를 넘지 않게 해줘", "출력할 아이템 개수는 무조건 1개에서 100개 사이여야 해" 같은 세밀한 정책이 필요합니다.
이때 FastAPI가 제공하는 `Path`와 `Query` 클래스를 사용합니다.

```python
from fastapi import FastAPI, Path, Query
from typing import Annotated

app = FastAPI()

@app.get("/articles/{article_id}")
def read_article(
    article_id: Annotated[int, Path(title="기사 ID", ge=1)],
    q: Annotated[str | None, Query(max_length=50, alias="search-query")] = None
):
    return {"id": article_id, "query": q}
```
* `ge=1`: Greater than or equal to 1. 0이나 음수가 들어오면 곧바로 에러 처리!
* `max_length=50`: 글자 수 50자 제한.
* `alias="search-query"`: 파이썬 변수명에는 대시(-)를 쓸 수 없지만, URL에는 `?search-query=fastapi` 처럼 대시를 적용하고 싶을 때 쓰는 유용한 기법입니다.
"""
            },
            {
                "title": "3. Pydantic을 이용한 Request Body와 데이터 검증",
                "content": """# 3강. 복잡한 데이터 다루기 Request Body (JSON)

주소창의 한계를 넘어, 새 사용자를 가입시키거나 거대한 문서를 저장해야 할 때 클라이언트는 데이터를 **요청 본문(Request Body)**의 JSON 형태로 서버에 전송합니다.
과거 프레임워크들은 이 JSON을 일일이 파싱(Parsing)하고 필수값이 다 있는지 `if`문으로 떡칠하며 검사해야 했습니다. FastAPI는 이를 **Pydantic** 모델 단 하나로 완벽히 해결합니다.

---

## 1. Pydantic 기본 모델 정의하기

어떤 형태의 JSON이 들어와야 하는지를 파이썬 `class`로 정의합니다. 이 클래스는 반드시 `pydantic.BaseModel`을 상속받아야 합니다.

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# 1. Pydantic 모델 선언
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

# 2. 라우터에 타입 힌트로 주입
@app.post("/items/")
def create_item(item: Item):
    # item은 딕셔너리가 아닌 'Item' 클래스 인스턴스입니다!
    item_dict = item.model_dump() # dict 형태로 변환
    
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
        
    return item_dict
```

**자동 검사의 축복**
만약 사용자가 `{"name": "Laptop", "tax": 1.5}` 만 보낸다면? 필수값인 `price`가 누락되었음을 감지하고, "price 필드가 누락되었습니다"라는 에러를 즉각 반환합니다. 개발자는 오직 비즈니스 로직(부가세 계산 등)에만 집중할 수 있게 됩니다.

---

## 2. Pydantic Field를 이용한 세밀한 조건 설정

`Path`, `Query` 처럼 JSON 내부 필드 단위로도 강력한 유효성 검사가 필요합니다.
Pydantic의 `Field` 클래스를 통해 정규표현식, 값의 범위 제한 등을 선언합니다.

```python
from pydantic import BaseModel, Field

class UserSignup(BaseModel):
    username: str = Field(..., min_length=3, max_length=15, pattern="^[a-zA-Z0-9_-]+$")
    age: int = Field(..., ge=14, description="가입은 14세 이상만 가능합니다.")
    bio: str | None = Field(None, max_length=300)
```
* `...` 표기는 이 필드가 "필수값(Required)" 임을 뜻하는 엘립시스(Ellipsis) 관용구입니다 (요즘은 생략 후 타입을 곧바로 써도 필수값으로 인식합니다).
* `pattern`: 정규 표현식을 사용해 영문과 숫자, 그리고 언더바/대시만 닉네임에 허용합니다.

---

## 3. 중첩된 계층 구조 (Nested Models)

JSON은 1차원이 아니라 딕셔너리 안에 리스트가 있고, 그 리스트 안에 또 딕셔너리가 있는 다차원 트리 구조입니다.
이를 검증하기 위해 Pydantic 모델을 레고 블록 조립하듯 서로 끼워 넣습니다.

```python
from pydantic import BaseModel

class Image(BaseModel):
    url: str
    name: str

class Product(BaseModel):
    name: str
    price: float
    tags: set[str] = set() # 중복 없는 태그 리스트
    images: list[Image] | None = None # 모델 안에 모델(Image)을 감쌌습니다!

@app.put("/products/{product_id}")
def update_product(product_id: int, product: Product):
    return {"product_id": product_id, "product": product}
```
이로써 아래와 같은 복잡한 계층 구조 JSON도 단 0.1초 만에 유효성 검사가 자동 통과되며 파이썬 객체로 딱 떨어집니다!

```json
{
    "name": "Super Laptop",
    "price": 999.99,
    "tags": ["electronics", "computers"],
    "images": [
        {
            "url": "http://example.com/front.jpg",
            "name": "Front view"
        },
        {
            "url": "http://example.com/back.jpg",
            "name": "Back view"
        }
    ]
}
```
"""
            },
            {
                "title": "4. Response Models (응답 객체)와 HTTP 상태 코드",
                "content": """# 4강. 서버의 대답 모양 결정하기 (Response Model & Status Codes)

지금까지는 클라이언트로부터 데이터를 **어떻게 안전하게 받을 것인가**(Request)에 집중했습니다.
이번에는 서버가 클라이언트에게 **어떻게 안전하고 명확하게 데이터를 줄 것인가**(Response)에 대해 학습합니다.

---

## 1. Response Model (응답 모델 지정하기)

데이터베이스에서 유저 정보를 꺼내 클라이언트에게 전달한다고 가정해봅니다.
`UserInDB` 객체에는 비밀번호(Password)나 개인정보가 포함되어 있습니다. 코드를 짜다 실수로 `return user_in_db` 해버리면 큰 보안 사고가 터집니다!

FastAPI는 출력할 데이터의 구조를 제한하고 보호하는 `response_model` 기능을 라우터 데코레이터 단에서 지원합니다.

```python
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()

# 1. DB에서 꺼내올 형태 (민감한 데이터 포함)
class UserInDB(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None

# 2. 클라이언트에게 노출할 형태 (비밀번호 제외)
class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None

# 3. 라우터에 response_model 매개변수로 지정!
@app.post("/users/", response_model=UserOut)
def create_user(user: UserInDB):
    # (내부 로직) DB에 사용자 정보를 저장하는 과정...
    
    # 실수로 비밀번호가 포함된 객체를 그대로 리턴해도, 
    # FastAPI가 UserOut 마스크를 씌워 password 필드를 '자동으로 걸러낸(Filter)' 뒤 전송합니다!
    return user
```
이 기능은 보안 누수를 강력하게 방지하며, 동시에 Swagger UI 문서에 서버가 어떤 모양으로 데이터를 응답할지(Schema) 100% 명확하게 박제해줍니다.

---

## 2. HTTP 상태 코드 제어 (Status Codes)

웹 표준에서 HTTP 상태 코드는 매우 중요한 의사소통 수단입니다.
기본적으로 FastAPI는 정상 응답으로 `200 OK`를 리턴하지만, 데이터를 "새로 생성(Create)" 했을 때는 `201 Created`를, 내용을 깔끔히 비웠을 때는 `204 No Content`를 내리면 훨씬 훌륭한 API가 됩니다.

가장 쉬운 방법은 데코레이터의 `status_code` 파라미터를 조작하는 것입니다.
```python
from fastapi import FastAPI, status

app = FastAPI()

# 201 상태코드 상수를 활용하여 명시적 의미 전달
@app.post("/items/", status_code=status.HTTP_201_CREATED)
def create_item(name: str):
    return {"name": name, "message": "새 아이템이 성공적으로 생성되었습니다!"}
```
파이썬에는 `fastapi.status` 모듈 안에 모든 HTTP 상태 코드들이 보기 좋은 상수(Constant)로 정의되어 있습니다. (`status.HTTP_404_NOT_FOUND` 등). 외울 필요 없이 자동완성을 활용하세요.

---

## 3. 동적 Response 응답 (JSONResponse)

응답 모델(`response_model`) 속성에 갇히지 않고, 비즈니스 로직 도중 동적으로 응답 헤더(Headers)나 상태 코드를 바꾸고 싶을 때가 있습니다. (예: 쿠키(Cookies)를 구워주거나 커스텀 헤더를 전송할 때). 이 땐 `Response` 객체 구조체를 임포트해서 다룹니다.

```python
from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/legacy-login")
def legacy_login(response: Response):
    # 직접 헤더나 쿠키 조작
    response.set_cookie(key="fakesession", value="fake-cookie-session-value")
    response.headers["X-Custom-Header"] = "Go to new login API!"
    
    # 본문 데이터 출력
    return {"message": "You are logged in."}

# 처음부터 JSONResponse 클래스로 응답을 말아서 던지는 방법
@app.get("/custom-response")
def custom_json_response():
    data = {"system_status": "Healthy"}
    return JSONResponse(content=data, status_code=status.HTTP_202_ACCEPTED, headers={"X-Error": "None"})
```
"""
            },
            {
                "title": "5. 예외 처리(Error Handling)와 폼 데이터(Form/Upload)",
                "content": """# 5강. 에러 다루기와 고급 입력 방식 (Error Handling & Form Data)

비즈니스 로직을 짜다 보면 무수한 에러(아이디 중복, 잔액 부족, 권한 차단)들이 발생합니다.
또한 JSON이 아닌 구식 `multipart/form-data` 나 파일 업로드(File Upload)를 처리해야 하는 케이스도 실무에 빈번합니다. 이 두 가지를 완벽하게 통제해 보겠습니다.

---

## 1. 정석적인 예외 던지기: HTTPException

FastAPI는 에러 로직을 마주쳤을 때 파이썬 내장 `Exception` 이 아니라, 웹용 규격인 `HTTPException`을 일으키게(`raise`) 설계되었습니다.

```python
from fastapi import FastAPI, HTTPException

app = FastAPI()

items_db = {"1": "Laptop", "2": "Mouse"}

@app.get("/items/{item_id}")
def read_item(item_id: str):
    if item_id not in items_db:
        # 이 코드를 마주친 즉시 로직이 중단되고 404 에러와 JSON 메시지가 클라이언트에 날아갑니다.
        raise HTTPException(
            status_code=404, 
            detail="요청하신 아이템을 찾을 수 없습니다."
        )
    return {"item": items_db[item_id]}
```

여기에 사용자 정의 헤더를 추가해서 에러와 함께 보낼 수도 있습니다. (예: 인증 실패 시 인증 스킴(`Bearer`)을 같이 보내야 하는 규약이 있을 때).

---

## 2. 전역 예외 처리기 (Custom Exception Handlers)

어느 라우터에서 `UserNotFound` 라는 커스텀 에러 클래스가 터졌든 간에, 중앙에서 하나의 일관된 포맷(예: 사내 표준 에러 포맷 `{"code": "ERR_001", "msg": "..."}`)으로 포장(Wrapping)해서 내보내고 싶다면 как할까요?

**전역 예외 처리기에 함수를 등록**해 두면 됩니다.

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name

# UnicornException 클래스가 앱 내 어디서든 터지면 무조건 이 함수가 캐치합니다!
@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=418,  # I'm a teapot
        content={"message": f"이런! {exc.name} 유니콘이 말썽을 부리고 있군요."}
    )

@app.get("/unicorns/{name}")
async def read_unicorn(name: str):
    if name == "yolo":
        # 그냥 파이썬 에러를 발생시킴
        raise UnicornException(name=name)
    return {"unicorn_name": name}
```

---

## 3. 웹사이트의 터줏대감: 폼 데이터(Form Data) 수신

기존 웹사이트의 간단한 `<form>` 제출(로그인 태그 등)은 JSON이 아닌 `application/x-www-form-urlencoded` 타입을 던집니다.
이를 처리하려면 별도 패키지인 `python-multipart` 가 설치되어 있어야 합니다. (`pip install python-multipart`)

그리고 `Form` 이라는 특별한 디펜던시 마커를 사용합니다.

```python
from fastapi import FastAPI, Form

app = FastAPI()

@app.post("/login/")
async def login(username: str = Form(...), password: str = Form(...)):
    # Swagger에서 실행해 보면 JSON 입력칸이 아니라 폼(인풋 박스) 입력칸으로 바뀐 것을 볼 수 있습니다.
    return {"username": username, "status": "Form Data Received"}
```

---

## 4. 파일 업로드 (UploadFile과 File)

사용자의 프로필 이미지, 엑셀 문서 등을 서버에 업로드 받는 것은 현대 웹의 알파이자 오메가입니다.
FastAPI는 파이썬 비동기 철학에 걸맞게 `UploadFile` 이라는 아주 똑똑한 클래스를 지원합니다. (메모리에 다 올리지 않고 청크스트림으로 임시 파일 스풀링(Spooling)을 하여 서버가 뻗는 걸 방지함).

```python
from fastapi import FastAPI, File, UploadFile
import shutil

app = FastAPI()

@app.post("/uploadprofile/")
async def upload_profile_image(file: UploadFile = File(...)):
    # 1. 업로드된 파일의 메타데이터 확인
    file_name = file.filename
    content_type = file.content_type
    
    # 2. 이미지 파일만 허용하기 (간단한 예시)
    if not content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only images are allowed!")
        
    # 3. 서버 하드 디스크에 파일 비동기 혹은 스플릿 안전 저장하기
    with open(f"uploaded_{file_name}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    return {
        "info": f"파일 {file_name} 이 안전하게 서버에 저장되었습니다."
    }
```
여기까지 기초 코스를 수료하신 것을 축하합니다! 
FastAPI의 라우터, 입력(Request), 출력(Response), 예외처리, 파일 업로드를 마스터했으니, 
이제 6강부터 시작되는 진짜 실무, "엔터프라이즈 레벨의 아키텍처"를 구축하는 험난한 여행을 떠날 준비가 되셨을 겁니다. 화이팅!
"""
            }
        ]

        # 1. 1~5레슨을 순서대로 추가한다
        for idx, lesson_data in enumerate(basic_lessons_data):
            order = idx + 1
            new_lesson = Lesson(
                title=lesson_data["title"],
                content=lesson_data["content"],
                order=order,
                course_id=course.id
            )
            session.add(new_lesson)
            
        session.commit()
        print("훌륭합니다! 5개의 기초 레슨이 성공적으로 앞에 추가되었습니다. 기존 강좌들은 6~11강으로 밀려났습니다.")

if __name__ == "__main__":
    append_basic_lessons()
