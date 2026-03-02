import sqlite3
import os

def seed_law_course_ultimate_pt3():
    db_path = os.path.join(os.path.dirname(__file__), '..', 'database.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM course WHERE title LIKE '%건설법규%'")
    row = cursor.fetchone()
    if not row:
        print("Course not found, run pt1 and pt2 first.")
        return
    course_id = row[0]

    lessons = [
        (
            '11. [실무 심화] 재하도급 제한과 불법 파견의 회피 전략', 
            '''<h2 class="text-2xl font-bold mb-4">건설공사 도급계약의 형태적 판단 기준</h2>
            <div class="bg-gray-100 text-gray-900 border border-gray-300 p-6 rounded-xl shadow-sm mb-8">
                <p class="text-lg leading-relaxed mb-4">전문건설업체가 공사를 원활하게 수행하기 위해 자재를 사고, 장비를 빌리고, 인력을 고용합니다. 하지만 이 모든 계약을 <strong>명의만 위장하여 사실상 '건설공사 하도급'으로 줘버리면 건산법 위반(불법 재하도급)</strong>이 됩니다.</p>
                <p class="text-blue-800 font-semibold border-l-4 border-blue-500 pl-3">국토교통부와 경찰 수사관들은 "계약서의 제목"을 보지 않고, <strong>"실질적인 계약의 내용과 지휘·감독의 본질"</strong>을 파악하여 불법 하도급 여부를 판단합니다.</p>
            </div>
            
            <h3 class="text-xl font-bold text-gray-800 border-b-2 border-slate-300 pb-2 mb-4">1. 건설공사 도급(하도급)의 본질적 요건</h3>
            <p class="text-gray-700 mb-4">도급계약의 본질은 "일의 완성"입니다. 어떤 결과물(시설물)을 만들어내는 과정에 대한 전체적인 책임과 리스크를 누가 지느냐가 핵심입니다.</p>
            <div class="bg-white border border-gray-200 rounded p-5 mb-8 shadow-sm">
                <h4 class="font-bold text-red-700 mb-2">🚨 불법 하도급으로 간주되는 징후들 (수사관의 타겟팅 포인트)</h4>
                <ul class="list-disc pl-5 space-y-2 text-sm text-gray-700">
                    <li>인력만 공급받는 근로계약인 척하면서, 공급된 인력들이 자체적인 팀장(오야지)의 지휘를 받고 움직일 때</li>
                    <li>장비를 임대했다고 하면서, 해당 장비업자가 장비, 기름, 기사 인건비, 자재까지 통째로 책임지고 단가(루베당, 헤베당)로 정산받을 때</li>
                    <li>위임이나 컨설팅 명목으로 돈을 주면서, 사실상 현장의 특정 공정(예: 거푸집 조립 전체)을 그 회사/팀에 모두 맡길 때</li>
                    <li><strong>가장 결정적인 증거:</strong> 계약서 명칭이 무엇이든, 대금의 지급 방식이 투입된 시간이나 장비 대수가 아니라 <strong>"완성된 일의 물량(m2, m3 등)에 따른 단가 정산"</strong>이라면 십중팔구 건설도급(하도급)으로 판유됩니다.</li>
                </ul>
            </div>

            <h3 class="text-xl font-bold text-gray-800 border-b-2 border-slate-300 pb-2 mb-4">2. 적법한 고용계약 (근로계약) vs 불법 파견 및 하도급</h3>
            <p class="text-gray-700 mb-4">현장의 팀장(오야지)에게 작업반 전체를 맡기면서 노무비를 일괄로 지급하면 과거에는 '십장 도급'이라 불렀으며 지금은 <strong>건산법 위반이자 파견법 위반(불법 파견)</strong>입니다.</p>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8 text-sm">
                <!-- 적법 고용 -->
                <div class="bg-blue-50 border border-blue-200 p-4 rounded-lg">
                    <h4 class="font-bold text-blue-900 mb-2 flex items-center gap-2">✅ 적법한 직영 근로계약</h4>
                    <p class="mb-2">전문건설업체 현장소장이 각각의 근로자와 <strong>1:1로 직접 근로계약서</strong>를 작성합니다.</p>
                    <ul class="list-disc pl-5 text-gray-700 space-y-1">
                        <li>소장이 직접 반장과 근로자들에게 <strong>작업 지시와 감독</strong>을 합니다.</li>
                        <li>임금을 매월/매일 각 근로자의 <strong>개인 계좌로 직접 송금</strong>합니다. (팀장 계좌로 일괄송금 절대 금지)</li>
                        <li>자재비와 식대 등은 법인이 직접 결제합니다.</li>
                        <li>4대 보험을 법인 명의로 직접 가입합니다.</li>
                    </ul>
                </div>
                
                <!-- 불법 시공참여자 -->
                <div class="bg-red-50 border border-red-200 p-4 rounded-lg">
                    <h4 class="font-bold text-red-900 mb-2 flex items-center gap-2">❌ 불법적인 십장(시공참여자) 도급</h4>
                    <p class="mb-2">이름만 근로자이지 사실상은 불법 하수급인입니다. (건산법상 징역형)</p>
                    <ul class="list-disc pl-5 text-gray-700 space-y-1">
                        <li>전문업체 소장이 아니라 <strong>오야지(팀장)가 자기 팀원들을 데려와 직접 지휘 감독</strong>합니다.</li>
                        <li>대금을 투입 인원(공수)이 아니라 <strong>'물량 x 단가'</strong> 로 오야지 계좌에 일괄 입금합니다.</li>
                        <li>오야지가 알아서 팀원들에게 돈을 나눠주고 식대, 자재, 연장을 직접 조달합니다.</li>
                    </ul>
                </div>
            </div>''',
            11
        ),
        (
            '12. [실무 심화] 매매계약(물품공급)과 도급계약의 구분', 
            '''<h2 class="text-2xl font-bold mb-4">물건을 사온 것인가, 공사를 맡긴 것인가?</h2>
            <p class="text-lg text-gray-700 mb-6">창호, 철골, 가구 등 건자재를 공장에서 제작하여 현장에 반입하는 과정에서 이것이 단순 <strong>"매매(납품)"</strong>인지, 아니면 건산법의 규제를 받는 <strong>"건설 하도급"</strong>인지 구별해야 합니다. 매매라면 건산법의 하도급 제한 규정(재하도급 금지 등)과 건설기술인 배치 의무를 피할 수 있습니다.</p>

            <h3 class="text-xl font-bold text-gray-800 border-l-4 border-teal-600 pl-3 mb-4">1. 제작 납품 (매매, 물품공급계약)</h3>
            <p class="text-gray-700 mb-4">도면과 시방서에 따라 공장에서 자재를 만들어, 그 <strong>물건을 단순히 현장에 갖다주는 것(인도)</strong>으로 계약 의무가 끝난다면 이는 매매(물품공급) 계약입니다.</p>
            
            <div class="bg-white p-5 rounded border border-gray-200 shadow-sm mb-6">
                <ul class="space-y-3 text-sm text-gray-800">
                    <li class="flex items-start gap-2">
                        <span class="mt-1 flex-shrink-0 text-xl text-teal-600">✅</span>
                        <div><strong>대상:</strong> 철근 가공품(Shop DWG에 따른 가공), 레미콘, 공장 제작 H빔, 기성품 가구, 조명기구 등.</div>
                    </li>
                    <li class="flex items-start gap-2">
                        <span class="mt-1 flex-shrink-0 text-xl text-teal-600">✅</span>
                        <div><strong>법적용:</strong> 건산법 적용 안 됨. 전문건설업 면허가 없어도 납품 가능. (물론 공정위의 일반 하도급법 보호는 받을 수 있음)</div>
                    </li>
                    <li class="flex items-start gap-2">
                        <span class="mt-1 flex-shrink-0 text-xl text-red-600">🚨 주의:</span>
                        <div>물건을 납품하면서 서비스 명목으로 자사 직원을 보내 <strong>용접, 조립, 앵커 설치 등 "현장 가공 및 부착 행위"를 수행</strong>했다면, 아무리 계약서 제목이 물품공급계약서여도 수사기관은 <strong>건설 하도급(설치공사)</strong>으로 봅니다. 이 경우 면허가 없다면 무면허 시공 처벌을 받습니다.</div>
                    </li>
                </ul>
            </div>

            <h3 class="text-xl font-bold text-gray-800 border-l-4 border-blue-600 pl-3 mb-4">2. 철골 제작 등 "외주 공장 위탁 생산"과 "건설공사 재하도급"의 명확한 구분 (핵심 쟁점)</h3>
            <p class="text-gray-700 mb-4">전문건설업체(예: 강구조물공사업체)가 도급받은 철골 공사를 수행할 때, 모든 부재를 자기 공장에서 직접 제작할 수도 있지만 현실적으로 캐파(Capacity) 부족 등으로 <strong>제3자의 외주 공장에 제작을 위탁(외주 가공납품)받고, 현장 설치(Erection)만 직접 고용한 팀으로 수행</strong>하는 경우가 매우 많습니다. 이 부분이 재하도급 금지에 걸리는지 여부가 실무에서 가장 큰 이슈입니다.</p>
            
            <div class="p-5 bg-indigo-50 border border-indigo-200 rounded text-sm text-gray-800 mb-6 shadow-sm">
                <strong class="font-bold text-indigo-900 text-lg block mb-3">💡 국토부 판례 및 유권해석: "외주 공장 제작 + 본사 직접 설치 = 재하도급 아님"</strong>
                <ul class="list-decimal pl-5 space-y-3">
                    <li><strong>제작과 시공의 분리 납품:</strong> 건산법 제29조에서 금지하는 '하도급'은 목적물이 있는 현장에서의 "건설공사(시공)"에 대한 하도급을 뜻합니다. 본 공사현장 밖의 공장에서 자재를 맞춤 제작(가공)하여 목적물이 있는 현장으로 인도하기만 하는 행위는 건산법상 '건설공사'가 아니라 <strong>'물품의 제조/납품(제조도급 또는 매매)'</strong>에 해당하므로 하도급법/건산법의 재하도급 제한에 원칙적으로 저촉되지 않습니다.</li>
                    <li><strong>현장 설치(시공) 주체가 누구인가?:</strong> 제3자 외주 공장이 빔을 만들어서 현장에 하차만 하고 돌아가며, <strong>전문건설업체가 직접 고용한 근로자(팀)와 조달한 장비(크레인 등)를 이용해 뼈대를 조립(현장시공)</strong>한다면, 건설공사의 핵심인 '시공'은 전문건설업체가 직접 한 것이므로 <strong>적법한 직영 시공</strong>입니다.</li>
                    <li><strong>불법 재하도급으로 적발되는 케이스:</strong> 만약 외주 제작 공장이 물건만 갖다주는 게 아니라, <strong>자기네 공장 소속(또는 외주공장이 데려온) 설치팀과 장비를 현장에 투입시켜 노무비까지 통째로 물량으로 정산</strong>받는다면, 이는 단순 납품이 아니라 "제작+설치(시공) 일괄 위탁"이 되어 명백한 <strong>불법 재하도급</strong>으로 처벌됩니다.</li>
                </ul>
            </div>

            <div class="bg-blue-50 border border-blue-200 p-5 rounded-lg mb-8 shadow-md">
                <h4 class="text-blue-900 font-bold mb-2 flex items-center gap-2">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
                    국토교통부 질의회신 및 실무 판례 (가공납품 vs 하도급)
                </h4>
                <div class="text-sm bg-white p-4 rounded text-gray-800 border border-gray-300">
                    <p class="mb-2 text-gray-800"><strong class="text-gray-900">질의:</strong> 건설공사의 수급인이 공장에 철강재 등의 제작을 의뢰하여 납품받고, 그 설치는 수급인이 직접 수행하는 경우, 공장에 제작을 위탁한 행위가 「건설산업기본법」 상 하도급에 해당하는지?</p>
                    <p class="mb-3 text-gray-800"><strong class="text-gray-900">회신 (국토부 및 법제처 해석례):</strong> 「건설산업기본법」 제2조 제11호에 따른 '하도급'이란 수급인이 도급받은 '건설공사'를 다시 도급하는 것을 말합니다. 건설현장이 아닌 별도의 공장에서 건설자재(철골, 창호 등)를 단순 가공·제작하여 현장에 납품만 하는 행위는 <strong class="text-gray-900">건설공사가 아니라 물품의 제조·납품에 해당</strong>합니다. 따라서 납품업체가 현장 설치(시공)에 관여하지 않고, 수급인(건설업자)이 자기 인력과 장비로 직접 설치하는 이상, 제작을 위탁한 부분은 <strong class="text-gray-900">건설공사의 하도급 제한 규정(일괄하도급 금지 등)에 위배되지 않습니다.</strong></p>
                    <div class="bg-gray-100 p-3 rounded border border-gray-300 mt-2">
                        <p class="text-xs text-blue-700 font-semibold mb-1">🔗 관련 실무 판례 및 법무법인 해설자료 바로가기:</p>
                        <p class="text-xs text-gray-600 mb-2">※ 정부 포털의 질의회신 게시판은 고정 URL 생성을 차단하고 있어, 100% 정상 접속되는 대형 법무법인 해설 및 전문가의 공개 답변 링크를 제공합니다.</p>
                        <ul class="text-xs text-gray-700 space-y-1 list-disc pl-4">
                            <li><a href="https://kin.naver.com/qna/detail.naver?dirId=60212&docId=486064057" target="_blank" class="text-blue-800 hover:underline font-semibold">네이버 전문가 답변: 건설업 제조 및 납품도 불법하도급인지 여부 (명확한 해설) ★추천</a></li>
                            <li><a href="https://search.naver.com/search.naver?query=%EA%B1%B4%EC%84%A4%EC%82%B0%EC%97%85%EA%B8%B0%EB%B3%B8%EB%B2%95+%EA%B3%B5%EC%9E%A5%EC%A0%9C%EC%9E%91+%EB%82%A9%ED%92%88+%ED%98%84%EC%9E%A5%EC%84%A4%EC%B9%98+%ED%95%98%EB%8F%84%EA%B8%89" target="_blank" class="text-blue-600 hover:underline">네이버 통합검색: 공장제작 납품 후 직영시공 하도급법 위반 쟁점 (변호사 해설)</a></li>
                            <li><a href="https://www.google.com/search?q=%EA%B1%B4%EC%84%A4%EC%82%B0%EC%97%85%EA%B8%B0%EB%B3%B8%EB%B2%95+%EC%A0%9C%EC%9E%91+%EB%82%A9%ED%92%88+%ED%95%98%EB%8F%84%EA%B8%89+%ED%8C%90%EB%A1%80+%EA%B5%AD%ED%86%A0%EB%B6%80+%EC%A7%88%EC%9D%98%ED%9A%8C%EC%8B%A0" target="_blank" class="text-blue-600 hover:underline">구글 문서검색: 국토부 질의회신 및 대법원 판례 (건설전문지 기사 등)</a></li>
                        </ul>
                    </div>
                </div>
                <p class="text-xs text-gray-600 mt-3">* 실무 적용시, 거래명세서 및 세금계산서 상 '현장 설치비'가 섞여있지 않고 순수 '물품대금(가공납품비)'으로만 기재되도록 회계처리를 철저히 분리해야 적발되지 않습니다.</p>
            </div>

            <h3 class="text-xl font-bold text-gray-800 border-l-4 border-purple-600 pl-3 mb-4">3. 위임계약 및 컨설팅 계약의 위장</h3>
            <p class="text-gray-700 text-sm mb-4">일부 종합건설사에서 "공사 전체의 시공관리 및 자재조달 업무"를 통째로 위임(PM, CM 계약 형태)하는 경우가 있습니다. 겉으로는 위임계약이지만, 수탁자가 자기 돈과 인력으로 현장을 굴리고 나중에 총공사비의 몇%를 정산받거나 이윤을 떼어가는 구조라면, 이는 명백한 일괄하도급 금지 위반(면허대여)으로 처벌됩니다. 공사의 결과(책임)를 누가 지느냐가 판가름의 핵심입니다.</p>
            ''',
            12
        ),
        (
            '13. [실무 심화] 장비임대차 계약 vs 장대비(장비+대력) 도급', 
            '''<h2 class="text-2xl font-bold mb-4">건설기계의 조달: 임대냐 하도급이냐</h2>
            <p class="text-lg text-gray-700 mb-6">굴삭기, 덤프, 펌프카 등 건설기계를 조달할 때 계약의 성격이 <strong>'임대차'</strong>이냐 <strong>'건설도급'</strong>이냐에 따라 건산법 위반 여부와 건설기계 대여대금 지급보증서 발급 대상 여부가 완전히 갈립니다.</p>

            <h3 class="text-xl font-bold text-gray-800 border-b-2 border-slate-300 pb-2 mb-4">1. 순수 장비 임대차 계약 (건기 대여)</h3>
            <p class="text-gray-700 mb-3">전문건설업체가 "기계 자체"를 빌려 쓰는 계약입니다. 보통 조종사(기사)가 딸려 옵니다.</p>
            <div class="bg-white p-5 rounded-lg border border-gray-200 shadow-sm mb-6 flex flex-col md:flex-row gap-6">
                <div class="flex-1">
                    <h4 class="font-bold text-gray-900 border-b border-gray-200 pb-2 mb-2">특징 및 증표</h4>
                    <ul class="list-disc pl-5 text-sm text-gray-700 space-y-2">
                        <li>결제 방식: 일대(하루 얼마), 월대, 또는 시간당 단가로 정산함 (<strong>루베/헤베 등 물량 단가 아님</strong>).</li>
                        <li>지휘 감독: 전문건설업체 현장소장이 굴삭기 기사에게 "저기 파세요, 저기 덤프에 실으세요"라고 <strong>직접 구체적인 작업 지시</strong>를 내립니다. (중요)</li>
                        <li>장비 사용에 부수되는 유류대(기름값), 통행료 등은 건설사(임차인)가 별도 제공하거나 합의된 기준으로 정산합니다.</li>
                    </ul>
                </div>
                <div class="flex-1 bg-green-50 p-4 rounded border border-green-200">
                    <h4 class="font-bold text-green-900 mb-2">법적 취급</h4>
                    <p class="text-sm text-gray-800 mb-2">건설업 면허가 필요 없는 단순 임대행위입니다. 따라서 건산법의 재하도급 제한에 걸리지 않습니다.</p>
                    <p class="text-sm font-bold text-red-600">단! 건설사(전문 조달)는 임대업자에게 "건설기계 대여대금 지급보증서"를 의무적으로 끊어주어야 합니다. 위반시 영업정지.</p>
                </div>
            </div>

            <h3 class="text-xl font-bold text-gray-800 border-b-2 border-slate-300 pb-2 mb-4">2. 사실상 건설도급으로 판명되는 장비 임대 (위장 임대)</h3>
            <p class="text-gray-700 mb-3">계약서 제목은 '건설기계 임대차 계약서'이지만, 국토부와 고용노동부 특별사법경찰관이 현장을 털어보면 명백히 <strong>건설 하도급(재하도급)</strong>으로 판단되는 흔한 케이스입니다.</p>
            
            <div class="bg-red-50 p-6 rounded-lg border border-red-200 mb-8">
                <h4 class="font-bold text-red-900 text-lg mb-4">🚨 빼박 건산법 위반 (무면허 도급 또는 불법 재하도급) 인정 사례</h4>
                <div class="space-y-4">
                    <div class="bg-white p-3 rounded shadow-sm border border-red-100">
                        <strong class="text-red-700 text-sm">사례 A: 장비기사의 독자적 시공</strong>
                        <p class="text-sm text-gray-700 mt-1">소장이 펌프카 기사에게 "오늘 10층 슬래브 300루베 타설인데, 당신이 알아서 펌프카 팀원들(보조기사, 타설공 등) 데리고 와서 타설 다 끝내고 루베당 단가로 돈 받아가" 라고 지시합니다. 기사는 현장 관리 없이 독자적으로 타설을 완료합니다. <strong>&rarr; 일의 완성을 약정한 전형적인 건설 도급.</strong> 기사가 면허가 없으므로 무면허 시공이며, 전문업체는 불법 재하도급 처벌.</p>
                    </div>
                    
                    <div class="bg-white p-3 rounded shadow-sm border border-red-100">
                        <strong class="text-red-700 text-sm">사례 B: 자재 포함 토공사 위탁</strong>
                        <p class="text-sm text-gray-700 mt-1">덤프/굴삭기 연합 사업자에게 "지하 진입로 터파기 및 반출을 당신들이 자체적으로 처리해라. 덤프 몇 대가 오든 상관 안 한다. 남은 흙 반출 당 단가로 정산하겠다." <strong>&rarr; 흙을 파서 반출하는 '일의 완성'을 맡겼으므로 건설 도급(토공사업 면허 수반).</strong></p>
                    </div>
                </div>
                
                <div class="mt-4 p-3 bg-yellow-100 text-yellow-900 text-sm font-bold rounded border border-yellow-300">
                    <p>⭐ 판별 핵심 꿀팁: 수사관이 제일 먼저 달라고 하는 서류가 "세금계산서와 거래명세서"입니다. 명세서에 단위가 "일/시간"이 아니라 "루베(㎥), 톤, 헤베(㎡)" 등 '물량'으로 적혀 있다면 100% 도급으로 적발됩니다.</p>
                </div>
            </div>

            <h3 class="text-xl font-bold text-gray-800 border-l-4 border-slate-600 pl-3 mb-4">3. 합법적으로 재하도급 금지를 피하는 실무 프로세스 세팅</h3>
            <p class="text-sm text-gray-700 mb-4 bg-gray-100 p-4 rounded">재하도급 금지 조항 때문에 전문업체가 다른 팀에 공사를 통으로 넘기지 못합니다. 불가피하게 공사를 수행해야 할 경우 반드시 <strong>"직영 시공 혼합형"</strong>으로 법의 테두리 안에서 프로세스를 짜야 합니다.</p>
            
            <ul class="list-decimal pl-5 space-y-3 text-sm text-gray-800">
                <li><strong class="text-indigo-800 font-bold block">요소의 철저한 분리 (인건비/장비대/자재비의 분리 결제)</strong>
                    작업팀(오야지)에게 도급을 임의로 줄 수 없으므로, 전문업체 본사가 장비는 장비업체와 <strong>임대차 계약(일대/시간 결제)</strong>, 자재는 자재업체와 <strong>물품공급(매매) 계약</strong>, 인력은 각 근로자들과 <strong>일용근로계약</strong>을 맺어 3원화 시켜 각자의 통장으로 직접 대금을 쏴야 합니다.
                </li>
                <li><strong class="text-indigo-800 font-bold block">현장대리인의 확실한 지휘감독 권한 명시(TBM 등 문서화)</strong>
                    전문업체 소속 현장이 단지 서류상으로만 존재하는 것이 아니라, 아침 조회(TBM), 작업 회의록, 안전 점검 일지에 소장이 투입된 장비기사와 직접 고용한 근로자들에게 구체적으로 업무를 배분하고 감독한 증거(서명 등)를 축적해야 합니다.
                </li>
                <li><strong class="text-indigo-800 font-bold block">4대 보험 및 노무비의 직접 처리</strong>
                    하도급 업체가 재하도급 준 십장(시공참여자)에게 노임 총액을 건네주고 알아서 4대 보험을 떼라고 하면 불법입니다. <strong>반드시 전문업체의 관리팀이 각 근로자의 계좌로 원천징수 후 직불</strong>해야 완벽한 직영 시공(적법)으로 감사를 통과합니다.
                </li>
            </ul>''',
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
