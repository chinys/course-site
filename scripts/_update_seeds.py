import os
import re

db_file = os.path.join(os.path.dirname(__file__), '_db_lesson_55.txt')

with open(db_file, 'r', encoding='utf-8') as f:
    html = f.read()

# Fix the href links which might be relative due to rich text editor
html = re.sub(r'href="(\.\./)+static/downloads/', r'href="/static/downloads/', html)

# The content has sections.
# Intro is everything before <!-- ══ A.
parts = html.split('<!-- ══ A.')
intro = parts[0].strip()

# Now split the rest.
rest = '<!-- ══ A.' + parts[1]

a_split = rest.split('<!-- ══ B.')
section_a = a_split[0].strip()

b_split = ('<!-- ══ B.' + a_split[1]).split('<!-- ══ C.')
section_b = b_split[0].strip()

c_split = ('<!-- ══ C.' + b_split[1]).split('<!-- ══ D.')
section_c = c_split[0].strip()

d_split = ('<!-- ══ D.' + c_split[1]).split('<!-- ══ E.')
section_d = d_split[0].strip()

section_e = ('<!-- ══ E.' + d_split[1]).strip()

# wait, we need to remove the closing </div> of <div class="space-y-12">
if section_e.endswith('</div>\n</div>'):
    section_e = section_e[:-12].strip()
elif section_e.endswith('</div></div>'):
    section_e = section_e[:-12].strip()

if section_e.endswith('</div>'):
    # try one more
    pass

# write function for section
def write_section(filename, content, func_name):
    # escape single quotes just in case, or use triple quotes safely
    content_escaped = content.replace("'''", "\\'\\'\\'")
    code = f"# -*- coding: utf-8 -*-\ndef {func_name}():\n    return '''\n{content_escaped}'''\n"
    path = os.path.join(os.path.dirname(__file__), filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(code)
    print(f"Wrote {filename}")

write_section('_section_a.py', section_a, 'section_a')
write_section('_section_b.py', section_b, 'section_b')
write_section('_section_c.py', section_c, 'section_c')
write_section('_section_d.py', section_d, 'section_d')
write_section('_section_e.py', section_e, 'section_e')

# update seed_law_ultimate_pt4.py intro
intro_escaped = intro.replace("'''", "\\'\\'\\'")
seed_code = f"""import sqlite3
import os

def seed_law_course_ultimate_pt4():
    db_path = os.path.join(os.path.dirname(__file__), '..', 'database.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM course WHERE title LIKE '%건설법규%'")
    row = cursor.fetchone()
    if not row:
        print("Error: [건설법규] course not found.")
        return
    course_id = row[0]

    html = _build_html()
    title = '14. [실무 핵심 양식] 강구조물 불법 재하도급 방지용 계약서 모음'
    
    cursor.execute("SELECT id FROM lesson WHERE course_id = ? AND title LIKE '%계약서 모음%'", (course_id,))
    lesson_row = cursor.fetchone()
    
    if lesson_row:
        cursor.execute("UPDATE lesson SET content = ? WHERE id = ?", (html, lesson_row[0]))
        print("[법무 심화 14강] 기존 내용 업데이트 완료")
    else:
        cursor.execute("INSERT INTO lesson (title, content, course_id, \\"order\\") VALUES (?, ?, ?, ?)",
                       (title, html, course_id, 14))
        print("[법무 심화 14강] 강구조물 실무 특화 계약서 양식 추가 완료")
        
    conn.commit()
    conn.close()


def _build_html():
    from _section_a import section_a
    from _section_b import section_b
    from _section_c import section_c
    from _section_d import section_d
    from _section_e import section_e
    parts = [_intro(), section_a(), section_b(), section_c(), section_d(), section_e(), '</div>']
    return '\\n'.join(parts)


def _intro():
    return '''{intro_escaped}
<div class="space-y-12">'''


if __name__ == "__main__":
    seed_law_course_ultimate_pt4()
"""

with open(os.path.join(os.path.dirname(__file__), 'seed_law_ultimate_pt4.py'), 'w', encoding='utf-8') as f:
    f.write(seed_code)
print("Wrote seed_law_ultimate_pt4.py")
