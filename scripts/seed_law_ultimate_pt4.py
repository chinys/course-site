import sqlite3
import os

def seed_law_course_ultimate_pt4():
    db_path = os.path.join(os.path.dirname(__file__), '..', 'database.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM course WHERE title = '[건설법규]'")
    row = cursor.fetchone()
    if not row:
        print("Error: [건설법규] course not found.")
        return
    course_id = row[0]

    html = _build_html()
    lessons = [('14. [실무 핵심 양식] 강구조물 불법 재하도급 방지용 계약서 10종 (풀버전)', html, 14)]
    for title, content, order in lessons:
        cursor.execute("INSERT INTO lesson (title, content, course_id, \"order\") VALUES (?, ?, ?, ?)",
                       (title, content, course_id, order))
    conn.commit()
    conn.close()
    print("[법무 심화 14강] 강구조물 실무 특화 계약서 양식 추가 완료")


def _build_html():
    from _section_a import section_a
    from _section_b import section_b
    from _section_c import section_c
    from _section_d import section_d
    from _section_e import section_e
    parts = [_intro(), section_a(), section_b(), section_c(), section_d(), section_e(), '</div>']
    return '\n'.join(parts)


def _intro():
    return '''<h2 class="text-2xl font-bold mb-4">강구조물(철골) 공사 불법 재하도급 리스크 단절 완벽 가이드 및 계약서 양식 (전체 조문 풀버전)</h2>
<p class="text-lg text-gray-700 mb-6">전문건설업체가 철골 공사를 도급받아 수행할 때, 가장 적발되기 쉬운 "위장 하도급(불법 재하도급)" 혐의를 원천 차단하기 위한 <strong>실무 맞춤형 핵심 계약서 양식 10종의 전체 조문</strong>입니다. 민법상 계약 유형(매매·임대차·위임·고용·운송)별로 분류하여 법적 성격을 명확히 하였습니다. 단편적인 조항이 아닌 <strong>전문(문두)부터 부칙, 서명란까지 100% 완비된 실제 실무용 계약서</strong>입니다.</p>

<div class="bg-white border border-gray-200 rounded-lg p-5 mb-8 shadow-sm">
    <h3 class="font-bold text-lg mb-3">📋 민법상 계약유형별 분류 체계</h3>
    <table class="w-full text-sm border-collapse">
        <tr class="bg-gray-100"><th class="border p-2 text-left">유형</th><th class="border p-2 text-left">근거법</th><th class="border p-2 text-left">양식번호</th><th class="border p-2 text-left">계약서명</th></tr>
        <tr><td class="border p-2 font-bold text-blue-700" rowspan="3">A. 매매(물품공급) / 가공 도급</td><td class="border p-2" rowspan="3">민법 §563 / §664</td><td class="border p-2">A-1</td><td class="border p-2">철골 자재 물품공급(외주 가공제작/납품) 계약서</td></tr>
        <tr><td class="border p-2">A-2</td><td class="border p-2">외주 사급가공 계약서 (자재·DWG 수급자 직접가공)</td></tr>
        <tr><td class="border p-2">A-3</td><td class="border p-2">사내가공제작(사내도장) 계약서</td></tr>
        <tr><td class="border p-2 font-bold text-orange-700" rowspan="2">B. 임대차</td><td class="border p-2" rowspan="2">민법 §618</td><td class="border p-2">B-1</td><td class="border p-2">건설기계 장비 임대차계약서</td></tr>
        <tr><td class="border p-2">B-2</td><td class="border p-2">가설재(비계) 임대차계약서</td></tr>
        <tr><td class="border p-2 font-bold text-purple-700" rowspan="2">C. 위임·위탁</td><td class="border p-2" rowspan="2">민법 §680</td><td class="border p-2">C-1</td><td class="border p-2">NDT 기술용역 위탁계약서</td></tr>
        <tr><td class="border p-2">C-2</td><td class="border p-2">함바식당 운영 위탁계약서</td></tr>
        <tr><td class="border p-2 font-bold text-teal-700" rowspan="2">D. 고용·위촉</td><td class="border p-2" rowspan="2">민법 §655 / 근로기준법</td><td class="border p-2">D-1</td><td class="border p-2">기술자문 및 현장관리 위촉계약서</td></tr>
        <tr><td class="border p-2">D-2</td><td class="border p-2">일용직 근로계약서</td></tr>
        <tr><td class="border p-2 font-bold text-rose-700">E. 운송</td><td class="border p-2">상법 §125</td><td class="border p-2">E-1</td><td class="border p-2">화물(강재) 운반 용역계약서</td></tr>
    </table>
</div>

<div class="space-y-12">'''


if __name__ == "__main__":
    seed_law_course_ultimate_pt4()
