import os
import shutil

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))

STRUCTURE = {
    'templates': ['_section_a.py', '_section_b.py', '_section_c.py', '_section_d.py', '_section_e.py'],
    'seeders': ['seed_law_ultimate_pt1.py', 'seed_law_ultimate_pt2.py', 'seed_law_ultimate_pt3.py', 'seed_law_ultimate_pt4.py', 'seed_fastapi_course.py', 'expand_fastapi_course.py', 'append_basic_lessons.py', '_update_seeds.py'],
    'db_tools': ['check_db.py', 'fix_db.py', 'fix_law_bg.py', 'get_categories.py', 'create_admin.py', 'replace_terms.py', 'replace_terms2.py'],
    'export_tools': ['export_site.py', '_extract_db_content.py', 'generate_docx.py'],
    'media_tools': ['download_image.py', 'move_image.py']
}

for folder, files in STRUCTURE.items():
    folder_path = os.path.join(SCRIPTS_DIR, folder)
    os.makedirs(folder_path, exist_ok=True)
    if folder == 'templates':
        with open(os.path.join(folder_path, '__init__.py'), 'w') as f:
            f.write('')
    
    for file in files:
        src = os.path.join(SCRIPTS_DIR, file)
        dst = os.path.join(folder_path, file)
        if os.path.exists(src):
            shutil.move(src, dst)
            print(f'Moved {file} to {folder}')

print('Done moving files.')
