import sqlite3
import os
import sys

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def seed_law_course_ultimate_pt3():
    db_path = os.path.join(os.path.dirname(__file__), '..', '..', 'database.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    course_title = '건설법규'
    cursor.execute('SELECT id FROM course WHERE title = ?', (course_title,))
    row = cursor.fetchone()
    if not row:
        print("Course not found, run pt1 and pt2 first.")
        return
    course_id = row[0]

    lessons = [
        (
            '11. [실무 심화] 불법 하도급 및 위장 도급의 법적 판단 기준', 
            '''<h2 class="text-3xl font-extrabold mb-6 text-gray-900 border-b-2 border-slate-200 pb-3">건설업 면허 체계와 위장 도급의 사법적 제재</h2>
            <div class="bg-gray-100 text-gray-900 font-bold border border-gray-600 p-6 rounded-2xl shadow-xl mb-8">
                <p class="text-lg leading-relaxed mb-4">원수급인으로부터 하도급을 받은 전문건설업체가 자체적인 자재, 장비, 그리고 직접 고용한 근로자를 통해 통제하에 공사를 수행하는 것은 적법한 직영 시공입니다. <strong>다만, 명목상으로만 기성을 청구하고 현장의 실질적인 시공 통제권과 인력 관리를 형식적인 자격이 없는 제3자(이른바 무등록 시공참여자 또는 작업반장)에게 목적물의 특정 물량 단위로 일괄 위탁하는 경우, 이는 '동일업종 간 하도급 제한 규정' 및 '건산법상 명의 대여/무등록 시공/불법 파견' 위반으로 직결되어 엄중한 처벌 대상이 됩니다.</strong></p>
                <div class="bg-gray-100 text-gray-900 p-4 rounded-xl border-l-4 border-yellow-500 font-semibold pl-4 shadow-sm">
                    <span class="text-yellow-900 text-lg font-bold">🚨 감독 관청 및 수사 기관의 판단 원칙:</span><br>
                    수사 기관은 형식적으로 작성된 <strong>'일용근로계약서'라는 외관에 의존하지 않습니다.</strong> 대상 법인의 계좌 거래 내역, 법인카드 사용처, 현장 관리자들 간의 통신 기록 등을 종합적으로 분석하여 <strong>"누가 실질적인 지휘·감독 권한을 행사하였으며, 완성된 결과에 따른 대가가 어떠한 방식으로 정산되었는가 (실질적 종속성 및 사업 주체성)"</strong>를 집중적으로 추적하여 위법성을 판단합니다.
                </div>
            </div>
            
            <h3 class="text-2xl font-bold text-gray-900 border-l-4 border-slate-700 pl-3 mb-4">1. 도급 및 위장 근로의 실체적 분별 요건</h3>
            <p class="text-gray-900 text-base mb-4 leading-relaxed">계약의 명칭이 '위탁, 용역, 컨설팅' 등 어떠한 형태라 하더라도, 그 본질이 "일의 완성 결과에 대한 책임 전가와 독립적 이행"에 해당한다면 무등록 건설도급 행위로 처단됩니다.</p>
            <div class="bg-white border focus:outline-none focus:ring border-red-200 rounded-xl p-6 mb-10 shadow border-t-8 border-t-red-600">
                <h4 class="font-bold text-red-900 mb-3 flex items-center gap-2"><span class="text-xl">⚠️</span> 불법 위장 도급을 판별하는 4가지 핵심 징후</h4>
                <div class="space-y-4 text-sm text-gray-900">
                    <div class="flex gap-3 items-start">
                        <span class="font-black text-red-600 text-lg mt-0.5">1.</span>
                        <p class="leading-relaxed"><strong>조직적 지휘·감독 권한의 이탈:</strong> 서류상으로는 전문건설사업자의 직고용된 일용직 근로자로 등재되어 있으나, 실제 작업 현장에서는 당해 건설사의 현장대리인(소장)이 아닌 <strong>외부 무자격 작업 반장의 독단적 지시에 따르며, 원청의 근태 통제를 배제하거나 독립적인 체계로 인력을 운영할 때 (사용 종속 관계의 단절).</strong></p>
                    </div>
                    <div class="flex gap-3 items-start">
                        <span class="font-black text-red-600 text-lg mt-0.5">2.</span>
                        <p class="leading-relaxed"><strong>임금 산정 및 지급 방식의 위장:</strong> 겉으로는 일반적인 일급제(근로시간에 비례한 임금)로 서류를 꾸미지만, 실질적인 이면 정산은 <strong>투입된 자재량(톤)이나 면적(㎡) 단위의 결과물을 기준으로 한 '단가 도급' 방식</strong>으로 산출되며, 해당 대금이 작업 단위의 총괄자에게 일괄 지급될 때.</p>
                    </div>
                    <div class="flex gap-3 items-start">
                        <span class="font-black text-red-600 text-lg mt-0.5">3.</span>
                        <p class="leading-relaxed"><strong>장비 및 제반 비용의 포괄 부담:</strong> 장비 대여의 외관을 띠나, 실제로는 <strong>특정 구역의 장비, 유류대, 인부 식대, 안전 장구 등 공사 수행에 필요한 모든 요소적 비용을 대여업자 측이 독립적으로 부담하고 관리</strong>하며 이익을 남기는 완전한 턴키(Turn-key) 형태로 운영될 때.</p>
                    </div>
                    <div class="flex gap-3 items-start">
                        <span class="font-black text-red-600 text-lg mt-0.5">4.</span>
                        <p class="leading-relaxed"><strong>면허 대여 수수료의 우회 편취:</strong> 법인 면허를 대여한 대가로 브로커 등에게 <strong>'세무/공무 대행 자문료' 혹은 '현장 관리 수수료'</strong> 등 모호한 명목으로 공사금액의 일정 비율(도지)이 주기적으로 법인 계좌에서 이체될 때.</p>
                    </div>
                </div>
            </div>

            <h3 class="text-2xl font-bold text-gray-900 border-l-4 border-indigo-600 pl-3 mb-5">2. 적법한 '직영 시공'과 불법 '재하도급'의 명확한 판단 기준</h3>
            <p class="text-gray-900 mb-5 leading-relaxed text-sm">중간관리자(작업 반장)에게 특정 공정의 완성과 인력 소도를 포괄적으로 맡기어 이윤을 취하게 하는 방식은 현행법상 인정되지 않는 불법 구조입니다. 사법 당국의 조사를 대비할 명확한 법률적 방어선 구축이 필수적입니다.</p>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8 text-sm">
                <!-- 합법 (직영팀 패널) -->
                <div class="bg-blue-50 border border-blue-200 p-6 rounded-2xl shadow-md hover:shadow-lg transition duration-300">
                    <h4 class="font-bold text-blue-900 mb-3 text-lg border-b border-blue-200 pb-2 flex items-center justify-between">
                        <span class="flex items-center gap-2"><span class="text-xl">✅</span> 적법한 직영 시공 인정 요건</span>
                    </h4>
                    <p class="mb-3 text-blue-900 font-medium">건설사업자의 현장대리인이 각각의 현장 근로자와 <strong>1:1로 직접 근로계약을 체결하고, 제반 문서를 자사에 귀속하여 관리</strong>합니다.</p>
                    <ul class="list-none space-y-3 text-gray-900">
                        <li class="flex items-start gap-2">
                            <span class="text-blue-900 font-bold">✓</span>
                            <span>회사의 현장대리인이나 관리 직원이 각 근로자에게 구체적이고 <strong>직접적인 작업 명령 및 근무 지휘 감독</strong>을 행사하며 이를 문서화(작업 지시서 등)하여 증명합니다.</span>
                        </li>
                        <li class="flex items-start gap-2 bg-white p-2 rounded text-gray-900 font-bold border border-gray-200 shadow-sm">
                            <span class="text-blue-900 font-bold">✓</span>
                            <span>임금 지급 시 중간관리자를 배제하고, 반드시 약정된 지정일에 <strong>각 근로자 개인 명의 은행 계좌로 원천징수 대상 조세(갑근세, 주민세) 및 4대 보험료를 공제한 후 회사에서 직접 송금</strong>합니다. (제3자 일괄 지급 원천 금지)</span>
                        </li>
                        <li class="flex items-start gap-2">
                            <span class="text-blue-900 font-bold">✓</span>
                            <span>작업 수행 중 발생한 소모품, 식대, 제반 경비는 모두 회사의 법인카드로 결제되거나 회사의 명의로 적격 증빙(세금계산서)을 수취하여 비용 처리됩니다.</span>
                        </li>
                    </ul>
                </div>
                
                <!-- 불법 (단속팀 패널) -->
                <div class="bg-red-50 border border-red-200 p-6 rounded-2xl shadow-md hover:shadow-lg transition duration-300">
                    <h4 class="font-bold text-red-900 mb-3 text-lg border-b border-red-200 pb-2 flex items-center justify-between">
                        <span class="flex items-center gap-2"><span class="text-xl">❌</span> 위장 도급(파견법 위반) 구속 판례</span>
                    </h4>
                    <p class="mb-3 text-red-900 font-medium">관리 주체로서 소장은 형식적으로 존재하며, <strong>독립된 작업팀의 중간관리자가 자신의 소속 인원들을 임의로 통솔하여 당해 구역의 목적물을 임의로 시공</strong>합니다. (산재 발생에 따른 법률적 방어 불가)</p>
                    <ul class="list-none space-y-3 text-gray-900">
                        <li class="flex items-start gap-2">
                            <span class="text-red-900 font-bold">✖</span>
                            <span>정식 관리자의 실질적 통제가 결여되어 있고, 제3자(작업 반장)가 자신의 이윤 극대화 및 도급 목적 달성을 위해 편의에 따라 독단적 현장 지휘권을 행사합니다.</span>
                        </li>
                        <li class="flex items-start gap-2 bg-white p-2 rounded text-gray-900 font-bold border border-gray-200 shadow-sm">
                            <span class="text-red-900 font-bold">✖</span>
                            <span>당해 월의 대금 지급 시 근로자의 개별 근무 시간에 비례하지 아니하고, <strong>특정 결과물(면적, 체적 등 공사 완성량)에 비례한 거액의 도급 대금이 중간관리자 측 타인 명의 계좌로 일괄 지불</strong>됩니다.</span>
                        </li>
                        <li class="flex items-start gap-2">
                            <span class="text-red-900 font-bold">✖</span>
                            <span>지급받은 총액 중 중간관리자가 임의로 불법체류 자 등 미등록 인원의 임금을 배분하고 잔액을 부당 취득하는 <strong>전형적인 다단계 불법 하도급 계약 구조로서, 적발 시 즉각적인 건설 면허 취소 및 형벌 사유</strong>가 됩니다.</span>
                        </li>
                    </ul>
                </div>
            </div>
            
            <div class="mt-6 p-5 bg-gray-50 border border-gray-300 rounded-xl shadow-sm">
                <h4 class="font-bold text-gray-900 mb-3 border-b border-gray-300 pb-2 flex items-center gap-2"><span>📚</span> 참조 출처 및 관련 판례/행정해석</h4>
                <ul class="list-disc pl-5 space-y-2 text-sm text-gray-700">
                    <li><strong class="text-gray-900">도급과 근로자파견의 구별 기준:</strong> 대법원 2015. 2. 26. 선고 <a href="https://www.law.go.kr/precSc.do?menuId=7&subMenuId=47&tabMenuId=213&query=2010%EB%8B%A4106436" class="text-blue-600 hover:text-blue-800 underline" target="_blank" rel="noopener noreferrer">2010다106436 판결</a> (국가법령정보센터 | 독립적 사업 경영 주체성과 노무 종속성 판단 기준 제시)</li>
                    <li><strong class="text-gray-900">실질적인 하도급(위장도급) 판단:</strong> 대법원 2015. 8. 27. 선고 <a href="https://www.law.go.kr/precSc.do?menuId=7&subMenuId=47&tabMenuId=213&query=2013%EB%8F%846939" class="text-blue-600 hover:text-blue-800 underline" target="_blank" rel="noopener noreferrer">2013도6939 판결</a> (국가법령정보센터 | 노무 공급 및 관리 실태에 따른 무등록 하도급 인정 사례)</li>
                    <li><strong class="text-gray-900">파견근로자 보호 지침:</strong> <a href="https://www.law.go.kr/admRulSc.do?menuId=5&subMenuId=41&tabMenuId=183&query=%ED%8C%8C%EA%B2%AC%EA%B7%BC%EB%A1%9C%EC%9E%90" class="text-blue-600 hover:text-blue-800 underline" target="_blank" rel="noopener noreferrer">파견근로자보호 등에 관한 법률 행정규칙</a> (국가법령정보센터 | 위장도급 점검 매뉴얼)</li>
                </ul>
            </div>''',
            11
        ),
        (
            '12. [실무 심화] 물품 납품 계약과 건설 도급 공사의 명확한 구별', 
            '''<h2 class="text-3xl font-extrabold mb-6 text-gray-900 border-b-2 border-slate-200 pb-3">자재의 매매인가, 설치 시공을 수반한 도급인가?</h2>
            <p class="text-lg text-gray-900 mb-8 leading-relaxed">자재(창호재, 시스템 비계, 구조용 철골 등)를 외부에서 가공하여 현장으로 반입하는 일련의 과정에 있어서, 당초의 행위가 민법상 <strong>'단순 물품 매매(납품)'</strong>에 그치는가, 반면 건산법 규제가 엄격히 적용되는 <strong>'건설공사의 하도급'</strong>으로 포섭되는가를 분별하는 것은 건설사의 법적 리스크 관리에 직결됩니다. 만일 순수 '물품 납품'으로 소명될 경우, 해당 조달 업체는 건산법상 직접시공 의무, 현장대리인 상주, 등록 취소 등의 법적 책임으로부터 자유롭습니다.</p>
            
            <div class="grid lg:grid-cols-2 gap-8 mb-8">
                <!-- 물품공급납품 블록 -->
                <div class="bg-indigo-50 border-2 border-indigo-200 rounded-2xl shadow p-6">
                    <h3 class="text-xl font-bold text-indigo-900 border-b border-indigo-300 pb-3 mb-4 flex items-center gap-2">
                        <span class="bg-indigo-100 text-indigo-900 rounded-full w-8 h-8 flex items-center justify-center border border-indigo-300">1</span> 
                        안전한 법적 지위: 단순 제작 및 인도 (물품공급 계약)
                    </h3>
                    <p class="text-sm text-gray-900 mb-4 leading-relaxed font-medium">설계 도면과 시방서(Specification)에 따라 자사 혹은 타 외주 가공 시설에서 목적물을 특정한 규격으로 제작·가공한 후, <strong>해당 목적물을 당해 건설 현장에 운반하여 하차, 인도함으로써 이행이 완료</strong>된다면 이는 건산법이 규율하지 않는 '가공물 매매' 또는 '물품 위탁' 행위입니다.</p>
                    
                    <ul class="space-y-4 text-sm text-gray-900">
                        <li class="flex items-start gap-3 bg-white p-4 rounded-lg border border-gray-200 shadow-sm">
                            <span class="text-indigo-600 font-bold text-lg mt-0.5">💡</span>
                            <div><strong class="text-gray-900 text-base block mb-2">무면허 조달이 허용되는 물품 품목 (납품)</strong>
                            사전 가공된 철근, 굳지 않은 콘크리트(레미콘), 공장 가공된 철골 구조물, 규격화된 조명 및 가구재 하차 작업. 이러한 단순 인도에는 별도의 건설업 면허나 안전관리자 상주 의무가 부과되지 않습니다. (단, 하도급거래 공정화 법률상 제조 위탁의 적용은 받을 수 있습니다.)</div>
                        </li>
                        <li class="flex items-start gap-3 bg-red-50 p-4 rounded-lg border border-red-200 shadow-sm">
                            <span class="text-red-700 font-bold text-lg mt-0.5">⚠️</span>
                            <div class="leading-relaxed"><strong class="text-red-900 text-base block mb-2">권리 침해의 위험: "서비스 성격의 현장 부착 및 설치"</strong>
                            단순 자재 조달 계약이라 하더라도, 납품 업체의 직원이 당해 공사 현장에 부수적으로 파견되어 자재에 대한 <strong>용접, 조립, 앵커 체결 등 물리적인 "현장 가공 및 고정 부착 행위(설치 시공)"를 조금이라도 수행한 경우,</strong> 이는 명백히 '무면허자에 의한 건설공사 시행'으로 기소 대상이 됩니다. 서류 명칭과 무관하게 계약의 실질은 당해 면허가 필요한 <strong>건설업 하도급 시공</strong>으로 법원이 해석하게 됩니다.</div>
                        </li>
                    </ul>
                </div>
                
                <!-- 강구조물 외주가공 블록 -->
                <div class="bg-white border-2 border-emerald-300 rounded-2xl shadow p-6 relative">
                    <div class="absolute -right-3 -top-3 bg-emerald-100 text-emerald-900 border border-emerald-300 font-bold px-4 py-1.5 rounded-full text-xs shadow-md z-10">실무 법리 및 주요 판례 요지</div>
                    <h3 class="text-xl font-bold text-emerald-900 border-b border-emerald-200 pb-3 mb-4 flex items-center gap-2">
                        <span class="bg-emerald-50 text-emerald-900 rounded-full w-8 h-8 flex items-center justify-center border border-emerald-300">2</span> 
                        "기성품 가공 외주(납품) + 자가 직영 체결"의 적법한 분리
                    </h3>
                    <p class="text-sm text-gray-900 mb-4 leading-relaxed">전문건설업체 A사가 대규모 철골 시공 계약을 수주하였으나 조제 여건이 부합하지 않아, 제작 공장만을 구비한 타사 B에게 "부재에 대한 가공·제작과 인도(납품)"만을 한정 위탁하고, 해당 부재가 현장에 도달한 즉시 <strong>A사의 적법 면허와 자사 소속 근로자 및 통제 장비를 투입하여 단독으로 조립과 철골 세우기 공사를 완수</strong>하였다면 이는 법률에 부합하는 적법한 공정입니다.</p>
                    
                    <div class="bg-gray-50 text-gray-900 p-5 rounded-xl border border-gray-200 text-sm shadow-sm mt-5">
                        <strong class="text-gray-900 text-[15px] font-bold block mb-3 border-b border-gray-300 pb-2">💡 대법원 및 소관부처 유권해석: <span class="bg-white px-2 py-1 rounded text-emerald-800 border border-emerald-100">"핵심 물리적 타설·세립 행위의 직영수행 여부"</span></strong>
                        <ul class="list-none space-y-4">
                            <li class="flex gap-3">
                                <span class="text-emerald-700 font-bold mt-0.5">❶</span>
                                <div><strong class="text-gray-900 block mb-1">책임 주체의 귀속 분리:</strong> 건산법이 엄단하는 '하도급'은 목적물이 축조되는 <strong>"건설 현장 내에서의 본질적 시공 역무"를 타인에게 일괄 전가하는 행위</strong>에 국한됩니다. 현장에서 이탈된 독립 공장에서 물리력을 가해 제작된 후 현장 부지로 인도되는 행위 자체는 <strong>'자재 부속의 매매 조달'</strong>이므로 금지되는 재하도급 법리에 상응하지 아니합니다.</div>
                            </li>
                            <li class="flex gap-3">
                                <span class="text-emerald-700 font-bold mt-0.5">❷</span>
                                <div><strong class="text-gray-900 block mb-1">시공 권한의 고유성 수호:</strong> 부재를 타 업체로부터 매입 및 인도받았더라도, 이를 수직 시공하고 조립(Erection)하는 <strong>공정의 안전 관리 및 지시 이행 통제 전반을 A사의 기술 인력이 독점 실행</strong>하였다면 이는 해당 전문건설사가 준공 책임을 오롯이 실현한 <strong>적법한 직접 시공 의무 충족</strong>으로 판단됩니다.</div>
                            </li>
                            <li class="flex gap-3 bg-red-50 p-4 rounded-lg border border-red-100 mt-2">
                                <span class="text-red-700 font-bold mt-0.5 text-lg">⚠️</span>
                                <div class="text-gray-900"><strong class="text-red-900 block mb-1">법적 책임 전소의 위험 요건:</strong> 그러나, 자재 가공업자 B 측이 부재 납품에 부수하여 해당 <strong>자사 전문 세립공(조립원)과 운반 및 타설 기기를 투입하여 직접 조립 완수 절차까지 단독 전담</strong>하고, A사는 실소요비용으로 통합 정산하는 행위는 납품의 외피를 쓴 <strong>"건설 시공의 불법 일괄 하도급"</strong>으로 규정되어, B는 무면허 건설 시공, A사는 불법 재하도급으로 관계 법령에 의해 중징계를 받게 됩니다.</div>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
            
            <div class="mt-6 p-5 bg-gray-50 border border-gray-300 rounded-xl shadow-sm">
                <h4 class="font-bold text-gray-900 mb-3 border-b border-gray-300 pb-2 flex items-center gap-2"><span>📚</span> 참조 출처 및 관련 판례/행정해석</h4>
                <ul class="list-disc pl-5 space-y-2 text-sm text-gray-700">
                    <li><strong class="text-gray-900">제작물공급계약의 건설산업기본법 적용 여부:</strong> 대법원 2018. 10. 12. 선고 <a href="https://www.law.go.kr/precSc.do?menuId=7&subMenuId=47&tabMenuId=213&query=2018%EB%8F%848777" class="text-blue-600 hover:text-blue-800 underline" target="_blank" rel="noopener noreferrer">2018도8777 판결</a> (국가법령정보센터 | 단순 제작·납품과 시공 분리의 적법성 기준 제시)</li>
                    <li><strong class="text-gray-900">물품납품·설치계약의 실질:</strong> 대법원 2011. 12. 8. 선고 <a href="https://www.law.go.kr/precSc.do?menuId=7&subMenuId=47&tabMenuId=213&query=2010%EB%8F%8410065" class="text-blue-600 hover:text-blue-800 underline" target="_blank" rel="noopener noreferrer">2010도10065 판결</a> (국가법령정보센터 | 설치 행위가 수반된 납품의 불법 건설 하도급 인정 사례)</li>
                    <li><strong class="text-gray-900">건설산업기본법 원문/해석례:</strong> <a href="https://www.law.go.kr/lsSc.do?menuId=1&subMenuId=15&tabMenuId=81&query=%EA%B1%B4%EC%84%A4%EC%82%B0%EC%97%85%EA%B8%B0%EB%B3%B8%EB%B2%95" class="text-blue-600 hover:text-blue-800 underline" target="_blank" rel="noopener noreferrer">건설산업기본법 (국가법령정보센터)</a></li>
                </ul>
            </div>''',
            12
        ),
        (
            '13. [실무 심화] 건설기계 대여와 도급의 판별 및 통제 권한 증빙 매뉴얼', 
            '''<h2 class="text-3xl font-extrabold mb-6 text-gray-900 border-b-2 border-slate-200 pb-3">건설 장비 투입의 적법성 심의: 단순 임대차와 위장 도급 계약</h2>
            <p class="text-lg text-gray-900 mb-8 leading-relaxed">펌프카, 굴삭기, 타워크레인 등 대형 기계 자원을 동원함에 있어서, 해당 권리관계가 노무 및 통제권을 단일한 시간에 구속시키는 <strong>'건설기계 임대차'</strong>로 한정될 때에만 합법성을 보장받습니다. 반면 단가 등 물량 책임 조건이 결합한 <strong>'결과 보수 약정'</strong>의 외관을 띠는 순간 장비 대여자는 곧바로 무면허 건설 도급업자로 적발되어 처벌의 대상이 됩니다.</p>

            <div class="space-y-6">
                <!-- 임대차/렌트 (합법) -->
                <div class="bg-indigo-50 border border-indigo-200 rounded-lg p-6 shadow-sm flex flex-col md:flex-row gap-6 hover:shadow-md transition">
                    <div class="w-full md:w-1/3 border-b-2 md:border-b-0 md:border-r-2 border-indigo-200 pb-4 md:pb-0 md:pr-4">
                        <h3 class="text-xl font-bold text-indigo-900 mb-2">1. 적법한 조달: 장비 임대차 약정<br><span class="text-sm font-semibold text-indigo-700 block mt-1">(단순 건설기계 대여)</span></h3>
                        <p class="text-sm text-gray-900 leading-relaxed">계약 당사자가 기계 설비와 해당 기기를 운용할 지정 조종사 1인을 일정 시간 동안 당해 현장에 존속 대여하는 전형적 임대차 형태입니다.</p>
                    </div>
                    <div class="w-full md:w-2/3 bg-white p-5 rounded-lg border border-indigo-100">
                        <h4 class="font-bold text-gray-900 border-b border-gray-200 pb-2 mb-3">적법성(면허 불필요) 판단의 3대 요건</h4>
                        <ul class="list-disc pl-5 text-sm text-gray-900 space-y-3">
                            <li class="leading-relaxed"><strong class="text-gray-900">정산 기준의 시간 비례성:</strong> 급여(대금)의 조건이 장비 가동 시간(월대, 일대비 기준)으로 체결됩니다. <strong>"이동한 자재의 톤(t)수나 굴착해 낸 잉여 토사의 부피적 수량(㎥)" 성격을 띤 목적의 완성과 비례한 성과 단가 조항은 용인되지 않습니다.</strong></li>
                            <li class="leading-relaxed"><strong class="text-gray-900">사용자의 직접 지시·통제 (종속성 유지):</strong> 건설업자의 적격 보유 <strong>현장대리인 등 직원이 당해 장비 운용 기호에게 직접적인 지위와 안전 관리, 상세 공정 통제</strong>명령을 발부하여야 합니다. 작업의 속도나 방식에 기사의 자율적 통제가 인정되지 않습니다.</li>
                            <li class="leading-relaxed"><strong class="text-red-900">건설업 종사자 대금 보호 권리 (특칙):</strong> 장비 임대가 이행됨과 동시에, 건설사는 체불 분쟁을 억제하기 위한 제반 <strong>"건설기계 대여대금 지급보증서"</strong>를 대여 업체(기사)에게 법정 강제 교부해야 하며, 미발급 시 해당 영업 사업에 대해 중징계 행정처분이 과해집니다.</li>
                        </ul>
                    </div>
                </div>

                <!-- 도급/물량위장 (불법) -->
                <div class="bg-red-50 border border-red-200 rounded-lg p-6 shadow-sm flex flex-col md:flex-row gap-6 hover:shadow-md transition">
                    <div class="w-full md:w-1/3 border-b-2 md:border-b-0 md:border-r-2 border-red-200 pb-4 md:pb-0 md:pr-4">
                        <h3 class="text-xl font-bold text-red-900 mb-2">2. 불법적 위장 약정: 결과 보증식 장비 도급<br><span class="text-sm font-semibold text-red-700 block mt-1">(불법 하도급/무등록 시공 사유)</span></h3>
                        <p class="text-sm text-gray-900 leading-relaxed">서면상으로는 임대차 계약의 외양을 가장하였으나, 이행의 실체가 <strong>"장비 측이 목적 결과를 스스로 기획하고 완수하는 도급 체계"</strong>에 해당하는 행위.</p>
                    </div>
                    <div class="w-full md:w-2/3 space-y-4">
                        <div class="bg-white p-5 rounded-lg border border-red-100 shadow-sm relative">
                            <span class="absolute right-3 top-3 text-xs bg-red-100 text-red-800 px-2 py-1 rounded font-bold">주요 적발 사안 A</span>
                            <h4 class="font-bold text-gray-900 text-[15px] mb-2">총괄적 턴키(Turn-key) 방식의 독립 타설 공정</h4>
                            <p class="text-sm text-gray-900 leading-relaxed">특정 물량(예: 바닥 콘크리트 300㎥) 타설 공정을 의뢰하며, 장비 소유주가 자체적으로 타설 기사와 양생 인부 등을 자율 통솔하여 동원한 후 산출된 물량 단위의 요율을 적용하여 부대 금액 일체를 정산받는 경우. <br>
                            &rarr; 원청 지휘권이 배제되고 결과물 보증(도급) 의무를 띤 자립적 계약으로 간주하여 무등록 시공 및 불법 하도급으로 판단 및 처벌.</p>
                        </div>
                        <div class="bg-white p-5 rounded-lg border border-red-100 shadow-sm relative">
                            <span class="absolute right-3 top-3 text-xs bg-red-100 text-red-800 px-2 py-1 rounded font-bold">주요 적발 사안 B</span>
                            <h4 class="font-bold text-gray-900 text-[15px] mb-2">물량 단위에 비례한 제반비용 일괄 정산 방식</h4>
                            <p class="text-sm text-gray-900 leading-relaxed">지하 터파기 반출 현장 등에서 특정 장비 대여 업체 연합에 <em>"현장의 토사를 산출된 톤 단위로 임의 처리하며 대가로 사전에 정해진 반출 실적 단가를 정산한다"</em>라고 위탁하는 경우.<br>
                            &rarr; 장비 운용을 넘어선 당해 작업 결과(토사 처리 완수)의 실적 도급으로서 건설 면허(토공사업)를 수반치 아니하므로 불법 행위입니다.</p>
                        </div>
                        <div class="mt-4 p-4 bg-yellow-50 text-gray-900 text-sm rounded-lg border border-yellow-200">
                            <strong class="text-gray-900 flex items-center gap-2 mb-1"><span>🔍</span> 행정감사 시 증빙 식별 요점:</strong> 수사 권한을 지닌 감사관은 당해 거래 내역의 기반인 <strong>"거래명세표 및 부가가치세 세금계산서의 기재 항목"</strong>을 일차적으로 추적합니다. 시간(Hour) 등의 가동 일수 비례가 아닌, <strong class="text-gray-900 font-extrabold bg-yellow-100 px-1 rounded">"루베(㎥), 톤(ton), 면적(㎡)" 등 일괄 체적의 결과 단가</strong> 명칭이 기재되어 있다면 법규 위반(다단계 하도급 금지 등) 결정의 확정적 증거로 소추됩니다.
                        </div>
                    </div>
                </div>
            </div>

            <div class="mt-10 p-8 bg-gray-50 rounded-2xl shadow-sm text-gray-900 border border-gray-200">
                <h3 class="text-xl font-bold text-gray-900 mb-5 border-b border-gray-300 pb-3 flex items-center gap-2">
                    <span class="text-2xl text-blue-600">🛡️</span> 적법한 직영 관리 통제를 입증하는 3원적 실무 방어 매뉴얼
                </h3>
                <p class="text-[15px] text-gray-900 mb-6 leading-relaxed">특정한 외부 인력을 활용하여 공사를 수행하더라도, 이를 <strong>온전한 '적법 직영 시공'의 범위 내로 통제 및 소명하기 위해선, 기업 차원의 계약 및 자금의 분리 체계가 완연히 분산</strong>되어 있어야 객관성과 소명력을 갖출 수 있습니다.</p>
                
                <ul class="space-y-4 text-sm text-gray-900">
                    <li class="bg-white p-5 rounded-xl border border-gray-200 shadow-sm">
                        <strong class="text-gray-900 font-bold text-base block mb-3">❶ 자금 집행의 개별화와 전자 시스템 구축 분리</strong>
                        <p class="leading-relaxed">특정 작업 반장 등의 통합 개체에 하도급 대금을 총괄 이체하는 관습을 절대적으로 배제하여야 합니다.<br>
                        - 장비 동원: <strong>당해 법인에 대한 개별적 '건설기계 임대차 계약서(일 단위 정산)'</strong>에 기초한 전신 송금.<br>
                        - 자재 대금: <strong>자재 제조사에 대한 독립적 '단순 물품 매매 약정서'</strong>에 기한 지급.<br>
                        - 현장 인력 노무: <strong>일용직 근로자 개개인과의 직접 '근로계약서'</strong>에 의거한 임금 직접 송금.<br>
                        이 세 가지 회계 내역이 제3자 개인 통장에 병합하여 지불되지 않아야 합니다.</p>
                    </li>
                    <li class="bg-white p-5 rounded-xl border border-gray-200 shadow-sm">
                        <strong class="text-gray-900 font-bold text-base block mb-3">❷ 현장대리인 중심의 지휘감독 문서 및 제반 증명 이력 편철</strong>
                        <p class="leading-relaxed">서류상 소장이 아닌 실효적 관리자임을 입증하기 위하여 일별 작업 전 회의(TBM), 안전교육 관리, 작업 계획 지시서 등을 필수적으로 축적해야만 합니다. 당해 소장에 의해 매일 현장 투입 기사와 고용 근로자에게 <strong>직접적인 작업 영역 배분과 안전 공정 통제 등의 명시적인 세부 통제 권한이 작위 되었음을 시각화한 문서(작업일지, 조치 이행서, 사진 첨부 증명)</strong>가 상시 존재해야 합니다.</p>
                    </li>
                    <li class="bg-white p-5 rounded-xl border border-gray-200 shadow-sm">
                        <strong class="text-gray-900 font-bold text-base block mb-3">❸ 근로 임금의 원천징수 직접 신고 및 제3자 임금 지불 관여 절대 배제</strong>
                        <p class="leading-relaxed">무등록 반장에게 전체 총무권(근로자 인적 정보 관리, 세무 공제, 임금 분할 직접 권한)을 전권 위임할 경우 명의 대여 및 조세 포탈, 파견법의 직접 위반으로 제재에 처합니다. <strong>반드시 본사 재무담당자가 해당 근로자 1인별 기초 주민 명단과 근태 일수를 회수·파악해, 회사 통제하에 법적 공제(갑근세, 4대 보험 대납)를 완료한 순직접성 임금을 근로 당사자의 명의 계좌로 직불 결제 송금</strong>하여야만 규제 당국의 면책 조사 절차를 적법하게 극복하게 됩니다.</p>
                    </li>
                </ul>
            </div>''',
            13
        )
    ]

    for title, content, order in lessons:
         cursor.execute('''
            INSERT INTO lesson (title, content, "order", course_id)
            VALUES (?, ?, ?, ?)
        ''', (title, content, order, course_id))
        
    conn.commit()
    conn.close()
    print("[실무 심화 11강~13강 분석편] 데이터베이스 테이블 시딩 완료")

if __name__ == '__main__':
    seed_law_course_ultimate_pt3()
