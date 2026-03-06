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

def fix_tag(m):
    tag_full = m.group(0)
    class_m = re.search(r'class=\"([^\"]*)\"', tag_full)
    if not class_m: return tag_full
    
    cls = class_m.group(1)
    # Remove existing text color
    cls_clean = re.sub(r'text-(white|black|[a-zA-Z]+-[1-9]00|gray-50)', '', cls)
    cls_clean = ' '.join(cls_clean.split())
    
    bg_m = re.search(r'bg-([a-zA-Z]+)-([1-9]00|50)', cls_clean)
    if bg_m:
        weight = int(bg_m.group(2))
        
        # Determine appropriate text color for the background
        if weight >= 600:
            cls_clean += ' text-white'
        else:
            cls_clean += ' text-gray-900'
            
        return re.sub(r'class=\"[^\"]*\"', f'class=\"{cls_clean}\"', tag_full)
        
    return tag_full

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Process only relevant tags
    new_content = re.sub(r'<(th|tr|td|thead)[^>]*>', fix_tag, content)
    
    if content != new_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {os.path.basename(filepath)}")

print('All tables have been re-processed to automatically enforce explicit high-contrast text color!')
