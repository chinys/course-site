import os

filepath = r'd:\workai\course-site\course-site\scripts\_section_a.py'
with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

# Split into A-1 and the rest (A-2/A-3)
parts = text.split('<!-- A-2: 외주 사급가공 계약서')
if len(parts) == 2:
    a1_part = parts[0]
    rest_part = parts[1]
    
    # In rest_part (A-2 and A-3), replace "발주자" with "甲" and "수급자" with "乙"
    # carefully. We already have '위탁자(이하 "甲")' because of my manual replaces.
    # What about 발주자/수급자 in quotes and text?
    rest_part = rest_part.replace('"발주자"', '"甲"')
    rest_part = rest_part.replace('"수급자"', '"乙"')
    
    # Also without quotes, just in case "발주자가 직접", "수급자는"
    # Actually modifying "발주자" to "甲" is good, but "발주자는" -> "甲은" or stays "甲는"?
    # The user asked: "위탁자, 수탁자로만 통일해 주고 발주자나 수급자 용어는 제거해 줘. 그리고 갑지 맨 위쪽에 '상기의' 라는 부분은 제거해야 하지 않을까?"
    # Oh! The user said "위탁자, 수탁자로만 통일해주고 발주자나 수급자 용어는 제거해 줘".
    # And then "위탁자, 수탁자라고 하고 A-1처럼 갑, 을 추가는 가능해".
    
    # So wherever it says "발주자" -> "위탁자", "수급자" -> "수탁자".
    # WAIT! "발주자" -> "위탁자"("甲")
    # Let's just replace in general conditions A-2/A-3:
    # "발주자" -> "甲"
    # "수급자" -> "乙"
    # Or "발주자" -> "위탁자"
    # Let me replace exactly what's needed.
    
    # The previous instruction was: 
    # "\"발주자\"" -> "\"甲\""
    # "\"수급자\"" -> "\"乙\""
    # Let's do that for now. Wait, replacing "발주자" with "위탁자" and "수급자" with "수탁자" might be safer for grammatical markers (은/는/이/가).
    # "발주자가" -> "위탁자가"
    # "발주자는" -> "위탁자는"
    # "수급자가" -> "수탁자가"
    # "수급자는" -> "수탁자는"
    # Since Korean particles for 주자(ja) and 탁자(ja) end in the exact same vowel, the particles match perfectly!
    # "발주자" -> "위탁자"
    # "수급자" -> "수탁자"
    # Then I will replace "위탁자(\"발주자\")" -> "위탁자(\"甲\")", etc.
    
    rest_part = rest_part.replace('발주자', '위탁자')
    rest_part = rest_part.replace('수급자', '수탁자')
    
    # Clean up double "위탁자(위탁자)" if they happen
    rest_part = rest_part.replace('위탁자(위탁자)', '위탁자')
    rest_part = rest_part.replace('수탁자(수탁자)', '수탁자')
    rest_part = rest_part.replace('위탁자("위탁자")', '위탁자("甲")')
    rest_part = rest_part.replace('수탁자("수탁자")', '수탁자("乙")')
    
    # Reassemble
    new_text = a1_part + '<!-- A-2: 외주 사급가공 계약서' + rest_part
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_text)
    print('Replacements done successfully.')
else:
    print('Split failed.')
