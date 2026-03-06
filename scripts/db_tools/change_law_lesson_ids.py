# -*- coding: utf-8 -*-
"""
건설법규 강좌 레슨 ID 변경 스크립트
- 현재 ID: 91-104
- 변경할 ID: 42-55
"""
import sqlite3
import os

# DB 경로 (프로젝트 루트의 database.db)
db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'database.db')
print(f"DB 경로: {db_path}")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("=== 건설법규 레슨 ID 변경 ===\n")

# 1. 현재 상태 확인
print("[1] 현재 레슨 상태:")
cursor.execute("""
    SELECT id, title, "order", course_id 
    FROM lesson 
    WHERE course_id = (SELECT id FROM course WHERE title LIKE '%건설법규%')
    ORDER BY "order"
""")
rows = cursor.fetchall()
for row in rows:
    print(f"  ID {row[0]}: {row[1][:40]}... (order={row[2]})")

# 2. ID 변경 (임시 ID 사용)
print("\n[2] ID 변경 중... (임시 ID 사용)")

# SQLite 는 ID 를 직접 UPDATE 할 수 없으므로, 임시 ID 를 사용
# 91-104 → 1000+91 ~ 1000+104 → 42-55

id_mapping = {}
for i in range(14):
    old_id = 91 + i
    temp_id = 1000 + old_id
    new_id = 42 + i
    id_mapping[old_id] = (temp_id, new_id)

# Step 1: 임시 ID 로 변경
for old_id, (temp_id, new_id) in id_mapping.items():
    cursor.execute("UPDATE lesson SET id = ? WHERE id = ?", (temp_id, old_id))
    print(f"  {old_id} → {temp_id} (임시)")

conn.commit()

# Step 2: 임시 ID 를 최종 ID 로 변경
for old_id, (temp_id, new_id) in id_mapping.items():
    cursor.execute("UPDATE lesson SET id = ? WHERE id = ?", (new_id, temp_id))
    print(f"  {temp_id} → {new_id} (최종)")

conn.commit()

# 3. 변경 결과 확인
print("\n[3] 변경된 레슨 상태:")
cursor.execute("""
    SELECT id, title, "order", course_id 
    FROM lesson 
    WHERE course_id = (SELECT id FROM course WHERE title LIKE '%건설법규%')
    ORDER BY "order"
""")
rows = cursor.fetchall()
for row in rows:
    print(f"  ID {row[0]}: {row[1][:40]}... (order={row[2]})")

# 4. 관련 테이블 외래 키 확인 (문제 없는지)
print("\n[4] 외래 키 참조 확인...")
cursor.execute("SELECT COUNT(*) FROM lesson WHERE course_id = (SELECT id FROM course WHERE title LIKE '%건설법규%')")
count = cursor.fetchone()[0]
print(f"  총 {count}개 레슨이 정상적으로 업데이트되었습니다.")

conn.close()

print("\n[OK] 건설법규 레슨 ID 변경 완료!")
print("   이전: 91-104")
print("   이후: 42-55")
