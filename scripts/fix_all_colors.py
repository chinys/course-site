import os
import re

directories = ['scripts/seeders', 'scripts/templates']
files = []
for d in directories:
    abs_d = os.path.join(os.path.dirname(__file__), '..', d)
    if os.path.exists(abs_d):
        for f in os.listdir(abs_d):
            if f.endswith('.py') and ('seed_law' in f or '_section_' in f):
                files.append(os.path.join(abs_d, f))

def fix_all_tags(m):
    tag_full = m.group(0)
    class_m = re.search(r'class=\"([^\"]*)\"', tag_full)
    if not class_m: return tag_full
    
    cls = class_m.group(1)
    
    # Check if there's any background applied
    bg_m = re.search(r'bg-([a-zA-Z]+)-([1-9]00|50)', cls)
    
    need_replace = False
    
    # 1. Modify dark backgrounds to very light backgrounds
    cls_clean = re.sub(r'bg-(gray|slate|indigo|emerald|blue|red|yellow|purple|teal|rose|orange)-(700|800|900|600|500)', r'bg-\1-50', cls)
    if cls_clean != cls: need_replace = True
    
    # 2. Modify any light text to dark text
    cls_clean2 = re.sub(r'text-(white|gray-50|gray-100|gray-100|gray-200|slate-100|slate-200)', 'text-gray-900', cls_clean)
    if cls_clean2 != cls_clean: need_replace = True
    
    # 3. Modify light colored letters to somewhat dark letters to make them visible on light backgrounds 
    cls_clean3 = re.sub(r'text-(gray|slate|indigo|emerald|blue|red|yellow|purple|teal|rose|orange)-(50|100|200|300|400)', r'text-\1-900', cls_clean2)
    if cls_clean3 != cls_clean2: need_replace = True

    if not need_replace:
        return tag_full
        
    # Clear out duplicate classes
    words = []
    for w in cls_clean3.split():
        if w not in set(words): words.append(w)
    cls_clean_final = ' '.join(words)
    
    # Replace the exact class attribute string
    new_tag = tag_full.replace(class_m.group(0), f'class=\"{cls_clean_final}\"')
    return new_tag

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Process ALL tags, not just table tags
    new_content = re.sub(r'<([a-zA-Z0-9]+)[^>]*>', fix_all_tags, content)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'Done replacing in {os.path.basename(filepath)}')

print('All elements with dark background or light texts have been fixed for legibility!')
