import sqlite3
import os

def seed_law_course_ultimate_pt4():
    db_path = os.path.join(os.path.dirname(__file__), '..', 'database.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM course WHERE title LIKE '%건설법규%'")
    row = cursor.fetchone()
    if not row:
        print("Error: [건설법규] course not found.")
        return
    course_id = row[0]

    html = _build_html()
    title = '14. [실무 핵심 양식] 강구조물 불법 재하도급 방지용 계약서 모음'
    
    cursor.execute("SELECT id FROM lesson WHERE course_id = ? AND title LIKE '%계약서 모음%'", (course_id,))
    lesson_row = cursor.fetchone()
    
    if lesson_row:
        cursor.execute("UPDATE lesson SET content = ? WHERE id = ?", (html, lesson_row[0]))
        print("[법무 심화 14강] 기존 내용 업데이트 완료")
    else:
        cursor.execute("INSERT INTO lesson (title, content, course_id, \"order\") VALUES (?, ?, ?, ?)",
                       (title, html, course_id, 14))
        print("[법무 심화 14강] 강구조물 실무 특화 계약서 양식 추가 완료")
        
    conn.commit()
    conn.close()


def _build_html():
    from _section_a import section_a
    from _section_b import section_b
    from _section_c import section_c
    from _section_d import section_d
    from _section_e import section_e
    parts = [_intro(), section_a(), section_b(), section_c(), section_d(), section_e(), '</div>']
    return '\n'.join(parts)


def _intro():
    return '''<h2 class="text-2xl font-bold mb-4">강구조물(철골) 공사 불법 재하도급 리스크 예방 가이드 및 계약서 양식</h2>

<p class="text-lg text-gray-700 mb-6">전문건설업체가 철골 공사를 도급받아 수행할 때, 가장 적발되기 쉬운 "위장 하도급(불법 재하도급)" 문제를 사전에 예방하고자 만든&nbsp;<strong>계약서 양식</strong>입니다. 민법상 계약 유형(매매&middot;임대차&middot;위임&middot;고용&middot;운송)별로 분류하여 법적 성격을 명확히 하였습니다. 단편적인 조항이 아닌 <strong>전문부터 부칙, 서명란까지 포함된 실무용 계약서</strong>입니다. 현업에 맞게 수정 사용하되, 핵심적인 문구는 유지하기 바랍니다.</p>

<div class="bg-white border border-gray-200 rounded-lg p-5 mb-8 shadow-sm">

<h3 class="font-bold text-lg mb-3">📋 민법상 계약유형별 분류 체계</h3>

<table class="w-full text-sm border-collapse">

<tbody>

<tr class="bg-gray-100">

<th class="border p-2 text-left">유형</th>

<th class="border p-2 text-left">근거법</th>

<th class="border p-2 text-left">양식번호</th>

<th class="border p-2 text-left">계약서명</th>

<th class="border p-2 text-center" style="width: 110px;">다운로드</th>

</tr>

<tr>

<td class="border p-2 font-bold text-blue-700" rowspan="3">A. 매매(물품공급) / 도급(가공)</td>

<td class="border p-2" rowspan="3">민법 &sect;563 / &sect;664</td>

<td class="border p-2">A-1</td>

<td class="border p-2">물품공급(제조납품) 계약서</td>

<td class="border p-2 text-center"><a class="inline-block text-xs bg-blue-600 text-white px-2 py-1 rounded hover:bg-blue-700 no-underline" href="/static/downloads/contract_A1.docx" target="_blank" rel="noopener" download="contract_A1.docx">📄 docx</a></td>

</tr>

<tr>

<td class="border p-2">A-2</td>

<td class="border p-2">외주가공(제조위탁) 계약서</td>

<td class="border p-2 text-center"><a class="inline-block text-xs bg-blue-600 text-white px-2 py-1 rounded hover:bg-blue-700 no-underline" href="/static/downloads/contract_A2.docx" target="_blank" rel="noopener" download="contract_A2.docx">📄 docx</a></td>

</tr>

<tr>

<td class="border p-2">A-3</td>

<td class="border p-2">사내가공(제조위탁) 계약서</td>

<td class="border p-2 text-center"><a class="inline-block text-xs bg-blue-600 text-white px-2 py-1 rounded hover:bg-blue-700 no-underline" href="/static/downloads/contract_A3.docx" target="_blank" rel="noopener" download="contract_A3.docx">📄 docx</a></td>

</tr>

<tr>

<td class="border p-2 font-bold text-orange-700" rowspan="2">B. 임대차</td>

<td class="border p-2" rowspan="2">민법 &sect;618</td>

<td class="border p-2">B-1</td>

<td class="border p-2">건설기계 장비 임대차계약서</td>

<td class="border p-2 text-center"><a class="inline-block text-xs bg-orange-600 text-white px-2 py-1 rounded hover:bg-orange-700 no-underline" href="/static/downloads/contract_B1.docx" target="_blank" rel="noopener" download="contract_B1.docx">📄 docx</a></td>

</tr>

<tr>

<td class="border p-2">B-2</td>

<td class="border p-2">가설재(비계&middot;서포트) 임대차계약서</td>

<td class="border p-2 text-center"><a class="inline-block text-xs bg-orange-600 text-white px-2 py-1 rounded hover:bg-orange-700 no-underline" href="/static/downloads/contract_B2.docx" target="_blank" rel="noopener" download="contract_B2.docx">📄 docx</a></td>

</tr>

<tr>

<td class="border p-2 font-bold text-purple-700" rowspan="2">C. 위임&middot;위탁</td>

<td class="border p-2" rowspan="2">민법 &sect;680</td>

<td class="border p-2">C-1</td>

<td class="border p-2">기술&middot;품질용역 위탁계약서(NDT)</td>

<td class="border p-2 text-center"><a class="inline-block text-xs bg-purple-600 text-white px-2 py-1 rounded hover:bg-purple-700 no-underline" href="/static/downloads/contract_C1.docx" target="_blank" rel="noopener" download="contract_C1.docx">📄 docx</a></td>

</tr>

<tr>

<td class="border p-2">C-2</td>

<td class="border p-2">건설현장 급식(함바식당) 운영 위탁계약서</td>

<td class="border p-2 text-center"><a class="inline-block text-xs bg-purple-600 text-white px-2 py-1 rounded hover:bg-purple-700 no-underline" href="/static/downloads/contract_C2.docx" target="_blank" rel="noopener" download="contract_C2.docx">📄 docx</a></td>

</tr>

<tr>

<td class="border p-2 font-bold text-teal-700" rowspan="2">D. 고용&middot;위촉</td>

<td class="border p-2" rowspan="2">민법 &sect;655 / 근로기준법</td>

<td class="border p-2">D-1</td>

<td class="border p-2">전문 기술자문 및 현장관리 위촉계약서</td>

<td class="border p-2 text-center"><a class="inline-block text-xs bg-teal-600 text-white px-2 py-1 rounded hover:bg-teal-700 no-underline" href="/static/downloads/contract_D1.docx" target="_blank" rel="noopener" download="contract_D1.docx">📄 docx</a></td>

</tr>

<tr>

<td class="border p-2">D-2</td>

<td class="border p-2">일용직 근로계약서</td>

<td class="border p-2 text-center"><a class="inline-block text-xs bg-teal-600 text-white px-2 py-1 rounded hover:bg-teal-700 no-underline" href="/static/downloads/contract_D2.docx" target="_blank" rel="noopener" download="contract_D2.docx">📄 docx</a></td>

</tr>

<tr>

<td class="border p-2 font-bold text-rose-700">E. 운송</td>

<td class="border p-2">상법 &sect;125</td>

<td class="border p-2">E-1</td>

<td class="border p-2">화물(강재) 운반 용역계약서</td>

<td class="border p-2 text-center"><a class="inline-block text-xs bg-rose-600 text-white px-2 py-1 rounded hover:bg-rose-700 no-underline" href="/static/downloads/contract_E1.docx" target="_blank" rel="noopener" download="contract_E1.docx">📄 docx</a></td>

</tr>

</tbody>

</table>

</div>

<div class="space-y-12">
<div class="space-y-12">'''


if __name__ == "__main__":
    seed_law_course_ultimate_pt4()
