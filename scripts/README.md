# Course Site - Scripts Manual

본 문서는 `course-site` 프로젝트의 데이터베이스 초기화 및 유지보수, 그리고 문서 자동화(DOCX, HTML 파싱), 정적 사이트 빌드에 사용되는 스크립트들을 체계적으로 분류하고 그 작동 방식 및 사용법을 안내하는 매뉴얼입니다.

---

## 📂 스크립트 디렉토리 구조 및 분류

스크립트 폴더는 목적별로 안전하고 효율적인 관리가 가능하도록 하위 디렉토리로 분리되어 있습니다.

### 1. `seeders/` (초기 데이터 등록/동기화 스크립트)
강의(Course) 및 각 레슨(Lesson), 기타 핵심 콘텐츠 데이터를 DB에 밀어넣는 역할을 담당합니다.
- **`seed_law_ultimate_pt1.py` ~ `pt4.py`**: 건설법무 심화 강의 등의 섹션별 콘텐츠 DB Insert 스크립트. (특히 `pt4.py`는 실무 핵심 양식 계약서 모음을 등록합니다.)
- **`seed_fastapi_course.py`**, **`expand_fastapi_course.py`**: FastAPI 강의 콘텐츠용 DB Seeder 스크립트.
- **`append_basic_lessons.py`**: 기존 강좌에 새 레슨을 이어붙일 때 사용하는 스크립트.
- **`_update_seeds.py`**: 시드 데이터 전체를 일괄 재적용하거나 갱신하는 헬퍼.

### 2. `templates/` (HTML/계약서 템플릿 모듈)
파이썬 내에서 계약서 양식 및 매뉴얼 지침의 HTML 블록을 생성해 반환하는 모듈입니다. 다른 폴더(seeders, export_tools)에서 Import하여 사용합니다.
- **`_section_a.py` ~ `_section_e.py`**: 민법상 계약 유형(매매/가공, 임대차, 위임, 고용, 운송)에 따른 건설 실무 특화 계약서 양식들의 설계 템플릿.

### 3. `db_tools/` (데이터베이스 유지보수 및 점검)
생성된 DB(.db)의 정합성을 검증하거나 특정 텍스트를 일괄 수정하고 관리자 계정을 추가하는 관리 유틸리티입니다.
- **`check_db.py`**: 데이터베이스 내 구조 시각화 및 무결성 검사.
- **`fix_db.py`**, **`fix_law_bg.py`**: DB 내 누락된 강의 테이블의 배경색, 태그, 설정값 등을 업데이트.
- **`get_categories.py`**: 현재 정의된 카테고리 구성 확인.
- **`create_admin.py`**: 관리자 시스템 로그인용 User 계정 생성.
- **`replace_terms.py`**, **`replace_terms2.py`**: 법률 용어/표현이 대대적으로 바뀔 때 DB의 `content` 컬럼을 정규식 등으로 일괄 변환.

### 4. `export_tools/` (문서 변환 및 파일/사이트 추출)
DB에 저장된 HTML 형태의 교재/자료들을 유저 배포용 산출물(DOCX)로 변환하거나, 정적 웹 호스팅을 위한 빌드를 수행합니다.
- **`generate_docx.py`**: `templates/_section_*.py` 내용을 불러와 동적으로 Word(`contract_*.docx`) 파일로 컴파일하여 `static/downloads/` 폴더에 생성합니다. (HTML 파싱 알고리즘 포함)
- **`_extract_db_content.py`**: 특정 Lesson의 코드를 터미널 및 임시 txt 파일에 덤프하여 정합성을 맨눈으로 확인할 수 있게 합니다.
- **`export_site.py`**: 동적 FastAPI 사이트를 크롤링하여 GitHub Pages 등 호스팅용 정적 HTML/CSS 웹사이트 폴더(`build/`)로 컴파일합니다.

### 5. `media_tools/` (미디어 및 에셋 관리)
외부 URL의 썸네일/사진을 다운로드하거나 재배치할 때 사용하는 스크립트입니다.
- **`download_image.py`**: 웹에서 임시 이미지를 서버 로컬 스토리지로 캡처 다운로드.
- **`move_image.py`**: 다운로드한 로컬 이미지를 웹 Root 스태틱 폴더 구조에 맞게 복사/재배치.

---

## 🚀 파이프라인 자동화: `update_all.bat`

유지보수를 하다 보면, 템플릿의 문구를 수정하거나 DB를 재갱신한 후 DOCX를 다시 컴파일하고 사이트를 내보내야 하는 연속적인 수작업이 강제됩니다. 
이를 자동화하기 위하여 모든 메인 파이프라인을 관장하는 안전망으로서 **`update_all.bat`**를 이용합니다.

#### 실행 절차 (한 번의 클릭)
1. DB Seeding 갱신 (법무 심화 강의의 변경사항 적용 등)
2. 확인용 TXT Content Extraction (DB가 온전히 저장되었는지 결과 출력)
3. DOCX 파일 자동 재생성 (`templates/`의 디자인/서명란 변경점 반영)
4. Static 파일 변환 및 Build 폴더 적용

#### 사용 방법
```bat
cd scripts
update_all.bat
```
이 스크립트는 내부적으로 `cd /d "%~dp0.."` 을 통해 프로젝트 루트(course-site)로 경로를 포착하고 `uv run python` 명령어로 환경 변수 분리 없이 안전하게 일괄 실행합니다. (파이썬 인코딩 깨짐을 방지하기 위해 `PYTHONIOENCODING=utf-8`이 세팅되어 있습니다.)

---

## 🛠️ 개발/유지보수 시 유의사항
- **템플릿 변경:** 계약서 내용(갑/을 위치, 표 내용 추가, 문구 수정)을 변경하려면 `templates/_section_X.py`만 수정하십시오. 그 후 `update_all.bat`만 실행하면 DB 업데이트와 워드 다운로드 파일 재생성이 한 번에 끝납니다.
- **DOCX 스타일 파싱 규칙:** HTML 표를 Word로 바꿀 때 `<br>`은 줄바꿈으로, `p` 등 블록 태그는 파이썬에서 정규식을 통해 문서 단락으로 치환됩니다. 간격 등 양식 파싱 디테일을 세부 조정하실 때는 `export_tools/generate_docx.py`의 `_strip`과 `_add_word_table` 로직을 조절하세요.
- **경로 의존성:** 모든 스크립트는 상대 경로 탐색 시 해당 파이썬 파일 기준이 아니라 **프로젝트 루트 디렉토리** 위주로 동작하도록 설계되어 있습니다. 개별 파일을 실행할 때도 루트 디렉토리에서 `uv run python scripts/폴더/스크립트.py` 형식으로 실행하시길 권장합니다.
