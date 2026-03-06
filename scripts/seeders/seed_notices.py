# -*- coding: utf-8 -*-
"""
공지사항 초기 데이터 생성 스크립트
"""
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from sqlmodel import Session, select
from core.database import engine, create_db_and_tables
from models import Notice

def seed_notices():
    create_db_and_tables()
    
    with Session(engine) as session:
        # 기존 공지사항 확인
        statement = select(Notice)
        existing_notices = session.exec(statement).all()
        
        if existing_notices:
            print(f"기존 공지사항 {len(existing_notices)}개가 있습니다.")
            return
        
        # 샘플 공지사항 생성
        sample_notices = [
            Notice(
                title="서비스 오픈 안내",
                content="""안녕하세요!

강좌 플랫폼 서비스가 오픈되었습니다.

본 플랫폼은 다음과 같은 기능을 제공합니다:
- 다양한 강좌 수강
- 실시간 강의 열람
- 관리자 페이지를 통한 강좌 관리

이용에 참고하시기 바랍니다.

감사합니다.""",
                is_pinned=True,
                is_active=True
            ),
            Notice(
                title="FastAPI 강좌 업데이트 완료",
                content="""FastAPI 실무 마스터 강좌가 대대적으로 업데이트되었습니다.

[변경 사항]
1. 총 10 개 레슨으로 구성
2. 기초부터 고급까지 체계적인 커리큘럼
3. 실전 예제 및 코드 샘플 대폭 추가
4. 테스트 작성법 추가

많은 관심과 수강 부탁드립니다.""",
                is_pinned=True,
                is_active=True
            ),
            Notice(
                title="정기 점검 안내",
                content="""안녕하세요.

시스템 정기 점검이 예정되어 있습니다.

[점검 일정]
- 일시: 2026 년 3 월 15 일 (일) 02:00 ~ 04:00
- 내용: 서버 성능 개선 및 보안 업데이트

점검 시간 동안 서비스 이용이 제한될 수 있습니다.
이용에 참고하시기 바랍니다.

감사합니다.""",
                is_pinned=False,
                is_active=True
            ),
        ]
        
        for notice in sample_notices:
            session.add(notice)
        
        session.commit()
        print(f"샘플 공지사항 {len(sample_notices)}개가 생성되었습니다.")


if __name__ == "__main__":
    seed_notices()
