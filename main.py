from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from core.database import create_db_and_tables
from routers import auth, admin, public
from routers.auth import NotAuthenticatedException

app = FastAPI(title="Course Site FastAPI")

@app.exception_handler(NotAuthenticatedException)
async def not_authenticated_exception_handler(request: Request, exc: NotAuthenticatedException):
    return RedirectResponse(url="/admin/login", status_code=303)

app.include_router(public.router)
app.include_router(auth.router)
app.include_router(admin.router)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/fix_db")
def fix_db():
    from sqlmodel import Session
    from core.database import engine
    from sqlalchemy import text
    try:
        with Session(engine) as session:
            # Delete duplicates keeping the minimum ID
            session.exec(text('''
                DELETE FROM lesson 
                WHERE id NOT IN (
                    SELECT MIN(id) 
                    FROM lesson 
                    GROUP BY course_id, title
                )
            '''))
            session.commit()
        return {"status": "success", "message": "Duplicate lessons purged successfully."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

