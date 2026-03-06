# Course Site - Scripts Manual

본 문서는 `course-site` 프로젝트의 데이터베이스 관리, 콘텐츠 업데이트, 문서 자동화 (DOCX), 정적 사이트 빌드에 사용되는 스크립트들의 구조와 사용법을 안내합니다.

---

## 📂 스크립트 디렉토리 구조

```
scripts/
├── update_all.bat          # 전체 파이프라인 자동화 (권장)
├── README.md               # 이 파일
│
├── seeders/                # DB 초기 데이터 등록
│   ├── seed_law_ultimate_pt1.py    # 건설법규 1-5 강
│   ├── seed_law_ultimate_pt2.py    # 건설법규 6-10 강
│   ├── seed_law_ultimate_pt3.py    # 건설법규 11-13 강
│   ├── seed_law_ultimate_pt4.py    # 건설법규 14 강 (계약서)
│   ├── seed_fastapi_course.py      # FastAPI 강좌
│   ├── seed_notices.py             # 공지사항 초기 데이터
│   └── append_basic_lessons.py     # 기존 강좌에 레슨 추가
│
├── db_tools/               # DB 유지보수 도구
│   ├── create_admin.py     # 관리자 계정 생성
│   ├── check_db.py         # DB 구조 및 무결성 검사
│   ├── get_categories.py   # 카테고리 목록 확인
│   ├── fix_db.py           # DB 스타일/설정 수정
│   └── replace_terms.py    # 법률 용어 일괄 치환
│
├── export_tools/           # 문서 변환 및 사이트 추출
│   ├── generate_docx.py    # 계약서 DOCX 파일 생성
│   ├── export_site.py      # 정적 사이트 빌드 (GitHub Pages)
│   └── _extract_db_content.py  # DB 콘텐츠 추출 (검증용)
│
├── media_tools/            # 미디어 에셋 관리
│   ├── download_image.py   # 이미지 다운로드
│   ├── move_image.py       # 이미지 정리/이동
│   └── create_fastapi_thumbnail.py  # FastAPI 썸네일 생성
│
└── templates/              # HTML 템플릿 모듈
    ├── _section_a.py       # 매매/가공 계약서
    ├── _section_b.py       # 임대차 계약서
    ├── _section_c.py       # 위임/위탁 계약서
    ├── _section_d.py       # 고용/위촉 계약서
    └── _section_e.py       # 운송 계약서
```

---

## 🚀 빠른 시작

### 1. 전체 업데이트 (권장)

**`update_all.bat`** 을 실행하면 모든 작업이 자동으로 처리됩니다:

```bat
cd scripts
update_all.bat
```

**자동으로 수행되는 작업:**
1. ✅ DB 업데이트 (건설법규 1-5 강)
2. ✅ 중복 레슨 자동 정리 (ID 유지)
3. ✅ 정적 사이트 빌드 (`build/` 폴더)

**생성되는 결과물:**
- `database.db` - 업데이트된 데이터베이스
- `build/` - GitHub Pages 용 정적 사이트
- `static/downloads/` - DOCX 계약서 파일들

---

## 📋 주요 스크립트 사용법

### DB 관리

#### 관리자 계정 생성
```bash
uv run python scripts/db_tools/create_admin.py
```
- 기본 계정: `admin@example.com` / `password123`

#### DB 구조 확인
```bash
uv run python scripts/db_tools/check_db.py
```

#### 카테고리 목록 확인
```bash
uv run python scripts/db_tools/get_categories.py
```

---

### 콘텐츠 업데이트

#### 건설법규 강좌 업데이트

**전체 업데이트 (권장):**
```bat
scripts\update_all.bat
```

**개별 실행:**
```bash
# 1-5 강
uv run python scripts/seeders/seed_law_ultimate_pt1.py

# 6-10 강
uv run python scripts/seeders/seed_law_ultimate_pt2.py

# 11-13 강
uv run python scripts/seeders/seed_law_ultimate_pt3.py

# 14 강 (계약서)
uv run python scripts/seeders/seed_law_ultimate_pt4.py
```

#### FastAPI 강좌 업데이트
```bash
uv run python scripts/seeders/seed_fastapi_course.py
```

#### 공지사항 생성
```bash
uv run python scripts/seeders/seed_notices.py
```

---

### 문서 변환

#### 계약서 DOCX 생성
```bash
uv run python scripts/export_tools/generate_docx.py
```
- 생성 위치: `static/downloads/contract_*.docx`
- 10 종 계약서 (A1-E1) + 매뉴얼 지침

---

### 정적 사이트 빌드

```bash
uv run python scripts/export_tools/export_site.py
```
- 출력 폴더: `build/`
- GitHub Pages 에 푸시하여 배포

---

## 🔧 고급 사용법

### DB 레슨 ID 변경 (special case)

레슨 ID 를 일괄 변경해야 할 경우:

```bash
# 예: 91-104 → 42-55
uv run python scripts/db_tools/change_law_lesson_ids.py
```

### 중복 레슨 정리

중복 생성된 레슨을 정리할 경우:

```bash
uv run python scripts/db_tools/cleanup_law_lessons.py
```

### 법률 용어 일괄 치환

```bash
uv run python scripts/db_tools/replace_terms.py
```

---

## ⚠️ 중요 주의사항

### 1. ID 유지 원칙

**`update_all.bat`** 은 다음을 보장합니다:
- ✅ 레슨 ID 변경 안 됨
- ✅ 중복 생성 안 됨
- ✅ 링크 깨짐 없음

**개별 스크립트 실행 시 주의:**
- `seed_law_ultimate_pt1.py` 만 사용 (pt2-pt4 는 중복 생성 가능)
- 반드시 `cleanup_law_lessons.py` 를 함께 실행

### 2. 경로 규칙

모든 스크립트는 **프로젝트 루트** 기준입니다:

```bash
# ✅ 올바른 방법
cd d:\workai\course-site
uv run python scripts/seeders/seed_law_ultimate_pt1.py

# ❌ 잘못된 방법 (상대 경로 오류)
cd scripts/seeders
python seed_law_ultimate_pt1.py
```

### 3. 템플릿 변경 시

`templates/_section_*.py` 수정 후:

```bat
scripts\update_all.bat
```

이렇게 하면:
- DB 자동 업데이트
- DOCX 자동 재생성
- 정적 사이트 자동 빌드

---

## 📝 파일 정리 가이드

### 삭제해도 되는 파일

- `_*.py` - 임시/테스트용 (언더스코어로 시작)
- `*_fixed.py`, `*_keep_id.py` - 개발 중간 파일
- `*.txt` - 로그/덤프 파일

### 유지해야 할 파일

- `seed_law_ultimate_pt[1-4].py` - 건설법규 강좌
- `seed_fastapi_course.py` - FastAPI 강좌
- `export_site.py` - 정적 사이트 빌드
- `generate_docx.py` - DOCX 생성

---

## 🐛 문제 해결

### Q1. 레슨 ID 가 바뀌었어요

**원인:** `DELETE` 후 `INSERT` 하는 스크립트 사용

**해결:**
```bash
# 1. ID 재설정
uv run python scripts/db_tools/change_law_lesson_ids.py

# 2. 앞으로는 update_all.bat 만 사용
scripts\update_all.bat
```

### Q2. 중복 레슨이 생겼어요

**해결:**
```bash
uv run python scripts/db_tools/cleanup_law_lessons.py
```

### Q3. 정적 사이트에서 링크가 깨져요

**해결:**
```bash
# DB 정리 후 재빌드
uv run python scripts/db_tools/cleanup_law_lessons.py
uv run python scripts/export_tools/export_site.py
```

---

## 📚 관련 문서

- [프로젝트 루트 README.md](../README.md) - 전체 프로젝트 개요
- [GitHub Pages 배포 가이드](../GITHUB_GUIDE.md) - 정적 사이트 배포

---

**마지막 업데이트:** 2026-03-06
