# -*- coding: utf-8 -*-
"""
건설법규 강좌 중복 레슨 정리 스크립트
- 중복된 레슨 삭제 (42-55 번만 유지)
"""
import sqlite3
import os

# DB 경로 (프로젝트 루트의 database.db)
db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'database.db')
print(f"DB 경로: {db_path}")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("=== 건설법규 중복 레슨 정리 ===\n")

# 1. 현재 상태 확인
print("[1] 현재 레슨 상태:")
cursor.execute("""
    SELECT id, title, "order" 
    FROM lesson 
    WHERE course_id = 5
    ORDER BY "order", id
""")
rows = cursor.fetchall()

current_order = None
for row in rows:
    if row[2] != current_order:
        print(f"\n  Order {row[2]}:")
        current_order = row[2]
    print(f"    ID {row[0]}: {row[1][:30]}...")

# 2. 중복 레슨 삭제 (42-55 번만 유지)
print("\n\n[2] 중복 레슨 삭제 중...")

# order 별로 그룹화
cursor.execute("""
    SELECT "order", GROUP_CONCAT(id) as ids
    FROM lesson
    WHERE course_id = 5
    GROUP BY "order"
""")
order_groups = cursor.fetchall()

deleted_count = 0
for order, ids_str in order_groups:
    ids = [int(x) for x in ids_str.split(',')]
    # 42-55 사이 ID 는 유지, 나머지는 삭제
    ids_to_keep = [x for x in ids if 42 <= x <= 55]
    ids_to_delete = [x for x in ids if x < 42 or x > 55]
    
    if ids_to_delete:
        for id_to_delete in ids_to_delete:
            cursor.execute("DELETE FROM lesson WHERE id = ?", (id_to_delete,))
            deleted_count += 1
            print(f"  [DELETE] ID {id_to_delete} (order={order})")

conn.commit()

# 3. 정리 결과 확인
print(f"\n\n[3] 정리 완료 - {deleted_count}개 레슨 삭제됨\n")

cursor.execute("""
    SELECT id, title, "order" 
    FROM lesson 
    WHERE course_id = 5
    ORDER BY "order"
""")
rows = cursor.fetchall()

print("남은 레슨:")
for row in rows:
    print(f"  ID {row[0]}: order={row[2]}, {row[1][:30]}...")

conn.close()

print(f"\n[OK] 정리 완료! 총 {len(rows)}개 레슨 유지")
