import os
import sys
import shutil
from bs4 import BeautifulSoup

# Add project root to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(project_root)

from fastapi.testclient import TestClient
from main import app
from core.database import engine
from sqlmodel import Session, select
from models import Course, Lesson

BUILD_DIR = os.path.join(project_root, "build")
PREFIX = "/course-site/build"

def rewrite_html(html_bytes):
    soup = BeautifulSoup(html_bytes, "html.parser")
    
    # Rewrite hrefs
    for a in soup.find_all("a", href=True):
        href = a['href']
        if href == "/":
            a['href'] = f"{PREFIX}/index.html"
        elif href.startswith("/static/"):
            a['href'] = f"{PREFIX}{href}"
        elif href.startswith("/courses/"):
            parts = href.split("/")
            if len(parts) == 3: # /courses/1
                a['href'] = f"{PREFIX}/courses/{parts[2]}.html"
            elif len(parts) == 5 and parts[3] == "lessons": # /courses/1/lessons/2
                a['href'] = f"{PREFIX}/courses/{parts[2]}/lessons/{parts[4]}.html"
            else:
                a['href'] = f"{PREFIX}{href}"
                
    # Rewrite srcs
    for tag in soup.find_all(["img", "script"], src=True):
        src = tag['src']
        if src.startswith("/static/"):
            tag['src'] = f"{PREFIX}{src}"
            
    # Rewrite link hrefs (stylesheets, etc.)
    for tag in soup.find_all("link", href=True):
        href = tag['href']
        if href.startswith("/static/"):
            tag['href'] = f"{PREFIX}{href}"
            
    return str(soup)

def export_site():
    if os.path.exists(BUILD_DIR):
        shutil.rmtree(BUILD_DIR)
    os.makedirs(BUILD_DIR)
    
    # Create .nojekyll for Github Pages
    with open(os.path.join(BUILD_DIR, ".nojekyll"), "w") as f:
        f.write("")
        
    client = TestClient(app)
    
    print("Exporting index.html...")
    # 1. Export index
    r = client.get("/")
    if r.status_code == 200:
        html = rewrite_html(r.content)
        with open(os.path.join(BUILD_DIR, "index.html"), "w", encoding="utf-8") as f:
            f.write(html)
            
    print("Exporting static files...")
    # 2. Export static files
    static_src = os.path.join(project_root, "static")
    static_dst = os.path.join(BUILD_DIR, "static")
    if os.path.exists(static_src):
        if os.path.exists(static_dst):
            shutil.rmtree(static_dst)
        shutil.copytree(static_src, static_dst)
        
    print("Exporting courses and lessons...")
    with Session(engine) as session:
        courses = session.exec(select(Course)).all()
        for course in courses:
            courses_dir = os.path.join(BUILD_DIR, "courses")
            os.makedirs(courses_dir, exist_ok=True)
            
            # Fetch course page
            r = client.get(f"/courses/{course.id}")
            if r.status_code == 200:
                html = rewrite_html(r.content)
                with open(os.path.join(courses_dir, f"{course.id}.html"), "w", encoding="utf-8") as f:
                    f.write(html)
                    
            # Fetch lessons
            lessons = session.exec(select(Lesson).where(Lesson.course_id == course.id)).all()
            for lesson in lessons:
                lessons_dir = os.path.join(courses_dir, str(course.id), "lessons")
                os.makedirs(lessons_dir, exist_ok=True)
                
                r = client.get(f"/courses/{course.id}/lessons/{lesson.id}")
                if r.status_code == 200:
                    html = rewrite_html(r.content)
                    with open(os.path.join(lessons_dir, f"{lesson.id}.html"), "w", encoding="utf-8") as f:
                        f.write(html)
                        
    print("Static site exported successfully. Ready for GitHub Pages!")

if __name__ == "__main__":
    export_site()
