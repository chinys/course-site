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

