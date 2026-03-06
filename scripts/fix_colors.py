import os
import re

seeders_dir = os.path.join(os.path.dirname(__file__), 'seeders')
files_to_fix = [
    'seed_law_ultimate_pt1.py',
    'seed_law_ultimate_pt2.py',
    'seed_law_ultimate_pt3.py',
    'seed_law_ultimate_pt4.py'
]

for filename in files_to_fix:
    filepath = os.path.join(seeders_dir, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace dark backgrounds causing readability issues in TH/TD
        # Replace bg-gray-800/900 without text-white to have text-white
        content = re.sub(r'class="([^"]*)bg-gray-[89]00([^"]*)"', lambda m: f'class="{m.group(1)}bg-gray-100 text-gray-900 font-bold{m.group(2)}"', content)
        content = re.sub(r'class="([^"]*)bg-indigo-[89]00([^"]*)"', lambda m: f'class="{m.group(1)}bg-indigo-100 text-indigo-900 font-bold{m.group(2)}"', content)
        
        # Replace mid-gray backgrounds
        content = re.sub(r'bg-gray-[234]00', 'bg-gray-50', content)
        
        # Remove any residual text-white if we changed background to light
        content = re.sub(r'class="([^"]*)bg-gray-[15]0([^"]*)text-white([^"]*)"', lambda m: f'class="{m.group(1)}bg-gray-100 text-gray-900{m.group(2)}{m.group(3)}"', content)
        content = re.sub(r'class="([^"]*)bg-indigo-100([^"]*)text-white([^"]*)"', lambda m: f'class="{m.group(1)}bg-indigo-100 text-indigo-900{m.group(2)}{m.group(3)}"', content)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

print("색상 대비(가독성) 문제 수정 완료!")
