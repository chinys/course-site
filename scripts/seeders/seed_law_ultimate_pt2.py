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
            '6. [하도급법-1] 하도급거래 공정화 법률의 적용과 서면발급', 
            '''<h2 class="text-3xl font-extrabold mb-6 text-gray-900 border-b-2 border-slate-200 pb-3">하도급법의 규제 취지와 적용 대상</h2>
            <p class="text-lg text-gray-900 mb-8 leading-relaxed">하도급법(하도급거래 공정화에 관한 법률)은 거래상 우월적 지위 남용을 방지하고 원사업자와 수급사업자 간의 대등한 경제적 지위를 보장하여 공정한 하도급 거래 질서를 확립하고자 제정된 특별법입니다. <strong>공정거래위원회</strong>가 이를 관장하며 엄격한 제재 권한을 행사합니다.</p>
            
            <h3 class="text-xl font-bold text-gray-900 border-l-4 border-indigo-600 pl-3 mb-4">1. 하도급법 적용 요건 (당사자 정의)</h3>
            <div class="bg-gray-50 border border-gray-200 rounded-xl shadow-sm p-6 mb-8 flex flex-col md:flex-row gap-6">
                <div class="flex-1">
                    <h4 class="font-bold text-lg text-gray-900 border-b border-gray-200 pb-2 mb-3">적용 대상 사업자의 요건 (제2조)</h4>
                    <ul class="space-y-4 text-sm text-gray-900">
                        <li class="bg-white p-3 rounded shadow-sm border border-gray-200">
                            <span class="inline-block w-24 font-bold text-gray-900 text-base">원사업자:</span>
                            중소기업기본법상 대기업에 해당하거나, 도급 또는 하도급 위탁을 받는 당해 수급사업자보다 <strong>시공능력평가액(상당 매출액)이 명백히 상회(시행령상 2배 초과 등)</strong>하여 경제적 우위에 있는 중소기업(중견기업).
                        </li>
                        <li class="bg-white p-3 rounded shadow-sm border border-gray-200">
                            <span class="inline-block w-24 font-bold text-gray-900 text-base">수급사업자:</span>
                            원사업자로부터 건설, 제조, 역무 위탁을 받는 <strong>'해당 요건을 갖춘 중소기업자'</strong>. (법정 우위 사업자가 아닌 자에 한함.)
                        </li>
                    </ul>
                </div>
                <div class="flex-1 bg-gray-100 p-5 rounded-lg border border-gray-300">
                    <h4 class="font-bold text-gray-900 mb-2 flex items-center gap-2"><span>※</span> 위탁 행위의 법적 성질</h4>
                    <p class="text-sm text-gray-900 leading-relaxed mb-3">
                        <strong>"단순 물품 매매" vs "건설/제조 위탁"</strong><br>
                        표준 규격의 자재를 단순 구매하는 것은 하도급법상 위탁 계약이 아니나, 수급사업자에게 발주자의 도면 및 사양서에 부합하는 일정한 <strong>가공, 제작 또는 조립</strong>을 수반하는 역무(철골 구조물 제작/설치)를 의뢰하는 경우에는 하도급법의 '건설위탁 혹은 제조위탁'으로 편입되어 엄격한 보호 대상이 됩니다.
                    </p>
                </div>
            </div>

            <h3 class="text-xl font-bold text-gray-900 border-l-4 border-teal-600 pl-3 mb-4">2. 약정 서면 교부의 원칙 (제3조) - 사전 규제의 핵심</h3>
            <p class="text-gray-900 mb-3 text-sm leading-relaxed">계약 조건의 불명확성으로 인한 사후 분쟁을 예방하기 위해, 원사업자는 수급사업자가 <strong>당해 위탁 목적물에 대한 작업을 개시하기 이전</strong>에 법정 기재사항이 양 당사자에 의해 적법하게 서명 또는 기명날인된 '계약 서면'을 교부할 작위적 의무가 있습니다.</p>
            <div class="bg-gray-50 p-5 rounded-xl border border-gray-200 mb-8 shadow-sm">
                <p class="text-sm text-gray-900 font-semibold mb-3">구두 지시에 따른 구두 계약의 효력 부인 문제</p>
                <p class="text-sm text-gray-900 leading-relaxed">추가 공사 물량 발생 시 원사업자 측의 임의적 구두 지시는 사후 대금청구권의 존부를 다투는 증명책임 문제로 직결됩니다. 이는 하도급법 제3조 위반이 되어 원사업자의 불공정 이익 도모 행위로 처분될 수 있습니다.<br>
                <strong class="text-gray-900 block mt-2">💡 계약 실무 대응:</strong> 본 계약 외 경미한 설계 변경이나 투입 지연 지시가 있는 경우에도 반드시 <strong>전자메일, 공문서(작업일보), 서면 회의록</strong> 등의 객관적인 서면 자료를 원사업자 측으로부터 징구하거나 도달시켜야 추후 정당한 대금 청구 권한을 보전받을 수 있습니다.</p>
            </div>

            <h3 class="text-xl font-bold text-gray-900 border-l-4 border-gray-600 pl-3 mb-4">3. 부당한 특약의 효력 제한 (제3조의4)</h3>
            <p class="text-gray-900 mb-4 text-sm leading-relaxed">원사업자가 계약 체결 시 수급사업자의 정당한 권리를 부당하게 박탈하거나 이익을 제약하는 특수 조건을 부가하는 행위는 강행법규 위반으로 취급되어 <strong>해당 조항(특약)의 효력이 원천적으로 부정(무효)</strong>됩니다.</p>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-5 mb-6">
                <div class="bg-gray-50 border border-gray-200 p-5 rounded-lg shadow-sm font-sm">
                    <h4 class="font-bold text-gray-900 mb-3 border-b border-gray-300 pb-2">🚫 무효화 판례에 속하는 부당 특약 예시</h4>
                    <ul class="list-none pl-1 space-y-3 text-gray-900 text-sm">
                        <li class="flex gap-2"><span>▪️</span>"원 도급계약 및 본 공사 과정에서 발생하는 일체의 민원 배상과 행정 벌과금을 수급사업자의 전적인 책임으로 부담한다."</li>
                        <li class="flex gap-2"><span>▪️</span>"중대재해 등 산업재해 발생 시 귀책 사유를 불문하고 하수급인이 민/형사, 산재 및 유족 합의 비용을 전액 부담 및 공제에 동의한다."</li>
                        <li class="flex gap-2"><span>▪️</span>"설계 변경 등 조건 변동 시 전체 도급 물량의 10% 범위 내 초과분에 대하여는 별도의 증액(대가 지급)을 청구하지 아니한다."</li>
                        <li class="flex gap-2"><span>▪️</span>"천재지변, 발주자의 사정에 기인한 불가항력 상황에도 공기 연장 불허 및 지체상금 전액을 하수급인이 전부 부담한다."</li>
                    </ul>
                </div>
                
                <div class="bg-gray-100 border border-gray-300 p-5 rounded-lg shadow-sm font-sm">
                    <h4 class="font-bold text-gray-900 mb-3 border-b border-gray-300 pb-2 flex items-center gap-2"><span>⚖️</span> 수급사업자의 법률적 구제 절차</h4>
                    <p class="text-sm text-gray-900 leading-relaxed mb-3">수급사업자가 수주 과정에서 부당 특약이 명시된 합의서에 물리적인 동의(서명)를 하였다 하더라도, 권리 구제가 불가능한 것은 아닙니다.</p>
                    <p class="text-sm text-gray-900 leading-relaxed">해당 특약은 공정위 예규상 효력을 발휘하지 못하는 원시적 무효에 다름없으므로, 부당 감액이나 책임 전가 상황 발생 시 <strong>"하도급법상 제3조의4에 근거"한 법률 행위 부존재 내용증명</strong>을 발송하고, 하도급 분쟁조정협의회나 공정위에 불공정 행위를 신고함으로써 법원의 강제 조정을 통해 침해된 잔여 대금분과 법정 지연이자를 보상받을 수 있습니다.</p>
                </div>
            </div>''',
            6
        ),
        (
            '7. [하도급법-2] 하도급대금의 결정 및 지급 통제', 
            '''<h2 class="text-3xl font-extrabold mb-6 text-gray-900 border-b-2 border-slate-200 pb-3">정당한 하도급대금 보호 및 결제 지연 방지책</h2>
            <p class="text-lg text-gray-900 mb-8 leading-relaxed">계약 존속과 이행의 궁극적 효력인 <strong>적정 단가의 결정을 제재 없이 보장</strong>하고, 고의적 기성 대금 연체로 불필요한 공정 위험을 초래하는 관행을 규제하여 신의성실의 원칙을 공고히 합니다.</p>

            <div class="space-y-6">
                <!-- 1. 부당 대금 결정 -->
                <div class="bg-white border border-gray-200 p-6 rounded-xl shadow-sm transition">
                    <h3 class="text-xl font-bold text-gray-900 mb-3 flex items-center gap-2">
                        <span class="bg-gray-100 text-gray-900 p-1 rounded">1</span> 부당한 하도급대금의 결정 금지 (제4조)
                    </h3>
                    <p class="text-gray-900 mb-3 leading-relaxed text-sm">원사업자가 관련 산업계의 거래 관행상 통상적으로 기대되는 대가 이하로 부당하고 현저하게 감액하여 하도급 대금을 강압적으로 책정하는 행위는 엄격히 금지됩니다.</p>
                    <div class="bg-gray-50 p-4 border-l-4 border-gray-500 rounded text-sm text-gray-900">
                        <strong>경쟁입찰 부당 감액 제재의 판례:</strong> 다수 업체와의 공개 경쟁 입찰을 통해 수탁 업체를 선정한 후, 정당한 물량 변경 사유 없이 <strong>최저가 투찰 금액보다 임의로 재차 감액(추가 협상)을 요구하여 재계약을 강제하는 체결 행위</strong>는 공정거래법 위반으로서 중징계(과징금) 사유의 전형으로 판단합니다.
                    </div>
                </div>

                <!-- 2. 하도급 대금 60일 -->
                <div class="bg-white border border-gray-200 p-6 rounded-xl shadow-sm transition">
                    <h3 class="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
                        <span class="bg-gray-100 text-gray-900 p-1 rounded">2</span> 대금의 법정지급기한 및 수령 절차 (제13조)
                    </h3>
                    
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div class="bg-gray-50 border border-gray-200 rounded-lg p-4">
                            <h4 class="font-bold text-gray-900 mb-2 border-b border-gray-200 pb-1">기본 의무 (목적물 수령 후 60일)</h4>
                            <p class="text-sm text-gray-900 leading-relaxed">원사업자는 수급인으로부터 시공이 완료된 공사 목적물을 수령(준공/기성 청구)한 날부터 <strong>최장 60일 이내로 당사자 간 합의된 기일</strong> 내에 대금을 현금이나 이에 준하는 수단으로 지급하여야 합니다. (60일을 초과하는 지급 기일 특약은 법률상 강행규정 위배로 취급됩니다.)</p>
                        </div>
                        <div class="bg-gray-50 border border-gray-200 rounded-lg p-4">
                            <h4 class="font-bold text-gray-900 mb-2 border-b border-gray-200 pb-1">발주자 선(先) 수령 시 결제 지연 금지</h4>
                            <p class="text-sm text-gray-900 leading-relaxed">설령 목적물 인수 후 60일이 경과하기 이전이라도, 원사업자가 해당 부분에 대한 기성금을 발주처로부터 선지급받았다면 <strong>대금을 입금받은 날부터 기산하여 최장 15일 이내</strong>에 수급사업자에게 당해 비율을 귀속분으로서 신속히 지급하여야 합니다.</p>
                        </div>
                        <div class="bg-gray-50 border border-gray-200 rounded-lg p-4">
                            <h4 class="font-bold text-gray-900 mb-2 border-b border-gray-200 pb-1">지연 이자 및 어음할인료의 부과 의무</h4>
                            <p class="text-sm text-gray-900 leading-relaxed">전술한 법정 지급 기한(60일 또는 15일 우선 시효)을 도과하여 대금이 체불될 경우, 법정 요율인 <strong>고율의 지연이자(연 15.5%)</strong>가 자동 가산 발생하며, 수령 만기일이 60일을 초과하는 유가어음의 경우에는 공정위 규정에 따른 어음할인료(연 7.5%)를 지불할 의무가 부수됩니다.</p>
                        </div>
                    </div>
                </div>

                <!-- 3. 설계변경 대금 조정 -->
                <div class="bg-white border border-gray-200 p-6 rounded-xl shadow-sm transition">
                    <h3 class="text-xl font-bold text-gray-900 mb-3 flex items-center gap-2">
                        <span class="bg-gray-100 text-gray-900 p-1 rounded">3</span> 원 도급금액 증액 시 하도급대금 조정 의무 (제16조)
                    </h3>
                    <p class="text-gray-900 mb-3 text-sm leading-relaxed">계약 이행 중 발주자의 요구 등으로 인한 설계의 변경이나 경제적 사정 변동(물가 ESC)으로 원수급인이 도급 계약 금액을 발주처로부터 증액 조정을 받았다면, <strong>해당 증액 사유 통보 등을 받은 날부터 30일 이내에, 발주자로부터 상향된 요율 및 내용에 상응하여 하수급인의 하도급대금 또한 반드시 비례 증액</strong> 조정해 주어야 합니다.</p>
                    <p class="text-sm text-gray-900 bg-gray-50 border border-gray-200 p-3 rounded-lg">💬 수급사업자 배제에 의한 발주처 이익의 원사업자 독점 점유 관행을 통제하고 권익 균형을 유지하기 위함이며, 증액을 통보받은 당일부터 15일 이내에 원사업자의 증액 사실 여부를 수급사업자에게 명확히 서면으로 도달 고지할 의무가 부여되어 있습니다.</p>
                </div>
                
                <!-- 4. 보복 금지 -->
                <div class="bg-white border border-gray-300 p-6 rounded-xl shadow-sm border-l-8 border-l-gray-600">
                    <h3 class="text-xl font-bold text-gray-900 mb-2">🚨 4. 공정거래법상 보복 등 불이익 취급 금지 규정 (제19조)</h3>
                    <p class="text-gray-900 text-sm leading-relaxed">원수급인(원사업자)은 수급사업자가 부당 특약, 단가 감액 불공정 행위 등에 대해 공정거래위원회나 하도급분쟁조정기구에 <strong>적법한 신고나 조정을 요청 및 증거 제출을 이행했다는 이유만으로 해당 수급사업자와의 잔존 거래 승계 또는 향후 입찰 참여자격을 일방적으로 배제/제한하는 등 적개심에서 비롯된 보복성 조치</strong>를 가할 수 없으며, 적발 시 최대 수준의 법인 제재 및 형벌을 부담하게 됩니다.</p>
                </div>
            </div>''',
            7
        ),
        (
            '8. [도급계약서 양식] 민간건설공사 표준도급계약서 조항 분석', 
            '''<h2 class="text-3xl font-extrabold mb-6 text-gray-900 border-b-2 border-slate-200 pb-3">공사도급계약 일반조건 및 표준계약 구속력 심층 평가</h2>
            <p class="text-lg text-gray-900 mb-6 leading-relaxed">안정적인 시공 절차 완수와 상호 간 민사적 위험 배분을 위해, 국토교통부령이 권고하는 <strong>표준계약서 양식과 첨부 일반조건</strong>의 조문 배열을 충분히 숙지하여 불공정 독소조항 삽입을 차단하여야 합니다.</p>

            <div class="overflow-x-auto shadow-sm rounded-xl border border-gray-300 mb-8">
                <table class="w-full text-left bg-white border-collapse">
                    <thead>
                        <tr class="bg-gray-100 font-bold font-bold text-gray-900">
                            <th class="py-4 px-6 w-1/3 border-r border-gray-300">표준 계약 핵심 조항 명칭</th>
                            <th class="py-4 px-6">법적 쟁점 및 실무 담당 관점의 해석 방안</th>
                        </tr>
                    </thead>
                    <tbody class="text-gray-900 text-sm divide-y divide-gray-200">
                        <tr class="hover:bg-gray-50 transition text-gray-900">
                            <td class="py-5 px-6 border-r font-bold bg-white text-gray-900">제4조 (계약문서의 효력 상호 우선순위)</td>
                            <td class="py-5 px-6 leading-relaxed">
                                <span class="bg-gray-200 text-gray-900 px-2 rounded font-semibold text-xs mb-2 inline-block">해석 충돌 조정 기준</span><br>
                                방대한 서식 물량상 도면, 내역서 간 기재사항 불일치가 흔히 발생합니다. 대법원과 약관 해석 원칙상 <strong>"도급계약서 본문 > 공사(특기)시방서 > 설계도면 > 산출내역서"</strong>의 상위 효력 순위를 인정하므로, 실무적으로 누락된 공종에 대한 추가 공사 대금(물량 정산액 증액조치) 산정 시 명문상의 우선순위 규정을 강력히 원용하여 청구 근거를 유지해야 합니다.
                            </td>
                        </tr>
                        <tr class="hover:bg-gray-50 transition text-gray-900">
                            <td class="py-5 px-6 border-r font-bold bg-white text-gray-900">제16조 (공사기간의 연장과 불가항력)</td>
                            <td class="py-5 px-6 leading-relaxed">
                                <span class="bg-gray-200 text-gray-900 px-2 rounded font-semibold text-xs mb-2 inline-block">계약상 위험 수용 불가 원칙</span><br>
                                이례적인 감염병 사태 등 객관적 소요(천재지변 등 불가항력, 발주자 귀책 설계지연, 관급자재 납품 중단) 등의 <strong>수급인 통제 범위 외의 지연 조도 발생 시, 해당 소요일수만큼의 공기를 지체상금 조각(면제) 요건으로 연장 승인</strong>하는 합의 규정의 온전한 보전 여부를 반드시 심사해야 합니다.
                            </td>
                        </tr>
                        <tr class="hover:bg-gray-50 transition text-gray-900">
                            <td class="py-5 px-6 border-r font-bold bg-white text-gray-900">제22조 (물가변동 ESC 조정 - 에스컬레이션)</td>
                            <td class="py-5 px-6 leading-relaxed">
                                <span class="bg-gray-200 text-gray-900 px-2 rounded font-semibold text-xs mb-2 inline-block">공사비 원가 보상 실현</span><br>
                                원자재 급등에 대한 상업적 리스크 완화를 위해, 계약일 기산 90일 경과 시점에 원단위 품목이 잔여 전체 공사비용의 3% 증감 시 조정 비율을 적용한 <strong>대금 계약 변동권</strong>을 확보하여야 합니다. 발주자 우위 지위에서 흔히 제시하는 'ESC 불인정 영구단가 확정 특약'의 맹점을 사전에 식별하여 제외 권고하여야 합니다.
                            </td>
                        </tr>
                        <tr class="hover:bg-gray-50 transition text-gray-900">
                            <td class="py-5 px-6 border-r font-bold bg-white text-gray-900">제25조·제26조 (기성부분금, 준공검사 및 지급)</td>
                            <td class="py-5 px-6 leading-relaxed">
                                <span class="bg-gray-200 text-gray-900 px-2 rounded font-semibold text-xs mb-2 inline-block">현금 유동성 관리 규정</span><br>
                                기성검사 통과 통지가 도달한 이후 <strong>약정된 최단 기간(통상 기성 청구 통지로부터 14일)</strong> 이내에 해당 지불 금리를 포괄하여 신용도 높은 현금으로 수령 받을 재무적 여건을 계약서면에 합의 기재하여야 대금 담보 여부의 법적 안전성을 유지합니다.
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <div class="bg-gray-50 border border-gray-300 p-6 rounded-xl shadow-md mb-6">
                <h3 class="text-xl font-bold mb-3 border-b border-gray-300 pb-2 text-gray-900 flex items-center gap-2">
                    <span class="text-2xl">💡</span> 지체상금(Delay Damages) 부과 리스크 방어의 법률적 입증 팁
                </h3>
                <p class="text-sm font-semibold text-gray-900 mb-4 bg-white p-2 rounded">
                    준공 조달 의무 미이행에 대하여 총공사금액의 1,000분의 1의 승수를 부과하는 징벌적 배상 성격의 지연배상금 방어 대책 요약본입니다.
                </p>
                <div class="space-y-3">
                    <div class="flex gap-3 items-start bg-white p-3 rounded-lg border border-gray-200 shadow-sm">
                        <div class="bg-gray-100 text-gray-900 font-bold w-6 h-6 flex items-center justify-center rounded-full flex-shrink-0 text-xs mt-0.5">1</div>
                        <p class="text-sm text-gray-900">타 사업 소요나 극심한 기상 특보에 따른 당해 일체의 공정 마비 현상을 감리/발주처와 구두로 양해하는 데 그치지 않고, 반드시 <strong>발생 시점의 실질적인 상황을 작업일보, 현장 이력 보고서에 상술하여 감독인(감리단장)의 서면 서명 또는 승인 흔적</strong>의 문서 기록을 축적하여야 입증력이 제고됩니다.</p>
                    </div>
                    <div class="flex gap-3 items-start bg-white p-3 rounded-lg border border-gray-200 shadow-sm">
                        <div class="bg-gray-100 text-gray-900 font-bold w-6 h-6 flex items-center justify-center rounded-full flex-shrink-0 text-xs mt-0.5">2</div>
                        <p class="text-sm text-gray-900">통제 외 사유로 인한 지연일수 합의는 준공 일자가 형해화 되기 이전, 사전 요건 발생 즉시 <strong>'공사 기간의 조정 연장신청 및 증빙 첨부 공문' 형태로 발송하고 이에 대한 형식적 승낙 문서(회신공문)</strong>를 반드시 징구하여 증거 능력을 체계적으로 갖추어야 합니다.</p>
                    </div>
                    <div class="flex gap-3 items-start bg-white p-3 rounded-lg border border-gray-200 shadow-sm">
                        <div class="bg-gray-100 text-gray-900 font-bold w-6 h-6 flex items-center justify-center rounded-full flex-shrink-0 text-xs mt-0.5">3</div>
                        <p class="text-sm text-gray-900 font-semibold">대법원 주요 판례상 건축주 측의 하찮고 경미한 하자를 빌미로 한 준공 검사 승인 지연일지라도, 만약 해당 건축물이 임시사용승인 등 일부 인가를 통해 발주자 측에 <strong>'물리적, 사실상 점유 및 사용수익 통제 권한 내'에 편입되었다고 인정되는 시점부터 하수급인 측에 부과되는 기간 지연 배상(지체상금)의 귀책 누적은 전면 중단되어 손해배상 산정대상에서 배제</strong>됩니다.</p>
                    </div>
                </div>
            </div>''',
            8
        ),
        (
            '9. [하도급계약서 양식] 건설공사 하도급 표준 계약 양식 요건 및 협상', 
            '''<h2 class="text-3xl font-extrabold mb-6 text-gray-900 border-b-2 border-slate-200 pb-3">공정위 제정 건설 하도급 표준계약서 법적 실무 편람</h2>
            <p class="text-lg text-gray-900 mb-8 leading-relaxed">하수급인 보호에 관한 법익을 실체적으로 구현하기 위해 공정거래위원회가 작성 배포한 권장 서식 규격을 이해하고 부당한 강압 조건을 선제 억제할 수 있는 권리를 숙달하여야 상호 간의 법적 구속력을 적법하게 담지할 수 있습니다.</p>

            <div class="grid lg:grid-cols-2 gap-8 mb-8">
                <!-- 원청 의무 패널 -->
                <div class="bg-white rounded-2xl border border-gray-300 shadow-lg overflow-hidden">
                    <div class="bg-gray-100 px-6 py-4 flex items-center gap-3">
                        <span class="text-2xl">📋</span>
                        <h3 class="font-bold text-lg text-gray-900 m-0">수급인(원사업자) 대상 주요 강제 의무</h3>
                    </div>
                    <div class="p-6 text-sm text-gray-900 space-y-5">
                        <div class="relative pl-4 border-l-2 border-gray-400 hover:border-gray-600 transition">
                            <strong class="text-gray-900 text-base font-bold flex items-center gap-2 mb-1"><span class="bg-gray-200 text-gray-900 text-xs px-2 py-0.5 rounded-full">의무 1</span> 이행 담보 보증 수단의 법정 교환 (제8조)</strong>
                            <p class="leading-relaxed">하수급인이 원사업자에게 착수금 보전을 위한 계약이행 보증을 위한 지급채무 보험 증권을 전달함과 동시에, 원사업자 역시 하수급인에게 부도 등 이행위험 상계 목적으로 <strong>'하도급대금 등 지급 담보 보증서(전문공제조합 발행 등)'를 강제적으로 교부·제공</strong>하여야 쌍무 계약의 완전 성립 의사를 갈음합니다.</p>
                        </div>
                        <div class="relative pl-4 border-l-2 border-gray-400 hover:border-gray-600 transition">
                            <strong class="text-gray-900 text-base font-bold flex items-center gap-2 mb-1"><span class="bg-gray-200 text-gray-900 text-xs px-2 py-0.5 rounded-full">의무 2</span> 설계변경 시 서면 즉시 발급절차의 준수 (제16조)</strong>
                            <p class="leading-relaxed">구체적인 도면 변경 사항의 교부 전후 즉각 시공을 지시함과 별론으로, 단가 감액 시비를 예방하고자 <strong>수량 등 물량 변동, 변경 공사 금액, 착수 일자 등이 적시된 합의 서면 또는 지시서</strong>를 당해 공정에 대한 물적 인입 전에 교부하여 추가 대금 확정성 요건을 확보해야 할 의무를 집니다.</p>
                        </div>
                        <div class="relative pl-4 border-l-2 border-gray-400 hover:border-gray-600 transition">
                            <strong class="text-gray-900 text-base font-bold flex items-center gap-2 mb-1"><span class="bg-gray-200 text-gray-900 text-xs px-2 py-0.5 rounded-full">의무 3</span> 준공 목적물의 기한부 검사 인계 (제28조)</strong>
                            <p class="leading-relaxed">하도급 위탁 공정이 완료되어 서면 인계(기성, 준공청구 등)를 알리면 원사업자는 지체 없이 당해 인수 사항을 통보받은 일로부터 <strong>10일 이내에 즉각 현장 실사 및 확정 평가를 마무리</strong>하고 무조건 인수 절차를 갈음해야 부당 지연을 회피할 수 있습니다.</p>
                        </div>
                    </div>
                </div>

                <!-- 하청 방어 패널 -->
                <div class="bg-white rounded-2xl border border-gray-300 shadow-lg overflow-hidden">
                    <div class="bg-gray-100 px-6 py-4 flex items-center gap-3">
                        <span class="text-2xl">⚖️</span>
                        <h3 class="font-bold text-lg text-gray-900 m-0">하수급인 방어 및 적법 항변권 요건 </h3>
                    </div>
                    <div class="p-6 text-sm text-gray-900 space-y-5">
                        <div class="relative pl-4 border-l-2 border-gray-400 hover:border-gray-600 transition">
                            <strong class="text-gray-900 text-base font-bold flex items-center gap-2 mb-1"><span class="bg-gray-200 text-gray-900 text-xs px-2 py-0.5 rounded-full">방어 1</span> 임의 감액 및 부당 공제 청구 불응권 (제26조 2항)</strong>
                            <p class="leading-relaxed">장비 청구, 공사 외 제반비용 등을 빙자하여 준공 결산 시기에 수급단가를 일방적으로 전용 감액할 것을 압박 요구하는 경우, 이에 동의치 아니하는 명시적 의사표시와 함께 제소함으로써 감액분을 온전 보전받게 됩니다.</p>
                        </div>
                        <div class="relative pl-4 border-l-2 border-gray-400 hover:border-gray-600 transition">
                            <strong class="text-gray-900 text-base font-bold flex items-center gap-2 mb-1"><span class="bg-gray-200 text-gray-900 text-xs px-2 py-0.5 rounded-full">방어 2</span> 구조적 산업재해 책임의 일방귀속 차단</strong>
                            <p class="leading-relaxed"><em>"중대재해 등 안전 규정 위반 사건 도래 시 당해 민/형사상 소요, 산재보험 처리 일체를 하수급인이 감수한다"</em>의 특약은 명백한 불공정 행위입니다. 산업안전보건법 및 관계법령은 위험요소를 <strong>지배/관리/소유하는 원사업자와 사업주 등이 모두 전사적 규모의 안전 보증 관리망을 통해 공동 주체적 의무</strong>로 이행할 것을 입법 의도로 삼고 있기에 이러한 면책 전가 조항은 법적으로 수긍되지 아니합니다.</p>
                        </div>
                        <div class="relative pl-4 border-l-2 border-gray-400 hover:border-gray-600 transition">
                            <strong class="text-gray-900 text-base font-bold flex items-center gap-2 mb-1"><span class="bg-gray-200 text-gray-900 text-xs px-2 py-0.5 rounded-full">방어 3</span> 도급 불이행에 대한 해지 및 항변권 보장 (제32조)</strong>
                            <p class="leading-relaxed">계약 당시 대금지급보증 미루기나 이례적인 계속적 대금 지체 사실 등이 인지될 경우, 하수급사업자는 자신의 이무를 제공할 위험이 현저하다는 신뢰 상실에 근거하여 <strong>인력·장비 등 역무제공 공급 지체 중단을 통고하거나 더 나아가 단독 확정 해지 선언과 구상권 행사</strong>를 법적으로 지지받을 항변 채권의 존재를 확보케 됩니다.</p>
                        </div>
                    </div>
                </div>
            </div>

            <div class="p-5 bg-gray-50 border-2 border-gray-300 rounded-xl relative overflow-hidden shadow-sm">
                <div class="relative z-10">
                    <strong class="text-gray-900 font-extrabold text-lg mb-2 flex items-center gap-2"><span>📌</span> 계약 성립의 증명책임: 전자계약과 시스템 약관의 위험 관리</strong>
                    <p class="text-sm text-gray-900 leading-relaxed mb-3">거래 관습상 '전자 계약 문서 유통망 시스템' 등을 통하여 인증서 기반의 일괄 비대면 서명이 일상화되었습니다.</p>
                    <p class="text-sm font-semibold text-gray-900 bg-white p-3 rounded shadow-inner">이 과정에서 <strong>특수 조건안, 원사업자만의 일방적 특약 사항을 담은 임의 부수 파일(PDF)</strong> 등이 첨부 파일의 외관으로 합의 문건에 병합되어 결재될 우려가 존재합니다. 공인인증서를 통한 법적 승인(서명 완료) 행위는 계약의 세밀한 내용을 당사자가 숙지하였음을 간주케 하는 무거운 자기 책임의 법리를 갖는 바, <span class="underline">결재에 합의 서명 조치를 이행하기 직전 도급자는 반드시 병합된 일련의 문서 파일과 특기 조항 전문 다운로드 및 권리 박탈 성격의 독소 조항 포함 여부를 법무적 기준에서 꼼꼼히 분리 검수</span>하여야 항변 제한 사태를 회피할 수 있습니다.</p>
                </div>
            </div>''',
            9
        ),
        (
            '10. [안전 법령] 산업안전보건법 및 중대재해처벌법 (경영책임자 책임)', 
            '''<h2 class="text-3xl font-extrabold mb-6 text-gray-900 border-b-2 border-slate-200 pb-3">건설 전 영역에서 지배되는 최상위 안전 보건 확보 규제</h2>
            <p class="text-lg text-gray-900 mb-8 leading-relaxed">근로자 재해의 귀책을 현장 단위 인력의 1차원적 과실이나 사고 배상금 충당으로 종결 짓던 종래의 해석 범위는 일체 상실되었습니다. 현행 <strong>중대재해처벌 등에 관한 법률(이하 중대재해처벌법)</strong>은 근원적 안전을 경영 체계로 관리할 포괄 수여자인 <strong>기업의 경영책임자의 구체별 의무</strong>에 대해 직접적 처벌 규정을 부임함으로써 실 체적 중대 과실을 봉쇄하고 있습니다.</p>
            
            <h3 class="text-xl font-bold text-gray-900 border-l-4 border-gray-600 pl-3 mb-4">1. 중대재해처벌법(SAPA) 핵심 목적과 처벌 인용 요건</h3>
            <div class="bg-gray-50 p-6 rounded-xl border border-gray-200 shadow-md mb-8">
                <p class="text-sm text-gray-900 mb-5 leading-relaxed bg-white border border-gray-200 p-4 rounded-lg shadow-sm">법인은 고용한 소속 근로자만이 아닌 사업 수행의 모든 편제에 속한 용역, 도급, 타 수급사업자의 일용직 작업자에 이르기까지 <strong>현장 환경 내 전 인원의 안전과 건강 제도를 통제 및 개선할 "종합적이고 구조적 안전보건관리체계"의 기획 설계와 실행 관리 책임을 경영 최상위 집행권자(대표이사/CEO 등 경영책임자)</strong>에게 전적으로 부여합니다. 이를 궐한 사유에서 사상 등의 재해가 돌발한 경우, 의무를 소홀히 한 본사 경영책임자에 대한 형벌 소추가 즉각 이행되는 강력 규범입니다.</p>
                
                <div class="grid md:grid-cols-2 gap-6">
                    <div>
                        <h4 class="font-bold text-gray-900 mb-3 bg-gray-200 inline-block px-3 py-1 rounded">※ 중대산업재해의 성립 요건 3요소</h4>
                        <ul class="list-none pl-1 mb-4 text-sm text-gray-900 space-y-3">
                            <li class="flex items-start gap-2"><span class="bg-gray-200 text-gray-900 w-5 h-5 flex items-center justify-center rounded-full flex-shrink-0 text-xs mt-0.5">1</span> <strong>사망사고 사망자 1명 이상</strong> 도래 (현장에서 가장 빈번히 집무됨)</li>
                            <li class="flex items-start gap-2"><span class="bg-gray-200 text-gray-900 w-5 h-5 flex items-center justify-center rounded-full flex-shrink-0 text-xs mt-0.5">2</span> 동일 성격의 원인된 사고로 <strong>통상 치료가 6개월 이상 소요 예정인 상해자 2명 이상</strong> 초과</li>
                            <li class="flex items-start gap-2"><span class="bg-gray-200 text-gray-900 w-5 h-5 flex items-center justify-center rounded-full flex-shrink-0 text-xs mt-0.5">3</span> 급성중독 요소 등 법정 지정 유해인자에 복합 직업성 발병된 <strong>질병자 3명 이상 여부의 1년 주기 누적</strong></li>
                        </ul>
                    </div>
                    
                    <div class="border-l border-gray-200 pl-4">
                        <h4 class="font-bold text-gray-900 mb-3 bg-gray-200 inline-block px-3 py-1 rounded">⚖️ 제재 수준 (위법성 판단에 따른 양형)</h4>
                        <div class="space-y-4 text-sm">
                            <div class="flex flex-col">
                                <span class="font-bold text-gray-900">👤 개인 처벌 수준 (경영책임자 위주):</span>
                                <span class="text-gray-900 bg-gray-100 p-2 rounded block mt-1">사망 발생 책결 시 대다수 규정이 규정한 "이하" 한도가 아닌, 하한선이 고정된 <strong>"1년 이상의 유기징역형 선고의 원칙"</strong> 또는 10억원 이하 규모의 벌칙금 형벌에 병과됩니다.</span>
                            </div>
                            <div class="flex flex-col">
                                <span class="font-bold text-gray-900">🏢 양벌 규범 (법인 자산 대상 부과금):</span>
                                <span class="text-gray-900 bg-gray-100 p-2 rounded block mt-1">의무 위반으로 사망 사고 원인 기여 시 당해 법인 사업자 명의에 대하여는 <strong>최대 50억 원 이하 배수의 벌금형</strong>이 구가 청구됩니다.</span>
                            </div>
                            <div class="flex flex-col">
                                <span class="font-bold border border-gray-400 bg-gray-200 text-gray-900 px-2 py-1 inline-block rounded max-w-max text-xs">💸 징벌적 차원의 손해 및 합의금 보상</span>
                                <span class="text-gray-900 mt-1">상당한 악의 의도로 인정되거나 의무 소홀 과실 시, 타방 민사 재판 절차에서 손해 성립 추정액의 <strong>최대 5배 최고에 이를 수준에 해당하는 손해배상책임 한도</strong>를 판결 부과토록 규정하여 법인 재무 위험을 대폭 확대 조장합니다.</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <h3 class="text-xl font-bold text-gray-900 border-l-4 border-gray-600 pl-3 mb-4 mt-8">2. 산업안전보건법과 중대재해처벌법 간 적용 양태 및 규제 쟁점 비교</h3>
            <p class="text-gray-900 text-sm mb-4 leading-relaxed">현장 감식 절차가 돌입할 시 감독 기관 및 관련 특사경 부서는 중대재해처벌법과 산업안전보건법 양법의 과실 유무 조사를 중첩적 동시 절차(Twin-Track)로 진입합니다.</p>
            <div class="overflow-x-auto bg-white rounded-xl shadow-md border border-gray-300 mb-10">
                <table class="w-full text-left text-sm border-collapse">
                    <thead>
                        <tr class="bg-gray-100 font-bold text-gray-900">
                            <th class="p-4 w-1/5 border-r border-gray-300 font-bold text-center">주요 식별 항목</th>
                            <th class="p-4 w-2/5 border-r border-gray-300 font-bold">산업안전보건법 적용 대상 및 쟁점</th>
                            <th class="p-4 w-2/5 font-bold">중대재해처벌법 적용 대상 및 쟁점</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-gray-200">
                        <tr class="hover:bg-gray-50 text-gray-900">
                            <td class="p-4 font-extrabold bg-gray-50 border-r text-center text-gray-900">의무당사자 및 수사 초점 타겟</td>
                            <td class="p-4 border-r text-gray-900 font-medium">실질적 노무 행위를 지시, 통제하는 해당 공간 단위의 <strong>안전보건관리책임자 (일선 현장대리인, 현장소장)</strong></td>
                            <td class="p-4 bg-gray-100 font-bold shadow-inner text-gray-900">전사적 예산 조직 집행 인가 의무를 책임지는 본사 단위의 <strong>경영책임자 또는 각자/최고대표 대표이사</strong></td>
                        </tr>
                        <tr class="hover:bg-gray-50 text-gray-900">
                            <td class="p-4 font-extrabold bg-gray-50 border-r text-center text-gray-900">규제 위반 내용의 시야(Nature)</td>
                            <td class="p-4 border-r text-gray-900 leading-relaxed">
                                <span class="bg-gray-200 rounded px-1 font-semibold text-xs mb-1 inline-block">현장 단위 물리적/미시적 안전 수칙 준수 검증</span><br>
                                추락 시설, 개구부 난간 방호 설비, 안전고리 지급 강제 등 <strong>단편적·구체적 현장 설비 규정 미이행</strong> 여부에 대한 즉각적 형벌 단속 사유 여부가 점검 심오 사항입니다.
                            </td>
                            <td class="p-4 leading-relaxed bg-gray-100 font-medium text-gray-900">
                                <span class="bg-gray-300 text-gray-900 rounded px-1 font-bold text-xs mb-1 inline-block">기관 단위 구조적/거시적 경영 의무 증명</span><br>
                                단일 작업 위반 심문이 아닌 <strong>독립적 관장조직, 적정 최고예산 편성 집행, 이사회 및 통제 기구(평가 전담자) 등의 "조직적, 전사 방호 안전 경영 전담 메커니즘 구축 여부"</strong>를 서면 자료 등 객관적 실증 여부로 평가해 판단합니다.
                            </td>
                        </tr>
                        <tr class="hover:bg-gray-50 text-gray-900">
                            <td class="p-4 font-extrabold bg-gray-50 border-r text-center text-gray-900">처벌의 법정 요건 척도</td>
                            <td class="p-4 border-r text-gray-900 font-medium">최대 형량 기준 7년 이하의 징역(구조적 위반 인정 외 양형 하향 조절의 예 다수 등)</td>
                            <td class="p-4 font-bold bg-gray-100 text-gray-900">기본 최하 한도 1년 이상 징역 복역의 전격 요구 및 극단적 벌금 구상</td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <h3 class="text-2xl font-bold mb-5 flex items-center gap-2 text-gray-900 bg-gray-100 py-3 px-5 rounded-lg border-l-8 border-gray-600">
                경영 권인 확보를 위한 핵심 경영 4대 의무 이행 체계 증명 수단
            </h3>
            <p class="text-gray-900 text-base mb-6 leading-relaxed">경영책임자가 재해 발생 사실에도 형벌의 면책 조각 타당성을 인용 받기 위해서는, 단일 사고가 일선 하부직원의 극히 예외적 고의 등에 해당할 만큼 <strong>기관 차원에서는 안전에 관해 법이 의거한 체계적 예방 노력을 무결점으로 준수했음</strong>을 명시적이고 시계열 구조화된 일체의 공적인 결재 기록, 감찰 이력을 통해 실질 소명 입증해야 할 요건이 따릅니다.</p>
            
            <div class="space-y-4">
                <div class="flex items-start bg-white border border-gray-200 p-5 rounded-xl shadow-sm hover:shadow-md transition">
                    <div class="bg-gray-100 text-gray-900 font-bold text-xl w-12 h-12 flex items-center justify-center rounded-lg flex-shrink-0 shadow-sm mr-4 mt-1">1</div>
                    <div>
                        <h4 class="font-bold text-lg text-gray-900 mb-2">총괄 안전보건관리체계 전담 조직 명문화 및 법정 예외를 상회하는 실 집행 결재 내역 구비</h4>
                        <p class="text-sm text-gray-900 leading-relaxed">정규 조직도 상 대표 직속의 통제력을 소유한 권한 전담 부서 단위(CSO 본부격)를 구성 배치시키고, 전사적 기금 내 인건, 특장, 시설 장비를 보증할 별도의 <strong>안전 예산을 당해 전폭적으로 기안/편성/서명/지출 결재 수행</strong>하여 이에 따른 영수 증발 및 결재 흔적이 이력화 문서로 산입되어야 최우선적 입증 기초가 타결됩니다.</p>
                    </div>
                </div>
                
                <div class="flex items-start bg-white border border-gray-200 p-5 rounded-xl shadow-sm hover:shadow-md transition">
                    <div class="bg-gray-100 text-gray-900 font-bold text-xl w-12 h-12 flex items-center justify-center rounded-lg flex-shrink-0 shadow-sm mr-4 mt-1">2</div>
                    <div>
                        <h4 class="font-bold text-lg text-gray-900 mb-2">실체적 위험성 평가(Risk Assessment) 과정 내 작업 종사자 일체의 심층 참여 서류 축적</h4>
                        <p class="text-sm text-gray-900 leading-relaxed">현장 안전관리자가 도면만 대조하여 형식적 보고서를 날인한 바는 증빙 적법성에서 즉결 훼손됩니다. 일선 반장부터 단순 노무제공자인 소속, 특수형태 종사자 모두가 작업의 시작 단위에서 <strong>위험 포인트를 스스로 감식, 도출, 청취 제안하게 하는 상시적 의견 청취 창구를 유지</strong>한 채 조치 의견을 반영 및 이행한 결과 사진부와 시스템 피드백 데이터를 서류 편철에 포함하여야 적절 이행 증거로 채택됩니다.</p>
                    </div>
                </div>

                <div class="flex items-start bg-white border border-gray-200 p-5 rounded-xl shadow-sm hover:shadow-md transition">
                    <div class="bg-gray-100 text-gray-900 font-bold text-xl w-12 h-12 flex items-center justify-center rounded-lg flex-shrink-0 shadow-sm mr-4 mt-1">3</div>
                    <div>
                        <h4 class="font-bold text-lg text-gray-900 mb-2">위탁 대상 협력 사업자의 철저한 객관적 기준 평가 심사 선별 의무 이행</h4>
                        <p class="text-sm text-gray-900 leading-relaxed">도급 심의 단계 중 단순 최저 입찰 금액 지향에 함몰되는 관습을 타파하여야 합니다. 발주 부서는 협력 계약을 발효할 대상 수급사업자의 당해 역량인 <strong>법정 전담 요원 확보 현황, 과거의 산재 발병 공제 비율, 재해 이력 건수를 가시화한 객관적 정량 평가 심사 지표(Matrix) 시스템</strong> 상 결격 판정 업체엔 아예 자격을 박탈시킨 평가 통과 이력 명세 부첨 결재 사안을 구증하여야 실질 조사를 완벽 대비합니다.</p>
                    </div>
                </div>

                <div class="flex items-start bg-white border border-gray-200 p-5 rounded-xl shadow-sm hover:shadow-md transition">
                    <div class="bg-gray-100 text-gray-900 font-bold text-xl w-12 h-12 flex items-center justify-center rounded-lg flex-shrink-0 shadow-sm mr-4 mt-1">4</div>
                    <div>
                        <h4 class="font-bold text-lg text-gray-900 mb-2">최고경영진 등 정기 반기 단위 현장 이행 지도력 결과 징벌 문서 도출 여부</h4>
                        <p class="text-sm text-gray-900 leading-relaxed">본사 사무 구조 내 매뉴얼의 하달만으론 이행 통제 능력을 입증하기 불충분합니다. 최저 일 년에 두 차례, 반기별 필수 시점을 근거로 <strong>본사 관리의 경영진 또는 책임 직무 대표자</strong>가 직접적 통제 및 보고가 이뤄지는 현장에 진입 순회하고, 적시 감시 적발 미흡 결과물에 대해 즉결 징계, 계약 정지 경고 등 단호한 인사 및 물리 조치를 집행 처리된 시말 문서를 확충했을 시만이 <strong>'선량한 관리 감독의 경영진 과실 면제 방제 방벽'</strong> 능력을 확정 수립하게 만듭니다.</p>
                    </div>
                </div>
            </div>''',
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
    print("[건산법 중심 6강~10강 전문화 완료] 데이터베이스 테이블 시딩 완료")

if __name__ == '__main__':
    seed_law_course_ultimate_pt2()
