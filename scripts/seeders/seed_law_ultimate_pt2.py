import sqlite3
import os

def seed_law_course_ultimate_pt2():
    db_path = os.path.join(os.path.dirname(__file__), '..', 'database.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    course_title = '[건설법규]'
    cursor.execute('SELECT id FROM course WHERE title = ?', (course_title,))
    row = cursor.fetchone()
    if not row:
        print("Course not found, run pt1 first.")
        return
    course_id = row[0]

    lessons = [
        (
            '6. [하도급법-1] 하도급거래 공정화 법률의 적용과 서면발급', 
            '''<h2 class="text-2xl font-bold mb-4">하도급법의 보호 대상과 3대 불공정 행위 근절</h2>
            <p class="text-lg text-gray-700 mb-6">하도급법은 대기업(원청)의 갑질로부터 중소기업(하청)을 보호하기 위한 공정거래위원회의 강력한 무기입니다.</p>
            
            <h3 class="text-xl font-bold text-gray-800 border-l-4 border-blue-600 pl-3 mb-4">1. 하도급법 적용 대상 (누가 보호받는가?)</h3>
            <div class="bg-white border rounded shadow-sm p-5 mb-6">
                <ul class="space-y-3 text-sm text-gray-700">
                    <li><span class="inline-block w-24 font-bold text-blue-900">원사업자:</span> 중소기업이 아닌 사업자(대기업)이거나, 수급사업자보다 시공능력평가액(또는 연매출액)이 <strong>2배 이상 큰</strong> 중소기업.</li>
                    <li><span class="inline-block w-24 font-bold text-green-900">수급사업자:</span> 원사업자로부터 위탁을 받은 <strong>중소기업자</strong>. (※ 수급사업자가 대기업이면 하도급법 보호대상이 아닙니다.)</li>
                </ul>
                <p class="mt-4 p-3 bg-yellow-50 text-yellow-800 rounded border border-yellow-200">
                    <strong>주의:</strong> 단순히 건재상에서 시멘트를 사오는 "단순 자재구매"는 하도급법의 "건설위탁"이 아닙니다. 자재를 맞춤형으로 <strong>가공/제작</strong>하여 설치까지 하는 경우에만 하도급법이 적용됩니다.
                </p>
            </div>

            <h3 class="text-xl font-bold text-gray-800 border-l-4 border-blue-600 pl-3 mb-4">2. 선(先) 서면발급 의무 (제3조) - 입으로 지시 금지</h3>
            <p class="text-gray-800 mb-2">원사업자는 수급사업자가 <strong>작업(추가작업 포함)에 착수하기 전</strong>에 반드시 양 당사자가 서명/기명날인한 '계약서'를 발급해야 합니다.</p>
            <p class="text-gray-700 text-sm mb-4">"일단 공구리 쳐놔, 나중에 돈 줄게"라는 구두 지시는 하도급법 제3조 위반으로 원청이 과징금을 맞게 되는 1순위 사유입니다. 수급사업자는 반드시 작업 시작 전 <strong>"작업지시서(카톡, e메일, 작업일보 등)"</strong>를 증거로 남겨야 대금을 청구할 수 있습니다.</p>

            <h3 class="text-xl font-bold text-gray-800 border-l-4 border-blue-600 pl-3 mb-4">3. 부당특약의 금지 (제3조의4) - 계약서에 도장 찍어도 무효!</h3>
            <p class="text-gray-800 mb-3">수급사업자의 이익을 부당하게 침해하는 계약조건(특약)을 설정하는 행위는 절대 금지되며, 만약 <strong>계약서에 서명했더라도 그 조항은 사법상/공법상 원천 '무효'</strong>가 됩니다.</p>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                <div class="bg-red-50 border border-red-200 p-4 rounded text-sm">
                    <h4 class="font-bold text-red-800 mb-2">🚫 대표적인 부당특약 예시</h4>
                    <ul class="list-disc pl-5 text-gray-700 space-y-1">
                        <li>"현장에서 발생하는 모든 민원/소음 보상비용은 수급사업자가 책임진다."</li>
                        <li>"산업재해 발생 시 치료비와 합의금은 전액 하청이 부담한다."</li>
                        <li>"발주자의 도면 변경으로 인한 수량 증가분 중 10% 이하의 물량 변동은 대금을 증액하지 않는다."</li>
                        <li>"기상 악화로 인한 공기 지연의 책임과 지체상금은 모두 하청이 부담한다."</li>
                    </ul>
                </div>
                <div class="bg-green-50 border border-green-200 p-4 rounded text-sm text-gray-800">
                    <h4 class="font-bold text-green-800 mb-2">🛡️ 대처 방안</h4>
                    <p>착공 전 원청의 갑질 계약서를 받았다면, 일단 계약을 체결하여 일감을 확보하되, 추후 하자가 발생하거나 대금이 깎일 때 <strong>"이 조항은 하도급법 제3조의4에 따른 명백한 부당특약이므로 무효입니다"</strong>라는 내용증명을 띄우고 공정위에 신고하면 됩니다. 원청은 100% 패소합니다.</p>
                </div>
            </div>''',
            6
        ),
        (
            '7. [하도급법-2] 하도급대금의 결정 및 지급 보장', 
            '''<h2 class="text-2xl font-bold mb-4">대금 후려치기 방지와 신속한 결제 보장</h2>
            <p class="text-lg text-gray-700 mb-6">공사를 잘 해놓고 돈을 떼이는 것을 막기 위해 하도급법은 대금의 "결정-지급-직불" 전 과정을 촘촘히 규제합니다.</p>

            <h3 class="text-xl font-bold text-teal-800 border-b-2 border-teal-200 pb-2 mb-4">1. 부당한 하도급대금의 결정 금지 (제4조)</h3>
            <p class="text-gray-800 mb-3">정당한 이유 없이 일반적으로 지급되는 대가보다 현저하게 낮은 수준으로 대금을 인하하는 행위입니다. 특히, 경쟁입찰에 부친 후 <strong>최저가 낙찰 금액보다 더 낮은 금액(Nego)으로 계약을 강요</strong>하는 행위는 중대 범죄로 취급됩니다.</p>
            
            <h3 class="text-xl font-bold text-teal-800 border-b-2 border-teal-200 pb-2 mb-4">2. 하도급대금의 지급기한 (제13조) - "60일의 룰"</h3>
            <div class="flex flex-col md:flex-row gap-4 mb-6">
                <div class="bg-white border border-gray-300 rounded p-4 flex-1 shadow-sm">
                    <h4 class="font-bold text-gray-900 mb-2">기본 원칙</h4>
                    <p class="text-sm text-gray-700">원사업자는 목적물 수령일(기표, 준공청구일)로부터 <strong>가급적 짧은 기한으로 정한 60일 이내</strong>에 하도급 대금을 지급해야 합니다. (협의로 60일을 넘길 수 없음)</p>
                </div>
                <div class="bg-gray-100 border border-gray-300 rounded p-4 flex-1 shadow-sm">
                    <h4 class="font-bold text-gray-900 mb-2">발주자로부터 받은 경우</h4>
                    <p class="text-sm text-gray-700">원사업자가 발주자한테 기성이나 준공금을 받은 경우에는 <strong>받은 날로부터 15일 이내</strong>에 무조건 하수급인에게 돈을 넘겨야 합니다.</p>
                </div>
                <div class="bg-red-50 border border-red-200 rounded p-4 flex-1 shadow-sm">
                    <h4 class="font-bold text-red-800 mb-2">지연이자 및 어음할인료</h4>
                    <p class="text-sm text-gray-700">60일을 초과하여 지급할 때는 법정이자(연 15.5%)를, 어음으로 지급할 때는 어음할인료를 별도로 물어주어야 합니다.</p>
                </div>
            </div>

            <h3 class="text-xl font-bold text-teal-800 border-b-2 border-teal-200 pb-2 mb-4">3. 설계변경 등에 따른 하도급대금의 조정 (제16조)</h3>
            <p class="text-gray-800 mb-2">발주자가 설계변경이나 물가변동(ESC)을 이유로 원청의 도급금액을 증액해 주었다면, <strong>원청은 증액받은 날로부터 30일 이내에 반드시 그 비율만큼 하수급인의 대금도 증액</strong>해 주어야 합니다.</p>
            <p class="text-sm text-gray-600 mb-8 bg-gray-50 p-2 rounded">"발주처가 돈을 올려줬는데 내 돈만 닦아먹는다"를 막기 위한 조항입니다. 15일 이내에 증액 사유와 내용을 하수급인에게 반드시 서면 통지해야 할 의무도 신설되었습니다.</p>

            <h3 class="text-xl font-bold text-teal-800 border-b-2 border-teal-200 pb-2 mb-4">4. 원청의 보복조치 금지 (제19조)</h3>
            <p class="text-gray-800 mb-4">하수급인이 원청의 불공정행위를 공정위나 하도급분쟁조정위원회에 <strong>신고했다는 이유로 위탁을 취소하거나 거래를 단절하는 등 불이익(보복)</strong>을 가하는 것은 엄격히 금지됩니다.</p>
            ''',
            7
        ),
        (
            '8. [표준도급계약서] 발주자와 원청(종합) 간의 계약서 분석', 
            '''<h2 class="text-2xl font-bold mb-4">민간건설공사 표준도급계약서 심층 해부</h2>
            <p class="text-lg text-gray-700 mb-6">국토교통부가 고시한 <strong>표준도급계약서</strong>는 발주자(건축주)와 수급인(건설사) 간의 공정성을 맞춘 최고의 양식입니다.</p>

            <table class="w-full text-left border-collapse border border-gray-300 shadow-sm mb-8">
                <thead>
                    <tr class="bg-indigo-50 leading-normal border-b border-indigo-200">
                        <th class="py-3 px-6 font-semibold border-r border-indigo-200 w-1/3 text-indigo-900">계약 조항 (체크포인트)</th>
                        <th class="py-3 px-6 font-semibold text-indigo-900">실무적 해석 및 유의사항 (건설사 입장)</th>
                    </tr>
                </thead>
                <tbody class="text-gray-700 text-sm">
                    <tr class="border-b border-gray-200 hover:bg-gray-100">
                        <td class="py-4 px-6 border-r font-bold bg-indigo-50">제4조 (계약문서의 효력)</td>
                        <td class="py-4 px-6">
                            계약문서는 "계약서 > 시방서 > 설계도면 > 산출내역서 > 물량산출서" 순으로 우선순위를 가집니다. 가끔 도고와 내역서 수량이 안 맞을 때 <strong>우선순위에 명시된 문서</strong>를 근거로 설계변경(금액 증액)을 요구할 수 있습니다.
                        </td>
                    </tr>
                    <tr class="border-b border-gray-200 hover:bg-gray-100">
                        <td class="py-4 px-6 border-r font-bold bg-indigo-50">제16조 (공사기간의 연장)</td>
                        <td class="py-4 px-6">
                            천재지변, 전염병, 발주자의 책임, 관급자재 조달 지연, 등 시공자의 통제 밖의 사유로 공정이 지연되면 <strong>지체상금 없이 공기를 연장</strong>할 수 있어야 합니다. (반드시 이 조항이 살아있는지 확인)
                        </td>
                    </tr>
                    <tr class="border-b border-gray-200 hover:bg-gray-100">
                        <td class="py-4 px-6 border-r font-bold bg-indigo-50">제22조 (물가변동 ESC 조정)</td>
                        <td class="py-4 px-6">
                            계약일로부터 90일 이상 경과하고 물가가 3% 이상 증감 시, 잔여 부분에 대해 계약금를 조정합니다. 건축주가 <strong>특약으로 단가 고정(ESC 배제 특약)</strong>을 걸어두는 경우가 많으므로 도장 찍기 전 반드시 삭제를 요청해야 합니다.
                        </td>
                    </tr>
                    <tr class="hover:bg-gray-100">
                        <td class="py-4 px-6 border-r font-bold bg-indigo-50">제25조 (기성부분금의 지급)</td>
                        <td class="py-4 px-6">
                            통상적으로 1개월 단위로 기성검사를 하고 청구일로부터 <strong>14일 이내</strong>에 지급받도록 규정해야 합니다. 자금 흐름이 막히면 현장이 서므로 기성결제 기일은 매우 중요합니다.
                        </td>
                    </tr>
                </tbody>
            </table>

            <div class="bg-gray-100 border border-gray-300 p-6 rounded-lg shadow-md mb-6">
                <h3 class="text-xl font-bold mb-3 border-b border-gray-400 pb-2 text-gray-900">💡 지체상금(Delay Damages) 방어 전략</h3>
                <p class="text-sm leading-relaxed mb-3 text-gray-800">준공 기한을 어기면 하루당 총금액의 보통 1/1,000을 배상하게 됩니다.</p>
                <ul class="list-decimal pl-5 space-y-2 text-sm text-gray-700">
                    <li>공사진행 중 비가오거나 민원이 생기면 반드시 <strong class="text-gray-900">'작업일보'</strong>에 사유를 명시하고 발주자 측(감리)의 서명을 받으세요.</li>
                    <li>지연 사유 발생 즉시 <strong class="text-gray-900">'공기 연장 요청 공문'</strong>을 띄우고 회신을 받아 근거를 남기세요.</li>
                    <li>준공검사를 통과하지 못하더라도 건축주가 임시사용승인 등을 받아 건물을 <strong class="text-gray-900">'사실상 점유, 사용'</strong>하기 시작한 날부터는 지체상금이 면제됩니다.</li>
                </ul>
            </div>''',
            8
        ),
        (
            '9. [표준하도급계약서] 원청과 전문건설사(하청) 간의 계약서', 
            '''<h2 class="text-2xl font-bold mb-4">건설업종 표준하도급계약서 심층 해부</h2>
            <p class="text-lg text-gray-700 mb-6">원청(종합)의 부당한 요구를 쳐내기 위해 공정위가 마련한 양식입니다. 전문건설 공무는 이 양식을 달달 외워야 합니다.</p>

            <div class="grid md:grid-cols-2 gap-6 mb-8">
                <!-- 원청 의무 -->
                <div class="bg-white p-5 rounded-lg border border-gray-200 shadow hover:shadow-md transition">
                    <h3 class="font-bold text-lg text-blue-900 border-b pb-2 mb-3 flex items-center gap-2">
                        <span>🛡️</span> 원청의 핵심 채무 3가지
                    </h3>
                    <ul class="text-sm text-gray-800 space-y-3">
                        <li>
                            <strong class="text-blue-700 text-base block">1. 선급금 지급 보증 (제8조)</strong>
                            하청이 선급금(착수금)을 받기 전, 혹시 선급금을 먹고 튈까봐 원청은 '선급금반환보증서'를 요구합니다. 이 때 원청은 공사를 완료하면 대금을 주겠다는 <strong>'하도급대금 지급보증서'를 동시에 맞교환</strong>해야 합니다. (법적 의무)
                        </li>
                        <li>
                            <strong class="text-blue-700 text-base block">2. 설계변경 및 물량증가 서면발급 (제16조)</strong>
                            물량이 추가되면 하청이 시공하기 전에 반드시 '추가 작업 지시서(서면)'를 발급해야 합니다. (하도급법 제3조 서면발급 의무와 연계)
                        </li>
                        <li>
                            <strong class="text-blue-700 text-base block">3. 검사 및 인수 (제28조)</strong>
                            공사가 끝나 하청이 준공통지를 하면 <strong>10일 이내에 검사</strong>하고 목적물을 인수해야 합니다. 핑계를 대고 검사를 지연시켜서는 안 됩니다.
                        </li>
                    </ul>
                </div>

                <!-- 하청 방어 -->
                <div class="bg-white p-5 rounded-lg border border-gray-200 shadow hover:shadow-md transition">
                    <h3 class="font-bold text-lg text-red-900 border-b pb-2 mb-3 flex items-center gap-2">
                        <span>⚔️</span> 하청의 핵심 방어 권리 3가지
                    </h3>
                    <ul class="text-sm text-gray-800 space-y-3">
                        <li>
                            <strong class="text-red-700 text-base block">1. 핑계성 감액 금지 (제26조 2항)</strong>
                            원청이 "우리 회사가 여력이 안좋으니 이번 기성에서 너네 마진 좀 깎자", "어차피 일찍 끝났으니 인건비 까고 주마"라며 부당하게 감액해선 안 됩니다.
                        </li>
                        <li>
                            <strong class="text-red-700 text-base block">2. 산업재해 발생 시 은폐 및 전가 금지</strong>
                            특약에 "산재 처리는 모두 을이 알아서 한다(공상 처리 유도)"라고 적는 것은 전형적인 불법입니다. <strong>산안법에 따라 원청의 안전관리자 및 소장이 함께 책임지고 산재 보험을 처리</strong>해야 합니다.
                        </li>
                        <li>
                            <strong class="text-red-700 text-base block">3. 계약 해지의 요건 숙지 (제32조)</strong>
                            원청이 부당하게 대금지급보증서를 교부하지 않거나, 기성금 지급을 지연할 경우, <strong>하수급인(하청)이 먼저 당당하게 공사를 중지하거나 계약을 해지</strong>하고 손해배상을 청구할 수 있습니다.
                        </li>
                    </ul>
                </div>
            </div>

            <div class="p-4 bg-orange-100 border border-orange-300 rounded text-gray-800 text-sm">
                <strong class="text-orange-900 font-bold mb-1 block">📌 실무 팁: 전자서명의 중요성</strong>
                <p class="mb-2">요즘은 나이스다큐, 이크레더블 등의 전자계약 시스템을 많이 씁니다. 클릭 하나로 계약이 체결되므로, <strong>원도급사가 임의로 스리슬쩍 첨부한 "현장 특약조건" PDF 파일</strong>을 읽지도 않고 승인(서명)하는 순간 나중에 피를 봅니다. 도장 찍기 전에必ず 첨부문서를 모두 다운로드하여 독소조항을 검토하세요.</p>
            </div>''',
            9
        ),
        (
            '10. [안전] 산업안전보건법 및 중대재해처벌법 (CEO리스크)', 
            '''<h2 class="text-2xl font-bold mb-4">건설업 경영의 최대 리스크, 중대재해와 안전</h2>
            <p class="text-lg text-gray-700 mb-6">과거 현장 소장선에서 합의금으로 끝나던 시절은 끝났습니다. 이제는 <strong>본사 회장님을 구속시키는 치명적 법률</strong>인 중대재해처벌법(중처법)이 현장을 지배합니다.</p>
            
            <h3 class="text-xl font-bold text-red-800 border-b border-red-200 pb-2 mb-4">1. 중대재해처벌법(중처법) 요약</h3>
            <div class="bg-gradient-to-br from-red-50 to-white p-5 rounded-lg border border-red-100 shadow-sm mb-6">
                <p class="text-sm text-gray-800 mb-4">사업주나 <strong>경영책임자(CEO, 본사 대표이사)</strong>가 근로자, 종사자의 안전/보건 확보 의무를 다하지 않아 '중대산업재해'가 발생한 경우 경영책임관계를 형사처벌합니다.</p>
                
                <h4 class="font-bold text-gray-900 mb-2">중대산업재해의 3대 요건</h4>
                <ul class="list-disc pl-5 mb-4 text-sm text-red-700 font-semibold space-y-1">
                    <li>(1) 사망자 1명 이상</li>
                    <li>(2) 동일 사고로 6개월 이상 치료 요하는 부상 2명 이상</li>
                    <li>(3) 직업성 급성질병자 1년 이내 3명 이상</li>
                </ul>

                <h4 class="font-bold text-gray-900 mb-2">무서운 처벌 수위</h4>
                <p class="text-sm text-gray-800 mb-2">경영책임자 본인은 <strong>1년 이상의 징역 (하한선 명시로 매우 강력함)</strong> 또는 10억원 이하 벌금. (산안법은 '7년 이하'로 집행유예가 흔하지만, 중처법은 실형 선고율이 높습니다.) 법인에게는 최대 50억원의 벌금이 부과됩니다.</p>
                <p class="text-sm font-bold text-red-900">징벌적 손해배상: 중대재해 발생 시, 유족 등에게 손해액의 최대 5배까지 배상할 민사적 책임까지 발생합니다.</p>
            </div>

            <h3 class="text-xl font-bold text-teal-800 border-b border-teal-200 pb-2 mb-4">2. 산업안전보건법(산안법)과의 차이</h3>
            <div class="overflow-x-auto bg-white rounded-lg shadow-sm border border-gray-200 mb-8">
                <table class="w-full text-left text-sm">
                    <thead class="bg-gray-100 border-b border-gray-300">
                        <tr>
                            <th class="p-3 w-1/4 border-r font-semibold">비교 항목</th>
                            <th class="p-3 w-1/3 border-r font-semibold">산안법 (산업안전보건법)</th>
                            <th class="p-3 font-semibold text-red-800">중처법 (중대재해처벌법)</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr class="border-b">
                            <td class="p-3 font-bold bg-gray-50 border-r">핵심 주체</td>
                            <td class="p-3 border-r">안전보건관리책임자 (보통 현장소장)</td>
                            <td class="p-3 font-bold text-red-700">사업주, 경영책임자 (본사 CEO 등)</td>
                        </tr>
                        <tr class="border-b">
                            <td class="p-3 font-bold bg-gray-50 border-r">위반 내용 성격</td>
                            <td class="p-3 border-r">"안전난간대 미설치", "비계 불량" 등 물리적이고 구체적인 안전 수칙 위반</td>
                            <td class="p-3">본사 차원의 "안전 시스템(예산, 매뉴얼, 전담조직)" 미구축 등 구조적 결함</td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <h3 class="text-xl font-bold text-gray-800 border-l-4 border-emerald-500 pl-3 mb-4">3. 대표이사와 소장의 생존 전략: 4대 핵심 의무</h3>
            <p class="text-gray-700 text-sm mb-4">사고가 났을 때 구속을 면하려면 아래 4가지 시스템이 평소에 작동하고 있었음이 서류로 입증되어야 합니다.</p>
            <ol class="list-decimal pl-5 space-y-3 text-sm text-gray-800 bg-gray-50 p-5 rounded border border-gray-200">
                <li><strong class="text-emerald-800 text-base">안전보건관리체계 구축과 예산 편성:</strong> 단순한 페이퍼 조작이 아니라, 본사 전담조직(CSO)을 두고 <strong>과할 정도로 안전 전용 예산</strong>을 배정/집행한 대표이사의 결재 서류.</li>
                <li><strong class="text-emerald-800 text-base">위험성 평가(Risk Assessment)의 실질적 이행:</strong> 하청업체의 외국인 노동자까지 다 모아놓고 "오늘은 어디가 위험할까요?"를 스스로 찾게 하고 개선하는 회의록과 사진. (형식적 TBM 아님)</li>
                <li><strong class="text-emerald-800 text-base">적격 수급인의 선정:</strong> 제일 싼 견적서를 낸 하청업체를 그냥 쓰는게 아니라, 입찰 단계부터 업체의 <strong>'안전 관리 역량(재해율 등)'</strong>을 점수로 평가하여 업체를 선정했다는 객관적 지표.</li>
                <li><strong class="text-emerald-800 text-base">반기 1회 경영자 직접 점검:</strong> 반기 1회 이상(1년에 두 번) 본사의 CEO나 CSO가 현장에 직접 내려와서, 안전 체계가 말단 십장까지 작동하는지 검사하고 미조치 사항은 징계/보완한 보고서.</li>
            </ol>
            ''',
            10
        )
    ]

    for title, content, order in lessons:
         cursor.execute('''
            INSERT INTO lesson (title, content, "order", course_id)
            VALUES (?, ?, ?, ?)
        ''', (title, content, order, course_id))
        
    conn.commit()
    conn.close()
    print("[건산법 중심 6강~10강] 데이터베이스 테이블 시딩 완료")

if __name__ == '__main__':
    seed_law_course_ultimate_pt2()
