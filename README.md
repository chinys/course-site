# Course Site (FastAPI)

이 프로젝트는 **Python FastAPI**, **SQLModel**, **Jinja2** 템플릿 엔진을 사용하여 새롭게 구축된 경량 강좌/강의 플랫폼입니다. 서버 사이드 렌더링(SSR)을 통해 프론트엔드와 백엔드를 통합하여 단일 서버 모델로 매끄럽게 동작하게 설계되었습니다.

## 🚀 주요 기술 스택

- **Backend Framework:** FastAPI
- **Database ORM:** SQLModel (SQLite 기반)
- **Dependency Management:** `uv`
- **Frontend / Styling:** Jinja2 템플릿, Tailwind CSS (CDN), Vanilla HTML/JS
- **Content Editor:** TinyMCE (cdnjs Open Source) WYSIWYG Editor
- **Authentication:** `bcrypt` (단방향 해시), `PyJWT` (HTTP-only 세션 쿠키 인증)

## 📁 주요 디렉터리 구조

- `main.py`: FastAPI 애플리케이션 진입점 및 라우터 마운트, 정적 파일(`static`) 서빙
- `core/`:
  - `database.py`: SQLite 연동 및 컨텍스트 매니저 기반 DB 세션 의존성 제공
- `models/`: 어플리케이션 데이터 스키마 정의 (`User`, `Course`, `Lesson`)
- `routers/`:
  - `auth.py`: JWT 및 쿠키 기반 관리자 인증 로그인/로그아웃 처리
  - `admin.py`: 강좌/강의 CRUD API 및 수정 렌더링, 관리자 대시보드 뷰
  - `public.py`: 사용자 공개 뷰 (메인, 상세, 강의 열람 렌더링)
- `scripts/`: 초기 DB 세팅 관리자 생성(`create_admin.py`) 및 더미 데이터(EPC, 철골, 철근 매뉴얼) 시딩 스크립트 모음
- `templates/`: Jinja2 서버 사이드 렌더링용 HTML 파일 모음 (`admin/`, `public/`)
- `static/`: 클라이언트 제공 정적 파일 (`uploads/` 경로에 강의용 이미지, 썸네일 탑재)

## 🛠 처음 시작하기 (Installation & Setup)

1. Python 3.12 이상 버전을 준비합니다.
2. 초고속 파이썬 패키지 매니저인 `uv`를 전역으로 설치합니다.
   * **Windows (Powershell):**
     ```powershell
     powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
     ```
   * **macOS / Linux (터미널):**
     ```bash
     curl -LsSf https://astral.sh/uv/install.sh | sh
     ```
3. 프로젝트 경로로 이동하여 의존성을 설치하고 가상 환경을 구축동기화합니다.
   ```bash
   cd d:\workai\course-site
   uv sync
   ```

## ⚙️ 관리자 계정 생성 (Database Seeding)

대시보드에 접근하기 위해서는 최초 관리자 계정이 필요합니다. 아래 명령을 통해 `database.db` 파일 생성과 더불어 기본 `ADMIN` 유저를 생성할 수 있습니다.
```bash
uv run python scripts/create_admin.py
```
*(기본 계정: `admin@example.com` / `password123`)*

## 🚀 실행하기 (Running the App)

아래 명령어를 통해 개발 서버를 구동합니다. `--reload` 옵션이 켜져 있으므로 코드를 수정하면 자동으로 재시작됩니다. (포트 접근 권한 충돌 시 3004 등 포트를 자유롭게 변경 가능합니다)
```bash
uv run uvicorn main:app --reload --port 3004
```

- **퍼블릭 뷰 접속:** [http://localhost:3004/](http://localhost:3004/)
- **어드민 로그인 접속:** [http://localhost:3004/admin/login](http://localhost:3004/admin/login)

## 📝 관리자 주요 기능

- **과정(Course) 관리**: 썸네일 업로드와 함께 새로운 강좌 묶음을 발행합니다. 작성된 데이터 및 업로드는 로컬 데이터베이스 및 `static/uploads/` 폴더에 각각 저장됩니다.
- **강의(Lesson) 추가**: TinyMCE가 삽입된 텍스트 에디터를 이용해 각 Course에 소속된 리치 텍스트 강의 내용을 작성하고 저장합니다. 작성 순서(Order)에 따라 사용자에게 노출됩니다.

## 🌟 최근 주요 업데이트 내역

- **관리자 로그인 편의성 (보안 강화)**: 관리자 로그인 폼에 쿠키를 활용한 **'아이디 저장(Remember ID)'** 및 세션 만료기간(JWT)을 30일로 연장하는 **'자동 로그인(Auto Login)'** 기능을 추가했습니다.

- **정적페이지 추가**: Github Pages 기능을 활용하여 바로 접속가능할 수 있도록 정적파일로 변환 후 업로드함 (루트에 index.html과 build 폴더 추가됨. 불필요할 경우 이것들만 지우면 원래 파일과 동일함)
- 접속주소 : [https://chinys.github.io/course-site/](https://chinys.github.io/course-site/)


