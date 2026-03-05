import sqlite3
import os

def seed_law_course_ultimate():
    db_path = os.path.join(os.path.dirname(__file__), '..', 'database.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM category WHERE name = '법무관련'")
    row = cursor.fetchone()
    if not row:
        cursor.execute("INSERT INTO category (name, \"order\") VALUES ('법무관련', 3)")
        category_id = cursor.lastrowid
    else:
        category_id = row[0]

    course_title = '[건설법규]'
    thumbnail_path = '/static/uploads/law_thumbnail.png'
    
    cursor.execute('SELECT id FROM course WHERE title = ?', (course_title,))
    row = cursor.fetchone()
    if row:
        course_id = row[0]
        cursor.execute("DELETE FROM lesson WHERE course_id = ?", (course_id,))
        cursor.execute('''
            UPDATE course 
            SET description = '건설산업기본법(건산법)을 완벽 해부하는 10강 체제 궁극의 실무 매뉴얼. 하도급법, 도급계약서, 중처법 가이드까지 현장 공무/소장 필수 지침서.',
                thumbnail_url = ?, category_id = ? 
            WHERE id = ?
        ''', (thumbnail_path, category_id, course_id))
    else:
        cursor.execute('''
            INSERT INTO course (title, description, thumbnail_url, category_id) 
            VALUES (?, ?, ?, ?)
        ''', (course_title, "건설산업기본법(건산법)을 완벽 해부하는 10강 체제 궁극의 실무 매뉴얼. 하도급법, 도급계약서, 중처법 가이드까지 현장 공무/소장 필수 지침서.", thumbnail_path, category_id))
        course_id = cursor.lastrowid

    lessons = [
        (
            '1. [건산법 총칙] 건설산업기본법의 목적과 적용 범위', 
            '''<h2 class="text-2xl font-bold mb-4">건설산업기본법(건산법)이란 무엇인가?</h2>
            <div class="bg-blue-50 border border-blue-200 p-6 rounded-xl shadow-lg mb-8">
                <p class="text-lg leading-relaxed text-blue-900">건설산업기본법(이하 건산법)은 대한민국 건설공사의 조사, 설계, 시공, 감리, 유지관리 등 <strong>건설업에 관한 기본적인 사항과 건설업의 등록, 건설공사의 도급 등에 관한 기준</strong>을 명확히 정하여 건설공사의 적정한 시공과 건설산업의 건전한 발전을 도모함을 목적으로 하는 최상위 기본법입니다.</p>
            </div>
            
            <h3 class="text-xl font-bold text-gray-800 border-l-4 border-blue-600 pl-3 mb-4">1.1. 주요 용어의 정의 (제2조)</h3>
            <div class="overflow-x-auto bg-white rounded-lg shadow border border-gray-200 mb-8">
                <table class="w-full text-left border-collapse">
                    <thead>
                        <tr class="bg-gray-100 text-gray-800 text-sm">
                            <th class="p-4 border-b font-bold w-1/4">용어</th>
                            <th class="p-4 border-b font-bold">건산법상 정의 및 해석</th>
                        </tr>
                    </thead>
                    <tbody class="text-sm">
                        <tr class="border-b hover:bg-gray-50">
                            <td class="p-4 font-semibold text-blue-900">건설산업</td>
                            <td class="p-4 text-gray-700">건설업과 건설용역업을 말합니다.</td>
                        </tr>
                        <tr class="border-b hover:bg-gray-50">
                            <td class="p-4 font-semibold text-blue-900">건설공사</td>
                            <td class="p-4 text-gray-700">토목공사, 건축공사, 산업설비공사, 조경공사, 환경시설공사 등 시설물을 설치·유지·보수하는 공사. <strong>주의:</strong> 전기공사, 정보통신공사, 소방시설공사, 문화재수리공사는 건산법의 건설공사에 포함되지 않으며 각각 개별법의 적용을 받습니다.</td>
                        </tr>
                        <tr class="border-b hover:bg-gray-50">
                            <td class="p-4 font-semibold text-blue-900">도급 / 하도급</td>
                            <td class="p-4 text-gray-700"><strong>도급:</strong> 발주자와 수급인 간, 또는 수급인과 하수급인 간에 수급인이 일의 완성을 약정하고 상대방이 그 결과에 대해 대가를 지급할 것을 약정하는 계약.<br><strong>하도급:</strong> 도급받은 건설공사의 전부 또는 일부를 다시 도급하기 위하여 수급인이 제3자와 체결하는 계약.</td>
                        </tr>
                        <tr class="hover:bg-gray-50">
                            <td class="p-4 font-semibold text-blue-900">발주자 / 수급인</td>
                            <td class="p-4 text-gray-700"><strong>발주자:</strong> 건설공사를 건설사업자에게 도급하는 자 (자가 시공 제외).<br><strong>수급인(원도급자):</strong> 발주자로부터 건설공사를 도급받은 건설사업자.</td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <h3 class="text-xl font-bold text-gray-800 border-l-4 border-blue-600 pl-3 mb-4">1.2. 타 법률와의 관계 (제3조)</h3>
            <p class="text-gray-700 mb-4 text-base">건산법은 건설산업에 관하여 다른 법률에 우선하여 적용되는 <strong>일반법(기본법)</strong>의 지위를 가집니다. 단, 전기, 통신, 소방 등 타 법률에 특별한 규정이 있는 경우 그 법률을 따릅니다. 공정거래 측면에서는 '하도급거래 공정화에 관한 법률(하도급법)'이 건산법에 우선하는 특별법적 성격을 띱니다.</p>
            
            <div class="bg-blue-50 p-5 rounded border border-blue-200 mt-6">
                <h4 class="font-bold text-blue-800 mb-2">💡 실무 팁: 분리 발주의 원칙</h4>
                <p class="text-sm text-gray-800">건산법상 건설공사와 전기공사/정보통신공사는 한꺼번에 도급을 줄 수 없고 반드시 <strong>분리 발주</strong>해야 합니다. 이를 어기고 건설사가 전기/통신까지 일괄 수주하여 하도급을 주면 해당 개별법 위반으로 처벌받게 됩니다. 아파트 현장에서 골조 공사와 전기 배선 공사의 계약 주체가 다른 이유가 바로 이 법령 때문입니다.</p>
            </div>''', 
            1
        ),
        (
            '2. [건산법 등록] 건설업의 등록체계 및 결격사유', 
            '''<h2 class="text-2xl font-bold mb-4">건설업 면허 체계: 자격 없는 자의 시공을 막아라</h2>
            <p class="text-lg text-gray-700 mb-6">부실시공을 예방하기 위한 첫 번째 관문이 바로 <strong>"건설업 등록제도"</strong>입니다.</p>
            
            <h3 class="text-xl font-bold text-gray-800 border-b-2 border-gray-200 pb-2 mb-4">2.1. 건설업의 종류 및 등록 (제9조)</h3>
            <p class="text-gray-700 mb-4">건설업은 <strong>종합공사를 시공하는 업종(종합건설업)</strong>과 <strong>전문공사를 시공하는 업종(전문건설업)</strong>으로 나뉩니다. 건설업을 영위하려는 자는 업종별로 자본금, 기술능력(기술자 수), 사무실 및 장비 시설을 갖추어 국토교통부장관이나 시/도지사(시/군/구청장)에게 등록해야 합니다.</p>
            
            <div class="grid md:grid-cols-2 gap-4 mb-8">
                <div class="border p-4 rounded bg-white shadow-sm border-gray-300">
                    <h4 class="font-bold text-indigo-800 mb-2 truncate">🏗️ 종합건설업 (5개 업종)</h4>
                    <ul class="text-sm text-gray-700 list-disc pl-5">
                        <li>건축공사업 (자본금 3.5억 이상)</li>
                        <li>토목공사업 (자본금 5억 이상)</li>
                        <li>토목건축공사업 (자본금 8.5억 이상, 기술자 11인)</li>
                        <li>산업설비공사업</li>
                        <li>조경공사업</li>
                    </ul>
                </div>
                <div class="border p-4 rounded bg-white shadow-sm border-gray-300">
                    <h4 class="font-bold text-teal-800 mb-2 truncate">🛠️ 전문건설업 (29개 업종 - 대업종화됨)</h4>
                    <p class="text-sm text-gray-700 mb-2">2022년 시행령 개정으로 유사 업종이 대업종으로 통합되었습니다.</p>
                    <ul class="text-sm text-gray-700 list-disc pl-5">
                        <li>지반조성·포장공사업</li>
                        <li>실내건축공사업</li>
                        <li>금속·창호·지붕·건축물조립공사업</li>
                        <li>철근·콘크리트공사업 등</li>
                    </ul>
                </div>
            </div>
            
            <div class="bg-red-50 p-5 rounded border border-red-200 mb-8">
                <h4 class="font-bold text-red-800 text-lg mb-2">🚨 경미한 건설공사 (무면허 허용 기준)</h4>
                <p class="text-sm text-gray-800 mb-3">다음의 경미한 공사는 예외적으로 건설업 등록(면허) 없이도 시공이 가능합니다.</p>
                <ul class="text-sm font-semibold text-red-900 list-disc pl-5 space-y-1">
                    <li><strong>종합공사:</strong> 공사예정금액 <strong>5천만원 미만</strong>의 건설공사</li>
                    <li><strong>전문공사:</strong> 공사예정금액 <strong>1천5백만원 미만</strong>의 건설공사</li>
                </ul>
                <p class="text-xs text-red-700 mt-2">※ 단, 방수공사 등 일부 공종과 가스시설공사, 철강재설치공사 등은 금액에 상관없이 아무나 해서는 안되며 반드시 면허가 필요합니다. 또한 금액을 쪼개서 (분할발주) 1,500만원 미만으로 맞추는 꼼수도 합산하여 계산되므로 처벌 대상입니다.</p>
            </div>

            <h3 class="text-xl font-bold text-gray-800 border-b-2 border-gray-200 pb-2 mb-4">2.2. 무면허 시공 및 명의대여의 처벌 (제21조)</h3>
            <p class="text-gray-700 mb-4">건설업자가 다른 사람에게 자신의 성명이나 상호를 사용하여 건설공사를 수급/시공하게 하거나 건설업 등록증이나 등록수첩을 빌려주는 행위(일명 '면허 대여')는 건산법상 가장 <strong>질이 나쁜 중대 범죄</strong>로 취급됩니다.</p>
            <div class="bg-gray-100 border border-gray-300 p-4 rounded mt-2 shadow">
                <p class="text-sm text-gray-800"><strong class="text-gray-900">벌칙 규정 (제96조):</strong> 무등록 시공자, 명의대여자, 명의차용자, 명의대여 알선자 모두 <strong class="text-red-600">5년 이하의 징역 또는 5천만원 이하의 벌금</strong>에 처합니다. (기존 3년/3천만원에서 대폭 강화됨) + 해당 건설업자는 즉시 필요적 등록 말소됩니다.</p>
            </div>''',
            2
        ),
        (
            '3. [건산법 도급/하도급-1] 도급의 원칙과 하도급 제한', 
            '''<h2 class="text-2xl font-bold mb-4">건설공사 도급계약 및 하도급의 대원칙</h2>
            <p class="text-lg text-gray-700 mb-6">현장 소장들이 가장 많이 위반하여 행정명령을 받는 파트입니다. <strong>다단계 하도급(피라미드 구조)을 금지</strong>하여 중간 착취액을 없애고 품질을 보장하는 것이 목적입니다.</p>
            
            <h3 class="text-xl font-bold text-red-700 mb-4">1. 일괄 하도급의 절대 금지 (제29조 1항)</h3>
            <p class="text-gray-800 mb-3">건설사업자는 도급받은 건설공사의 <strong>전부(또는 주요 부분의 대부분)를 다른 건설사업자에게 일괄하여 하도급할 수 없습니다.</strong> 자기는 서류만 만지고 중간에 수수료 마진만 먹는 이른바 '페이퍼 컴퍼니(브로커)'를 근절하기 위함입니다.</p>
            <div class="bg-gray-100 p-4 border-l-4 border-red-500 mb-8 rounded text-sm text-gray-700">
                <strong>일괄하도급 예외 허용 기준:</strong> 발주자가 서면으로 승낙하고, 도급받은 공사를 2인 이상에게 분할하여 하도급하는 경우로서, 공사의 품질과 효율성을 위해 불가피한 제한적 경우에만 허용됩니다.
            </div>

            <h3 class="text-xl font-bold text-orange-700 mb-4">2. 동일 업종간 하도급 제한 (제29조 2항)</h3>
            <p class="text-gray-800 mb-3">종합건설업자는 도급받은 종합공사를 다른 종합건설업자에게, 전문건설업자는 전문공사를 다른 전문건설업자에게 하도급할 수 없습니다. (종합 &rarr; 종합 금지, 전문 &rarr; 전문 금지)</p>
            <p class="text-sm text-gray-600 mb-8">※ 예외: 발주자가 공사품질이나 시공상 능률을 높이기 위해 서면 승낙한 경우 등 매우 까다로운 예외 요건을 갖춰야 가능합니다.</p>

            <h3 class="text-xl font-bold text-yellow-600 mb-4">3. 재하도급(손자 하도급)의 원칙적 금지 (제29조 3항)</h3>
            <div class="p-5 border border-yellow-300 bg-yellow-50 rounded mb-8">
                <p class="text-gray-800 mb-3 font-semibold">"하수급인(하청)은 하도급받은 공사를 다른 사람에게 다시 재하도급(재하청)할 수 없다."</p>
                <p class="text-sm text-gray-700 mb-2">원청에서 100원에 받은 공사를 하청이 80원에 받고, 하청이 다시 십장이나 다른 업체에게 60원에 넘기는 행위를 막기 위한 규정입니다.</p>
                <div class="mt-4 pt-3 border-t border-yellow-200">
                    <strong class="text-yellow-800">합법적인 재하도급 요건 (아래 요건을 모두 충족해야 함):</strong>
                    <ul class="list-disc pl-5 mt-2 text-sm text-gray-700 space-y-1">
                        <li>하도급받은 공사 중 '전문기술'이 필요한 공사에 한할 것 (가설재 설치 등은 안됨)</li>
                        <li>해당 전문업종을 등록한 재하수급인에게 줄 것</li>
                        <li><strong>하도급금액의 20% 이내</strong>의 소규모 공사일 것</li>
                        <li>사전에 <strong>발주자 및 수급인(원청)의 서면 승낙</strong>을 모두 받을 것</li>
                    </ul>
                </div>
            </div>

            <h3 class="text-xl font-bold text-green-700 mb-4">4. 직접 시공 의무 비율 (제28조의2)</h3>
            <p class="text-gray-800 mb-3">과거 종합건설사들이 100% 하도급만 주고 본인들은 관리만 하는 관행을 타파하기 위해 일정 비율을 무조건 직접 인력을 투입해 <strong>'직접 시공'</strong> 하도록 강제하고 있습니다.</p>
            <div class="bg-white rounded border border-gray-200 shadow-sm p-4 overflow-x-auto text-sm">
                <table class="w-full text-left">
                    <thead>
                        <tr class="bg-gray-100"><th class="p-2 border-b">도급 금액</th><th class="p-2 border-b">직접시공 의무비율</th></tr>
                    </thead>
                    <tbody>
                        <tr><td class="p-2 border-b">3억원 미만</td><td class="p-2 border-b font-bold text-green-700">50% 이상</td></tr>
                        <tr><td class="p-2 border-b">3억원 ~ 10억원 미만</td><td class="p-2 border-b font-bold text-green-700">30% 이상</td></tr>
                        <tr><td class="p-2 border-b">10억원 ~ 30억원 미만</td><td class="p-2 border-b font-bold text-green-700">20% 이상</td></tr>
                        <tr><td class="p-2 border-b">30억원 ~ 70억원 미만</td><td class="p-2 border-b font-bold text-green-700">10% 이상</td></tr>
                        <tr><td class="p-2 text-gray-500">70억원 이상</td><td class="p-2 text-gray-500">의무 없음 (자율)</td></tr>
                    </tbody>
                </table>
            </div>''',
            3
        ),
        (
            '4. [건산법 도급/하도급-2] 불공정 행위 금지 및 대금의 보호', 
            '''<h2 class="text-2xl font-bold mb-4">원청의 갑질 방지와 하도급 대금의 절대적 보호</h2>
            <p class="text-lg text-gray-700 mb-6">건산법은 하도급계약 과정에서의 불공정 행위를 금지하고, 특히 <strong>노임(인건비) 및 자재/장비대금 체불을 막기 위한 강력한 직불 조항</strong>을 두고 있습니다.</p>
            
            <h3 class="text-xl font-bold text-blue-800 border-l-4 border-blue-600 pl-3 mb-4">1. 부당한 하도급대금 결정 금지 (제38조)</h3>
            <p class="text-gray-800 mb-3">수급인은 하도급대금을 원도급 내역 대비 턱없이 낮게 깎을 수 없습니다.</p>
            <div class="bg-red-50 p-4 border border-red-200 rounded text-sm text-gray-800 mb-6">
                <strong>하도급 적정성 심사 (제82조):</strong>
                발주자는 하수급인이 시공하기에 부적당하다고 인정되거나, 하도급금액이 도급금액 중 하도급부분에 상당하는 금액의 <strong>82%</strong>에 미달하는 경우, 또는 발주자의 예정가격 대비 <strong>60%</strong>에 미달하는 경우 그 수급인을 심사하여 시공을 막거나 하수급인을 변경하도록 요구할 수 있습니다. (이른바 저가 하도급 방지)
            </div>

            <h3 class="text-xl font-bold text-blue-800 border-l-4 border-blue-600 pl-3 mb-4">2. 하도급대금의 직접 지급 의무 (제35조) - 👑 실무 핵심</h3>
            <p class="text-gray-800 mb-4">보통 발주자 &rarr; 원청 &rarr; 하청 순서로 자금이 흐르지만, 원청이 이 돈을 다른 빚을 갚는데 유용하거나 파산해버리면 하청은 줄도산하게 됩니다. 이를 막기 위해 <strong>직불(직접 지불)</strong> 제도를 운영합니다.</p>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                <div class="bg-white border border-gray-300 p-5 rounded-lg shadow-sm">
                    <h4 class="font-bold text-lg text-indigo-700 mb-3">발주자가 <span class="bg-indigo-100 px-1">반드시 하청에 직접 줘야하는</span> 경우</h4>
                    <ul class="list-disc pl-5 space-y-2 text-sm text-gray-700">
                        <li>원청이 파산, 부도, 영업정지 등으로 결제 능력을 상실한 경우</li>
                        <li>원청이 <strong>2회 이상 하도급대금 지급을 지체</strong>한 경우</li>
                        <li>국가, 지자체 등 공공공사 발주자가 직접 지급하기로 하청 및 원청과 미리 합의한 경우</li>
                        <li>하도급대금 지급보증서를 원청이 교부하지 않은 경우</li>
                    </ul>
                </div>
                <div class="bg-white border border-gray-300 p-5 rounded-lg shadow-sm">
                    <h4 class="font-bold text-lg text-teal-700 mb-3">건설기계 대여대금 지급보증 (제68조의3)</h4>
                    <p class="text-sm text-gray-700 mb-2">포크레인, 크레인 등 장비사업자의 체불을 막기 위해 수급인(건설사)은 기계 대여업자에게 <strong>장비대금 지급보증서</strong>를 반드시 줘야 합니다. (단, 건당 200만원 이하 등 소액 예외)</p>
                    <p class="text-sm font-bold text-red-600">위반시 기계 대여업자는 시/군/구청에 직접 신고 가능하며, 건설사는 영업정지 또는 과징금 처분을 받게 됩니다.</p>
                </div>
            </div>

            <h3 class="text-xl font-bold text-blue-800 border-l-4 border-blue-600 pl-3 mb-4">3. 노임(임금)에 대한 압류 금지 (제88조)</h3>
            <p class="text-gray-800 mb-3">건설사업자가 부도가 나서 채권자들이 압류를 걸더라도, 도급금액 중 <strong>"근로자의 임금(노임단가 등)에 해당하는 금액"</strong>은 법적으로 압류할 수 없습니다. 즉, 근로자 인건비는 어떤 상황에서도 보호받는 최우선 과제입니다.</p>
            <p class="text-sm text-gray-600 bg-gray-100 p-3 rounded">실무적으로 계약 체결 시 산출내역서 상에 '노임부분'을 별도로 명확히 기재해야 이 법의 보호를 쉽게 받을 수 있습니다.</p>
            ''',
            4
        ),
        (
            '5. [건산법 시공관리] 현장대리인과 품질/안전 관리', 
            '''<h2 class="text-2xl font-bold mb-4">시공관리와 건설기술인(현장소장)의 배치</h2>
            <p class="text-lg text-gray-700 mb-6">모든 건설현장에는 법이 정한 자격과 등급을 갖춘 <strong>현장대리인(건설기술인)</strong>이 상주해야 하며, 이들이 제대로 관리하지 않으면 공사 자체가 중지될 수 있습니다.</p>
            
            <h3 class="text-xl font-bold text-gray-900 border-b-2 border-gray-300 pb-2 mb-4">1. 건설기술인의 배치 의무 (제40조)</h3>
            <p class="text-gray-800 mb-4">건설사업자는 공사현장의 공정, 안전, 품질 관리를 위해 <strong>해당 공종에 맞는 분야 및 등급(초급, 중급, 고급, 특급)의 건설기술인 1명 이상</strong>을 배치해야 합니다.</p>
            
            <div class="bg-yellow-50 border-l-4 border-yellow-500 p-5 mb-6 text-sm text-gray-800">
                <h4 class="font-bold text-yellow-800 text-lg mb-2">🚧 무단 이탈 금지 및 중복 배치 제한</h4>
                <ul class="list-disc pl-5 space-y-2">
                    <li>배치된 기술인은 발주자의 승낙 없이 <strong>절대 현장을 무단으로 이탈해서는 안 됩니다.</strong></li>
                    <li><strong>1인 1현장 원칙:</strong> 원칙적으로 1명의 현장소장은 1개의 현장만 맡아야 합니다.</li>
                    <li><strong>예외 (중복 배치 허용):</strong> 공사예정금액이 5억원 미만인 동일 시/군 내의 현장 3개까지는 발주자의 승인을 얻어 1명이 관리할 수 있습니다. (3억 미만은 5개까지) 이것을 어기고 '면허 대여 현장'에서 이름만 올려두면 자격증이 취소됩니다.</li>
                </ul>
            </div>

            <h3 class="text-xl font-bold text-gray-900 border-b-2 border-gray-300 pb-2 mb-4">2. 표지의 게시 (제42조)</h3>
            <p class="text-gray-800 mb-3">착공과 동시에 발주자, 설계자, 시공자(원청 및 하청 포함), 감리자, 현장소장의 실명이 기재된 <strong>'건설공사 표지판'</strong>을 공사현장 입구의 눈에 잘 띄는 곳에 설치해야 합니다. (실명제 강화)</p>

            <h3 class="text-xl font-bold text-gray-900 border-b-2 border-gray-300 pb-2 mb-4">3. 하도급 관리계획의 통보 (제29조 4항)</h3>
            <div class="bg-gray-100 p-4 rounded text-sm text-gray-700">
                <p>일정규모(국가 공사 등) 이상의 공사를 수주한 종합건설사는 자신이 직접 시공할 부분과, 하도급을 줄 파트에 대해 <strong>'어떤 업체에 얼마에 하도급을 주겠다'는 하도급 관리계획서</strong>를 입찰 시 발주처에 제출하고 이행해야 합니다. 이를 지키지 않으면 벌점 및 계약 해지의 사유가 됩니다.</p>
                <p class="mt-2 text-red-600 font-semibold">특히 관급공사에서는 KISCON(건설산업지식정보시스템)에 계약 후 30일 이내에 원하도급 계약 내용, 현장소장 정보를 모든 의무적으로 입력(통보)해야 합니다 미통보시 과태료 부과 대상입니다.</p>
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
    print("[건산법 중심 1강~5강] 데이터베이스 테이블 시딩 완료")

if __name__ == '__main__':
    seed_law_course_ultimate()
