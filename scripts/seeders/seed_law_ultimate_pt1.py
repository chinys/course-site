import sqlite3
import os
import sys

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def seed_law_course_ultimate():
    db_path = os.path.join(os.path.dirname(__file__), '..', '..', 'database.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM category WHERE name = '법무관련'")
    row = cursor.fetchone()
    if not row:
        cursor.execute("INSERT INTO category (name, \"order\") VALUES ('법무관련', 3)")
        category_id = cursor.lastrowid
    else:
        category_id = row[0]

    course_title = '건설법규'
    thumbnail_path = '/static/uploads/law_thumbnail.png'
    
    cursor.execute('SELECT id FROM course WHERE title = ?', (course_title,))
    row = cursor.fetchone()
    if row:
        course_id = row[0]
        cursor.execute("DELETE FROM lesson WHERE course_id = ?", (course_id,))
        cursor.execute('''
            UPDATE course 
            SET description = '건설산업기본법(건산법)을 완벽 해부하는 14강 체제 궁극의 실무 매뉴얼. 하도급법, 도급계약서, 중대재해처벌법 가이드까지 현장 관리자 및 실무진을 위한 필수 지침서입니다.',
                thumbnail_url = ?, category_id = ? 
            WHERE id = ?
        ''', (thumbnail_path, category_id, course_id))
    else:
        cursor.execute('''
            INSERT INTO course (title, description, thumbnail_url, category_id) 
            VALUES (?, ?, ?, ?)
        ''', (course_title, "건설산업기본법(건산법)을 완벽 해부하는 14강 체제 궁극의 실무 매뉴얼. 하도급법, 도급계약서, 중대재해처벌법 가이드까지 현장 관리자 및 실무진을 위한 필수 지침서입니다.", thumbnail_path, category_id))
        course_id = cursor.lastrowid

    lessons = [
        (
            '1. [건산법 총칙] 건설산업기본법의 목적과 적용 범위', 
            '''<h2 class="text-3xl font-extrabold mb-6 text-gray-900 border-b-2 border-slate-200 pb-3">건설산업기본법(건산법)의 개요</h2>
            
            <div class="bg-blue-50 border border-blue-200 p-6 rounded-xl shadow-lg mb-8">
                <p class="text-lg leading-loose text-blue-900"><span class="font-bold text-xl text-indigo-700">핵심 요약:</span> 건설산업기본법(이하 건산법)은 대한민국 건설공사의 조사, 설계, 시공, 감리, 유지관리 등 <strong>건설업에 관한 기본적인 사항과 건설업의 등록, 건설공사의 도급 등에 관한 기준</strong>을 명확히 규정하여 건설공사의 적정한 시공과 건설산업의 건전한 발전을 도모함을 목적으로 하는 최상위 기본법입니다.</p>
            </div>
            
            <h3 class="text-xl font-bold text-gray-900 border-l-4 border-blue-600 pl-3 mb-4">1.1. 주요 용어의 정의 (제2조)</h3>
            <div class="overflow-hidden bg-white rounded-xl shadow-md border border-gray-200 mb-8">
                <table class="w-full text-left border-collapse">
                    <thead>
                        <tr class="bg-gray-100 font-bold text-sm text-gray-900">
                            <th class="p-4 font-bold w-1/4">용어</th>
                            <th class="p-4 font-bold">건산법상 정의 및 실무적 해석</th>
                        </tr>
                    </thead>
                    <tbody class="text-sm">
                        <tr class="border-b hover:bg-gray-50 transition text-gray-900">
                            <td class="p-4 font-semibold text-gray-900">건설산업</td>
                            <td class="p-4 text-gray-900 leading-relaxed">건설업과 건설용역업을 통칭합니다.</td>
                        </tr>
                        <tr class="border-b hover:bg-gray-50 transition text-gray-900">
                            <td class="p-4 font-semibold text-gray-900">건설공사</td>
                            <td class="p-4 text-gray-900 leading-relaxed">토목공사, 건축공사, 산업설비공사, 조경공사, 환경시설공사 등 시설물을 설치·유지·보수하는 공사.<br><strong class="text-red-900">※ 주의사항:</strong> 전기공사, 정보통신공사, 소방시설공사, 문화재수리공사는 건산법상 제한적 적용을 받으며 별도의 개별법령이 우선 적용됩니다.</td>
                        </tr>
                        <tr class="border-b hover:bg-gray-50 transition text-gray-900">
                            <td class="p-4 font-semibold text-gray-900">도급 / 하도급</td>
                            <td class="p-4 text-gray-900 leading-relaxed"><ul class="list-disc pl-5 space-y-1"><li><strong>도급:</strong> 발주자와 수급인 간, 또는 수급인과 하수급인 간에 일의 완성을 약정하고 이에 대한 대가를 지급할 것을 약정하는 계약.</li><li><strong>하도급:</strong> 도급받은 건설공사의 전부 또는 일부를 다시 위탁하기 위하여 수급인이 제3자와 체결하는 도급계약.</li></ul></td>
                        </tr>
                        <tr class="hover:bg-gray-50 transition text-gray-900">
                            <td class="p-4 font-semibold text-gray-900">발주자 / 수급인</td>
                            <td class="p-4 text-gray-900 leading-relaxed"><strong>발주자:</strong> 건설공사를 도급하는 자 (직접 시공하는 자 제외).<br><strong>수급인(원도급자 / 원청):</strong> 발주자로부터 공사를 직접 도급받은 건설사업자.</td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <h3 class="text-xl font-bold text-gray-900 border-l-4 border-blue-600 pl-3 mb-4">1.2. 타 법률과의 관계 (제3조)</h3>
            <p class="text-gray-900 mb-4 text-base leading-relaxed">건산법은 건설산업에 관하여 다른 법률에 우선하여 적용되는 <strong>기본법</strong>의 지위를 가집니다. 다만, 전기, 통신, 소방 등 타 법률에 특별한 규정이 있는 경우에는 해당 법률이 우선합니다. 공정거래 및 하도급 계약 관계에 관해서는 '하도급거래 공정화에 관한 법률(하도급법)'이 건산법에 우선 적용되는 특별법적 효력을 지닙니다.</p>
            
            <div class="bg-indigo-50 p-6 rounded-lg border border-indigo-200 mt-6 shadow-sm">
                <h4 class="font-bold text-indigo-900 mb-3 text-lg flex items-center gap-2"><span>💡</span> 실무 판례 및 해석: 분리 발주의 원칙</h4>
                <p class="text-sm text-gray-900 leading-relaxed mb-3"><strong>Q: 복합 공사(건축 및 전기/통신)를 단일 종합건설사에게 일괄 도급(Turn-key) 형태로 발주할 수 있습니까?</strong></p>
                <p class="text-sm text-gray-900 leading-relaxed bg-white p-3 rounded border border-indigo-100"><strong>A: 원칙적으로 불가합니다.</strong> 관련 법령(전기공사업법 및 정보통신공사업법)에 따라 건설공사와 전기/정보통신공사는 각각 <strong>분리 발주</strong>하여야 합니다. 이를 위반하여 일괄 발주 후 하도급하는 경우 행정처분 및 형사처벌 대상이 될 수 있습니다. 단, 국가기밀 공사나 공정 구조상 분리가 불가능한 특수 공사에 한하여 예외가 인정됩니다.</p>
            </div>''', 
            1
        ),
        (
            '2. [건산법 등록] 건설업의 등록체계와 결격사유', 
            '''<h2 class="text-3xl font-extrabold mb-6 text-gray-900 border-b-2 border-slate-200 pb-3">건설업 면허 체계의 법적 이해</h2>
            <p class="text-lg text-gray-900 mb-6 leading-relaxed">부실시공 방지 및 현장 안전 확보를 위한 제도적 장치로서 건설공사는 법정 요건을 갖추어 등록한 <strong>건설사업자</strong>만이 수행할 수 있도록 규정하고 있습니다.</p>
            
            <h3 class="text-xl font-bold text-gray-900 border-b-2 border-gray-200 pb-2 mb-4">2.1. 건설업의 종류 및 등록 요건 (제9조)</h3>
            <p class="text-gray-900 mb-4 leading-relaxed">건설업은 <strong>종합적인 계획, 관리, 조정 하에 시설물을 시공하는 종합건설업</strong>과 <strong>세부 공종별 전문공사를 시공하는 전문건설업</strong>으로 분류됩니다. 건설업을 영위하려는 사업자는 자본금, 기술능력, 요건에 부합하는 시설 및 장비를 갖추어 주무관청(국토교통부 또는 관할 지자체)에 등록하여야 합니다.</p>
            
            <div class="grid md:grid-cols-2 gap-6 mb-8">
                <div class="border p-5 rounded-xl bg-white shadow-md border-blue-200 transition">
                    <h4 class="font-bold text-indigo-900 mb-4 text-lg border-b border-indigo-200 pb-2 flex items-center gap-2"><span>🏗️</span> 종합건설업 (5개 업종)</h4>
                    <ul class="text-sm text-gray-900 list-none space-y-2">
                        <li class="flex items-center gap-2"><span class="w-1.5 h-1.5 rounded-full bg-indigo-200"></span>건축공사업 (자본금 3.5억원 이상, 관련 기술인 5인 이상)</li>
                        <li class="flex items-center gap-2"><span class="w-1.5 h-1.5 rounded-full bg-indigo-200"></span>토목공사업 (자본금 5억원 이상, 관련 기술인 6인 이상)</li>
                        <li class="flex items-center gap-2"><span class="w-1.5 h-1.5 rounded-full bg-indigo-200"></span>토목건축공사업 (자본금 8.5억원 이상, 관련 기술인 11인 이상)</li>
                        <li class="flex items-center gap-2"><span class="w-1.5 h-1.5 rounded-full bg-indigo-200"></span>산업설비공사업</li>
                        <li class="flex items-center gap-2"><span class="w-1.5 h-1.5 rounded-full bg-indigo-200"></span>조경공사업</li>
                    </ul>
                </div>
                <div class="border p-5 rounded-xl bg-white shadow-md border-teal-200 transition">
                    <h4 class="font-bold text-teal-900 mb-2 text-lg border-b border-teal-200 pb-2 flex items-center gap-2"><span>🛠️</span> 전문건설업 (대업종화 체계)</h4>
                    <p class="text-xs text-gray-900 mb-3 bg-teal-50 p-2 rounded shadow-inner">2022년 시행령 개정으로 전문건설업 업종이 대업종 단위로 통합 운영되고 있습니다.</p>
                    <ul class="text-sm text-gray-900 list-none space-y-2">
                        <li class="flex items-center gap-2"><span class="w-1.5 h-1.5 rounded-full bg-teal-200"></span>지반조성·포장공사업</li>
                        <li class="flex items-center gap-2"><span class="w-1.5 h-1.5 rounded-full bg-teal-200"></span>실내건축공사업</li>
                        <li class="flex items-center gap-2"><span class="w-1.5 h-1.5 rounded-full bg-teal-200"></span>금속창호·지붕건축물조립공사업</li>
                        <li class="flex items-center gap-2"><span class="w-1.5 h-1.5 rounded-full bg-teal-200"></span>철근·콘크리트공사업 등 29개 업종</li>
                    </ul>
                </div>
            </div>
            
            <div class="bg-red-50 p-6 rounded-xl border border-red-200 mb-8 shadow-sm">
                <h4 class="font-bold text-red-900 text-lg mb-3 flex items-center gap-2"><span class="text-2xl">🚨</span> 경미한 건설공사의 구별 기준</h4>
                <p class="text-sm text-gray-900 mb-3 leading-relaxed">법률에서 정하는 극히 소규모 공사에 한하여 예외적으로 건설업 등록이 없는 일반 사업자나 개인의 시공을 허용합니다.</p>
                <div class="bg-white p-4 rounded-lg border border-red-100 mb-3 shadow-inner">
                    <ul class="text-sm font-semibold text-gray-900 list-disc pl-5 space-y-2">
                        <li><strong>종합공사:</strong> 예정금액 <strong>5천만원 미만</strong> (부가가치세 포함)</li>
                        <li><strong>전문공사:</strong> 예정금액 <strong>1천5백만원 미만</strong> (부가가치세 포함)</li>
                    </ul>
                </div>
                <p class="text-xs text-gray-900 leading-relaxed bg-white p-3 rounded-lg border border-red-100 mt-2">
                    <strong>[법무 해석] 분할발주(쪼개기 발주)의 제한:</strong> 무면허 시공을 우회하기 위해 다수의 계약으로 분할하여도, 동일 사업자가 동일 현장에서 연속하여 시공한 경우 법원은 이를 <strong>합산하여 판단</strong>합니다. 기준 금액 초과 시 무등록 시공으로 형사 처벌되며, 가스, 철강 등 특수 공종은 금액과 무관하게 무조건 등록증을 요합니다.
                </p>
            </div>

            <h3 class="text-xl font-bold text-gray-900 border-b-2 border-gray-200 pb-2 mb-4">2.2. 등록기준의 유지 및 실태조사 강화</h3>
            <p class="text-gray-900 mb-4 leading-relaxed text-sm">부실 건설사(페이퍼컴퍼니) 제재를 위해 관할 관청의 <strong>실태조사 및 조기경보시스템</strong> 운영이 강화되었습니다. 법정 실질자본금 미달 또는 독립된 사무실 미확보 등 등록기준 결격 요건 확인 시 직권으로 행정처분(영업정지 등)이 부과됩니다.</p>

            <h3 class="text-xl font-bold text-red-900 border-b-2 border-gray-200 pb-2 mb-4">2.3. 무면허 시공 및 명의대여 금지 규정 (제21조)</h3>
            <p class="text-gray-900 mb-3 leading-relaxed">건설업자가 타인에게 자신의 상호 또는 성명을 차용하게 하여 건설공사를 수급 또는 시공하게 하는 행위(명의대여)는 중대한 범죄에 해당합니다.</p>
            <div class="bg-gray-50 text-gray-900 font-bold p-5 rounded-xl shadow-md border border-gray-300">
                <p class="text-sm text-gray-900 leading-relaxed font-semibold"><strong class="text-gray-900 mr-2">강행 규정 및 벌칙 (제96조):</strong> 무등록 시공자, 명의 대여자 및 차용자, 관련 알선자 전원은 <strong class="text-red-900 text-lg mx-1">5년 이하의 징역 또는 5천만원 이하의 벌금</strong>에 처해집니다.<br>더불어, 해당 위반 사업자는 행정 처분으로 <strong>필요적 등록 말소(면허 영구 취소)</strong> 대상이 됩니다.</p>
            </div>''',
            2
        ),
        (
            '3. [건산법 도급/하도급-1] 도급의 원칙과 다단계 하도급 금지', 
            '''<h2 class="text-3xl font-extrabold mb-6 text-gray-900 border-b-2 border-slate-200 pb-3">건설공사 도급계약 및 하도급 규제</h2>
            <p class="text-lg text-gray-900 mb-8 leading-relaxed">법령 구조상 하도급 과정에서 발생할 수 있는 품질 저하 및 불공정 거래 구조를 사전에 차단하기 위해 <strong>단계적 하도급을 엄격히 금지</strong>하고 있습니다.</p>
            
            <div class="grid grid-cols-1 mb-8 gap-5">
                <div class="border-l-4 border-gray-600 bg-white p-5 rounded-r-xl shadow-sm transition">
                    <h3 class="text-xl font-bold text-gray-900 mb-3">🚫 일괄 하도급의 원칙적 금지 (제29조 제1항)</h3>
                    <p class="text-gray-900 text-sm mb-3 leading-relaxed">수급인은 도급받은 건설공사의 <strong>전부 또는 대통령령으로 정하는 주요 부분의 대부분을 다른 건설사업자에게 일괄하여 하도급할 수 없습니다.</strong> 이는 부당한 위탁 이익 수취 및 시공 책임 소수화를 막기 위한 조치입니다.</p>
                    <div class="bg-gray-50 p-3 rounded text-sm text-gray-900 border border-gray-200">
                        ※ 예외 규정: 발주자의 사전 서면 승낙이 존재하며, 둘 이상의 사업자에게 분할하여 도급하는 제한적 요건 하에 허용 가능.
                    </div>
                </div>

                <div class="border-l-4 border-gray-600 bg-white p-5 rounded-r-xl shadow-sm transition">
                    <h3 class="text-xl font-bold text-gray-900 mb-3">🔄 동일 업종 간 하도급의 제한 (제29조 제2항)</h3>
                    <p class="text-gray-900 text-sm mb-2 leading-relaxed">종합건설업자는 인수한 종합공사를 원칙적으로 다른 종합건설업자에게, 전문은 전문에게 하도급할 수 없습니다. <strong>불필요한 동종 간 이윤 공제 행위를 방지</strong>합니다.</p>
                    <p class="text-xs text-gray-900">※ 예외 규정: 발주자가 공사 품질 향상을 위해 서면 승낙하는 특수 조건 하에 제한적 허용.</p>
                </div>

                <div class="border-l-4 border-gray-600 bg-gray-50 p-5 rounded-r-xl shadow-md">
                    <h3 class="text-xl font-bold text-gray-900 mb-3">⚠️ 재하도급 행위의 원칙적 금지 (제29조 제3항)</h3>
                    <p class="text-gray-900 mb-3 font-semibold text-lg">"하수급인은 자신이 도급받은 건설공사를 제3자에게 다시 위탁(재하도급)할 수 없다."</p>
                    <p class="text-sm text-gray-900 mb-4 leading-relaxed">불법 다단계 하도급 관행이 야기하는 최종 작업자의 안전 위협과 공사비 부족으로 인한 부실시공을 원천 금지합니다.</p>
                    
                    <div class="bg-white p-4 rounded-lg border border-gray-200">
                        <strong class="text-gray-900 block mb-2 border-b border-gray-200 pb-1">적법한 재하도급의 성립 요건 (아래 항목 전부 충족 요건):</strong>
                        <ul class="list-none pl-1 mt-2 text-sm text-gray-900 space-y-2">
                            <li class="flex items-center gap-2"><span class="text-gray-900">①</span> 시공상 '전문적인 지식, 신기술, 특허' 등이 고도로 요구되는 공종일 것.</li>
                            <li class="flex items-center gap-2"><span class="text-gray-900">②</span> 해당 신기술 또는 전문성을 갖춘 합법적 등록업자에게 위탁할 것.</li>
                            <li class="flex items-center gap-2"><span class="text-gray-900">③</span> 재하도급 부분의 공사 금액이 재위탁 대상 공사 전체 도급액의 <strong>20% 이내</strong>일 것.</li>
                            <li class="flex items-center gap-2"><span class="text-gray-900">④</span> 사전에 <strong>발주자 및 수급인(원청)으로부터 '서면 승낙'</strong>을 득할 것.</li>
                        </ul>
                    </div>
                </div>
            </div>

            <h3 class="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2">직접 시공 의무 (제28조의2)</h3>
            <p class="text-gray-900 mb-4 leading-relaxed">건설업 종사자의 건전한 시공 능력 보증 및 하도급 의존도를 낮추기 위해, 예정 공사금액 구간별로 종합건설사업자는 <strong>자사의 기술인력과 자재 등을 동원해 일정 비율 이상을 직접 시공</strong>해야 할 법적 의무가 부여됩니다.</p>
            <div class="overflow-hidden bg-white rounded-xl border border-gray-200 shadow-sm text-sm mb-4">
                <table class="w-full text-center border-collapse">
                    <thead class="bg-gray-100 text-gray-900">
                        <tr><th class="p-4 border-b w-1/2">도급 예정 금액</th><th class="p-4 border-b">직접시공 의무비율</th></tr>
                    </thead>
                    <tbody class="divide-y divide-gray-200 text-gray-900">
                        <tr class="hover:bg-gray-50"><td class="p-4">3억원 미만</td><td class="p-4 font-bold text-gray-900">50% 이상</td></tr>
                        <tr class="hover:bg-gray-50"><td class="p-4">3억원 이상 ~ 10억원 미만</td><td class="p-4 font-bold text-gray-900">30% 이상</td></tr>
                        <tr class="hover:bg-gray-50"><td class="p-4">10억원 이상 ~ 30억원 미만</td><td class="p-4 font-bold text-gray-900">20% 이상</td></tr>
                        <tr class="hover:bg-gray-50"><td class="p-4">30억원 이상 ~ 70억원 미만</td><td class="p-4 font-bold text-gray-900">10% 이상</td></tr>
                        <tr class="bg-gray-50"><td class="p-4">70억원 이상</td><td class="p-4">적용 제외 (자율 시공)</td></tr>
                    </tbody>
                </table>
            </div>''',
            3
        ),
        (
            '4. [건산법 도급/하도급-2] 불공정 행위 금지 및 대금 직불 보장', 
            '''<h2 class="text-3xl font-extrabold mb-6 text-gray-900 border-b-2 border-slate-200 pb-3">공정거래 질서 확립과 하도급 대금 지급 보증체계</h2>
            <p class="text-lg text-gray-900 mb-8 leading-relaxed">수급사업자의 적정 이윤 보호와 <strong>노무비(임금) 채권의 절대적 보장</strong>, 도산에 따른 파생 피해 방지를 위한 제도적 안전망입니다.</p>
            
            <h3 class="text-xl font-bold text-gray-900 bg-gray-100 py-2 px-4 rounded-t-lg border-x border-t border-gray-300">1. 부당한 하도급대금 산정 금지 (제38조)</h3>
            <div class="border-x border-b border-gray-300 p-5 rounded-b-lg mb-8 bg-white shadow-sm">
                <p class="text-gray-900 mb-4 leading-relaxed text-sm">도급인은 우월적 지위를 남용하여 수급인에게 통상적인 도급 단가에 현저히 미달하는 하도급 대금을 강요할 수 없습니다.</p>
                <div class="bg-gray-50 p-4 border border-gray-200 rounded text-sm text-gray-900">
                    <strong class="text-gray-900 flex items-center gap-1 mb-2"><span>🔍</span> 발주자의 하도급 적정성 심사 의무 (제82조):</strong>
                    하도급 계약 금액이 도급액 내역 대비 <strong>82%</strong>에 미달하거나, 발주자 기준 예정가격의 <strong>60%</strong>에 미달하는 경우, 발주자는 해당 하도급 계약의 적정성 및 시공 능력을 평가위원을 통해 의무적으로 심사하여야 하며 하수급인의 변경을 수급인에게 요구할 권한을 가집니다.
                </div>
            </div>

            <h3 class="text-xl font-bold text-gray-900 bg-gray-100 py-2 px-4 rounded-t-lg border-x border-t border-gray-300 mt-6 flex justify-between items-center">
                <span>2. 하도급대금 직접 지급 사유 (제35조)</span>
                <span class="text-xs bg-gray-200 text-gray-900 px-2 py-1 rounded font-bold">대금 직불 제도</span>
            </h3>
            <div class="border-x border-b border-gray-300 p-6 rounded-b-lg mb-8 bg-white shadow-sm">
                <p class="text-gray-900 mb-5 leading-relaxed text-sm">일반적인 공사 대금은 발주자에서 우선 수급인으로 이전되나, 수급인의 지불 불능 사태에 대비하여 법령에 규정된 요건 성립 시 <strong>발주자가 하수급인에게 대금을 '직접 지불'하도록</strong> 강력한 보장 제도를 도입하고 있습니다.</p>
                
                <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
                    <div class="bg-gray-50 border border-gray-200 p-5 rounded-xl">
                        <h4 class="font-bold text-base text-gray-900 mb-3 border-b border-gray-200 pb-2">발주자 직접 지급 인용 필수 요건</h4>
                        <ul class="list-disc pl-5 space-y-2 text-sm text-gray-900 font-medium">
                            <li>발주자, 수급인, 하수급인 3자 간 하도급대금 직접 지급에 관한 '사전 합의서'를 작성한 경우.</li>
                            <li>수급인이 <strong>2회 이상의 하도급대금 지급 지체 사실</strong>이 발생한 경우.</li>
                            <li>수급인의 파산, 부도, 등록취소 등으로 인하여 <strong>계약상 대금 지급 능력이 현저히 상실</strong>된 경우.</li>
                            <li>수급인이 하도급대금 지급보증서의 교부 의무를 불이행한 경우.</li>
                        </ul>
                    </div>
                    
                    <div class="bg-gray-50 border border-gray-200 p-5 rounded-xl">
                        <h4 class="font-bold text-base text-gray-900 mb-3 border-b border-gray-200 pb-2">건설기계 대여대금 지급보증 의무 (제68조의3)</h4>
                        <p class="text-sm text-gray-900 mb-3 leading-relaxed">건설 현장에서 사용되는 장비나 기계 대여업자의 대금 보호를 위해, 체결 시마다 수급인은 <strong>장비대여금 지급보증서</strong> 발급 비용을 전액 부담하여 필수적으로 교부하여야 합니다.</p>
                        <p class="text-xs p-2 bg-gray-200 text-gray-900 rounded font-semibold">보증서 미교부 또는 체불 사실이 접수될 경우 행정처분 사유에 해당합니다.</p>
                    </div>
                </div>
            </div>

            <h3 class="text-xl font-bold text-gray-900 bg-gray-100 py-2 px-4 rounded-t-lg border-x border-t border-gray-300 mt-6 flex justify-between items-center">
                <span>3. 노무비(임금)에 대한 압류의 절대적 금지 (제88조)</span>
                <span class="text-xs bg-gray-200 text-gray-900 px-2 py-1 rounded font-bold">노임 권익 보호</span>
            </h3>
            <div class="border-x border-b border-gray-300 p-6 rounded-b-lg mb-8 bg-white shadow-sm">
                <p class="text-gray-900 mb-4 leading-relaxed">건설사업자의 재정 악화로 제3의 채권자가 채권을 가압류하려는 절차를 개시하더라도, 도급금액 구성 성분 중 <strong>"근로자의 임금에 명백히 해당하는 노임 상당액"</strong>에 대해서는 제3자가 강제집행이나 압류를 진위할 수 없습니다.</p>
                <div class="flex items-start gap-3 bg-gray-50 p-4 rounded-lg border border-gray-200">
                    <span class="text-xl mt-1">📝</span>
                    <p class="text-sm text-gray-900 leading-relaxed"><strong>실무 적용 방안:</strong> 향후 근로자의 권익을 두텁게 보호하기 위해서는 공사 도급계약서 및 산출내역서 상에 <strong>'직접 노무비'와 다른 구성 요소(재료비 및 기타 경비)의 산출 근거를 엄격히 분리하여 기재</strong>하여야 하며, 법원 및 관청 통보 시 이를 근거문서로 소명하여야 합니다.</p>
                </div>
            </div>''',
            4
        ),
        (
            '5. [건산법 현장관리] 현장대리인 지정, 전자카드제 및 표지 실명제', 
            '''<h2 class="text-3xl font-extrabold mb-6 text-gray-900 border-b-2 border-slate-200 pb-3">안전한 건설공사 수행을 위한 체계적 현장 통제</h2>
            <p class="text-lg text-gray-900 mb-8 leading-relaxed">법률에 근거한 적격 <strong>건설기술인(현장대리인)</strong>의 선임과, 공사 현장 내 종사자의 체계적 관리를 지원하는 <strong>전자카드제</strong> 등이 현장 관리의 주축을 이룹니다.</p>
            
            <h3 class="text-xl font-bold text-gray-900 border-l-4 border-gray-600 pl-3 mb-4">1. 건설기술인(현장대리인)의 배치 의무 (제40조)</h3>
            <p class="text-gray-900 mb-4 text-sm leading-relaxed">건설사업자는 당해 공사의 특성 및 규모에 부합하는 적격 <strong>분야 및 기술 등급(초급~특급 등)</strong>을 소지한 건설기술인을 1명 이상 현장마다 의무적으로 현장대리인으로 배치하여야 합니다.</p>
            
            <div class="bg-gray-50 border border-gray-300 rounded-xl p-6 mb-8 shadow-sm">
                <h4 class="font-bold text-gray-900 text-lg mb-3 flex items-center gap-2"><span>법적 이행사항:</span> 이탈의 금지 및 중복 선임 엄격 제한</h4>
                <ul class="list-disc pl-5 space-y-3 text-sm text-gray-900">
                    <li><strong class="text-gray-900">상주 유지 의무:</strong> 선임된 건설기술인은 발주자 또는 감리인의 사전 서면 동의를 얻은 특별한 질병, 교육 예외 사항 외에는 <strong>정당한 사유 없이 해당 건설 현장을 이탈할 수 없습니다.</strong></li>
                    <li><strong class="text-gray-900">단일 관장 원칙:</strong> 안전 및 품질 감독 권한의 약화 방지를 위해 원칙적으로 1인의 건설기술인은 하나의 현장에 전속적으로 소속되어 통제 업무를 수행해야 합니다.</li>
                    <li><strong class="text-gray-900">예외 조항 (영세 현장의 예외):</strong> 예정금액이 일정 규모(예: 5억 원) 미만인 동일 권역 내 현장에 한정하여, 발주자 전원의 승낙을 득한 경우 최대 3곳까지 중복하여 현장 관리 업무를 포괄 배분할 수 있습니다. (허위 기재 방지 필요)</li>
                </ul>
            </div>

            <h3 class="text-xl font-bold text-gray-900 border-l-4 border-gray-600 pl-3 mb-4">2. 투명한 노무관리를 위한 건설근로자 전자카드제 전면화</h3>
            <p class="text-gray-900 mb-3 text-sm leading-relaxed">하도급 구조상 빈번히 제기되어 온 노무 인력 정보의 오기 및 미보고를 예방하고 투명한 퇴직보증 환경을 조성하고자 제정된 절차입니다. 2024년 이후 민간을 포함한 대부분의 건설 현장으로 확대 적용 중입니다.</p>
            <div class="bg-white border border-gray-200 p-5 rounded-lg mb-8 shadow-sm text-sm text-gray-900">
                <ul class="list-none space-y-2">
                    <li class="flex gap-2"><span class="text-gray-600">✔️</span> 사업주는 단말기를 지정 구역에 설치하고, 하수급인 소속 근로자를 포함한 <strong>전체 현장 출입자가 본인의 전자카드를 통하여 정확한 근로 일수를 기록</strong>하도록 통제할 의무가 있습니다.</li>
                    <li class="flex gap-2"><span class="text-gray-600">✔️</span> 생성된 출입 및 노무 정보는 전자 시스템 내로 전송되며, 사업주는 이를 근거로 일체화된 <strong>정확한 통계 및 적법한 퇴직공제부금</strong>을 처리하여야 합니다.</li>
                </ul>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                <div class="border border-gray-200 p-5 rounded-lg shadow-sm">
                    <h3 class="text-lg font-bold text-gray-900 mb-2 border-b pb-2">3. 건설공사 현장 표지의 게시 (실명제 강화)</h3>
                    <p class="text-sm text-gray-900 leading-relaxed">도급인은 착공일로부터 당해 시설물이 준공될 때까지 외부의 식별이 용이한 정문 주변에, 수급인, 주요 하수급인, 설계담당사, 감리자 및 사업 주체의 성명과 연락처가 상세히 기록된 <strong>표지판(현장 알림판)</strong>을 상시적으로 보존해야 합니다. 법령 기준 미조치 시 제재가 가해집니다.</p>
                </div>
                
                <div class="border border-gray-200 bg-gray-50 p-5 rounded-lg shadow-sm">
                    <h3 class="text-lg font-bold text-gray-900 mb-2 border-b pb-2">4. 건설 하도급 사항 통보 의무 (KISCON)</h3>
                    <p class="text-sm text-gray-900 leading-relaxed">발주자의 감독권 보장 및 투명화 정책의 일환으로, 계약 당사자는 도급 약정 성립 혹은 하도급 업체 지정 후 관련 세부 정보를 <strong>기한(체결일로부터 30일 이내) 내에 KISCON(건설산업지식정보시스템)에 등재하고 이를 통보</strong>하여 현황 집계를 가능케 해야 합니다.</p>
                </div>
            </div>''',
            5
        )
    ]
    
    for title, content, order in lessons:
         cursor.execute('''
            INSERT INTO lesson (title, content, "order", course_id)
            VALUES (?, ?, ?, ?)
        ''', (title, content, order, course_id))
        
    conn.commit()
    conn.close()
    print("[건산법 중심 1강~5강 전문화 완료] 데이터베이스 테이블 시딩 완료")

if __name__ == '__main__':
    seed_law_course_ultimate()
