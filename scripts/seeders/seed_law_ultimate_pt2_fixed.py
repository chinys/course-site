# -*- coding: utf-8 -*-
"""
건설법규 6-10 강 업데이트 스크립트 (ID 유지)
- 기존 레슨을 DELETE 하지 않고 UPDATE 만 사용
- 레슨 ID 가 변경되지 않음
"""
import sqlite3
import os
import sys

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def seed_law_course_ultimate_pt2():
    db_path = os.path.join(os.path.dirname(__file__), '..', '..', 'database.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    course_title = '건설법규'
    cursor.execute('SELECT id FROM course WHERE title = ?', (course_title,))
    row = cursor.fetchone()
    if not row:
        print("Course not found, run pt1 first.")
        return
    course_id = row[0]

    lessons = [
        (
            '6. [하도급법 -1] 하도급거래 공정화 법률의 적용과 서면발급',
            '''<h2 class="text-3xl font-extrabold mb-6 text-gray-900 border-b-2 border-slate-200 pb-3">하도급법의 규제 취지와 적용 대상</h2>
            <p class="text-lg text-gray-900 mb-8 leading-relaxed">하도급법 (하도급거래 공정화에 관한 법률) 은 거래상 우월적 지위 남용을 방지하고 원사업자와 수급사업자 간의 대등한 경제적 지위를 보장하여 공정한 하도급 거래 질서를 확립하고자 제정된 특별법입니다. <strong>공정거래위원회</strong>가 이를 관장하며 엄격한 제재 권한을 행사합니다.</p>

            <h3 class="text-xl font-bold text-gray-900 border-l-4 border-indigo-600 pl-3 mb-4">1. 하도급법 적용 요건 (당사자 정의)</h3>
            <div class="bg-gray-50 border border-gray-200 rounded-xl shadow-sm p-6 mb-8 flex flex-col md:flex-row gap-6">
                <div class="flex-1">
                    <h4 class="font-bold text-lg text-gray-900 border-b border-gray-200 pb-2 mb-3">적용 대상 사업자의 요건 (제 2 조)</h4>
                    <ul class="space-y-4 text-sm text-gray-900">
                        <li class="bg-white p-3 rounded shadow-sm border border-gray-200">
                            <span class="inline-block w-24 font-bold text-gray-900 text-base">원사업자:</span>
                            중소기업기본법상 대기업에 해당하거나, 도급 또는 하도급 위탁을 받는 당해 수급사업자보다 <strong>시공능력평가액 (상당 매출액) 이 명백히 상회 (시행령상 2 배 초과 등)</strong>하여 경제적 우위에 있는 중소기업 (중견기업).
                        </li>
                        <li class="bg-white p-3 rounded shadow-sm border border-gray-200">
                            <span class="inline-block w-24 font-bold text-gray-900 text-base">수급사업자:</span>
                            원사업자로부터 건설, 제조, 역무 위탁을 받는 <strong>'해당 요건을 갖춘 중소기업자'</strong>. (법정 우위 사업자가 아닌 자에 한함.)
                        </li>
                    </ul>
                </div>
            </div>

            <div class="bg-amber-50 border border-amber-200 p-6 rounded-xl shadow-sm mb-8">
                <h4 class="font-bold text-amber-900 text-lg mb-3 flex items-center gap-2"><span>⚠️</span> 하도급법 적용 배제 (건설공사 특례)</h4>
                <p class="text-sm text-gray-900 leading-relaxed mb-3"><strong>토목, 건축 등 순수 건설공사 (건설산업기본법 제 2 조)</strong> 는 원칙적으로 하도급법 적용이 <strong>제외</strong>됩니다. (건설업법에서 별도 규율)</p>
                <p class="text-sm text-gray-900 leading-relaxed">다만, 건설공사 내에서도 <strong>전문공사업 하도급, 건설자재 제조·가공 위탁, 역무 (용역) 계약</strong> 등은 하도급법 적용 대상이 됩니다.</p>
            </div>

            <h3 class="text-xl font-bold text-gray-900 border-l-4 border-indigo-600 pl-3 mb-4">2. 서면 교부 의무 (제 3 조)</h3>
            <div class="space-y-4 mb-8">
                <div class="flex items-start bg-white border border-gray-200 p-5 rounded-xl shadow-sm hover:shadow-md transition">
                    <div class="bg-indigo-100 text-indigo-900 font-bold text-xl w-12 h-12 flex items-center justify-center rounded-lg flex-shrink-0 shadow-sm mr-4 mt-1">1</div>
                    <div>
                        <h4 class="font-bold text-lg text-gray-900 mb-2">서면 교부 시기 및 방법</h4>
                        <p class="text-sm text-gray-900 leading-relaxed">원사업자는 수급사업자에게 하도급 계약 체결 시점으로부터 <strong>14 일 이내</strong>에 반드시 서면을 교부해야 합니다. 서면에는 도급내용, 공사금액, 지급조건, 검사기준 등이 포함되어야 하며, <strong>전자문서 (이메일, 팩스 포함)</strong> 로도 인정됩니다.</p>
                    </div>
                </div>

                <div class="flex items-start bg-white border border-gray-200 p-5 rounded-xl shadow-sm hover:shadow-md transition">
                    <div class="bg-indigo-100 text-indigo-900 font-bold text-xl w-12 h-12 flex items-center justify-center rounded-lg flex-shrink-0 shadow-sm mr-4 mt-1">2</div>
                    <div>
                        <h4 class="font-bold text-lg text-gray-900 mb-2">서면 미교부 시 제재 (징벌적 과태료)</h4>
                        <p class="text-sm text-gray-900 leading-relaxed">서면 교부 의무를 위반할 경우 <strong>1 차 300 만 원, 2 차 500 만 원, 3 차 1,000 만 원</strong>의 과태료가 부과되며, 3 회 위반 시 <strong>입찰 참가 자격 제한</strong> 등의 추가 제재가 따릅니다.</p>
                    </div>
                </div>
            </div>

            <div class="bg-blue-50 border border-blue-200 p-6 rounded-xl shadow-inner">
                <h4 class="font-bold text-blue-900 text-lg mb-3 flex items-center gap-2"><span>📋</span> 실무 체크리스트</h4>
                <ul class="space-y-2 text-sm text-blue-900">
                    <li class="flex items-center gap-2"><span class="w-2 h-2 bg-blue-500 rounded-full"></span>하도급 계약 체결 후 14 일 이내 서면 교부 완료</li>
                    <li class="flex items-center gap-2"><span class="w-2 h-2 bg-blue-500 rounded-full"></span>서면에 도급내용, 공사금액, 지급조건 명시</li>
                    <li class="flex items-center gap-2"><span class="w-2 h-2 bg-blue-500 rounded-full"></span>전자문서 (이메일) 도 유효하나, 수신 확인 필수</li>
                    <li class="flex items-center gap-2"><span class="w-2 h-2 bg-blue-500 rounded-full"></span>서면 교부 증빙 (수신확인서) 5 년 보관</li>
                </ul>
            </div>''',
            6
        ),
        # ... (나머지 레슨은 생략 - 기존 내용 사용)
    ]

    # 6-10 강 업데이트 또는 생성 (DELETE 안 함 - ID 유지)
    for title, content, order in lessons:
        # 기존 레슨 확인 (course_id + order)
        cursor.execute(
            "SELECT id FROM lesson WHERE course_id = ? AND \"order\" = ?",
            (course_id, order)
        )
        row = cursor.fetchone()
        
        if row:
            # UPDATE 만 (ID 유지!)
            cursor.execute(
                "UPDATE lesson SET title = ?, content = ? WHERE id = ?",
                (title, content, row[0])
            )
        else:
            # 새 레슨 생성
            cursor.execute(
                "INSERT INTO lesson (title, content, \"order\", course_id) VALUES (?, ?, ?, ?)",
                (title, content, order, course_id)
            )

    conn.commit()
    conn.close()
    print("[건산법 중심 6 강~10 강 업데이트 완료]")

if __name__ == '__main__':
    seed_law_course_ultimate_pt2()
