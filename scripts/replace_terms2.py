import os
import io

filepath = r'd:\workai\course-site\course-site\scripts\_section_a.py'
with io.open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('<!-- A-2: 외주')
if idx != -1:
    a1_part = text[:idx]
    rest_part = text[idx:]

    rest_part = rest_part.replace('"발주자"', '"甲"')
    rest_part = rest_part.replace('"수급자"', '"乙"')
    
    rest_part = rest_part.replace('발주자', '위탁자')
    rest_part = rest_part.replace('수급자', '수탁자')
    
    # fix the double definitions if any
    rest_part = rest_part.replace('위탁자("甲")', '위탁자("甲")')  # no change
    rest_part = rest_part.replace('위탁자(위탁자)', '위탁자')
    rest_part = rest_part.replace('수탁자(수탁자)', '수탁자')
    
    # [위탁자(위탁자) / 甲] -> [위탁자 / 甲]
    rest_part = rest_part.replace('[위탁자(위탁자) / 甲]', '[위탁자 / 甲]')
    rest_part = rest_part.replace('[수탁자(수탁자) / 乙]', '[수탁자 / 乙]')

    new_text = a1_part + rest_part
    with io.open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_text)
    print(f"Success. Replaced {rest_part.count('위탁자')} times.")
else:
    print("Could not find A-2 section.")
