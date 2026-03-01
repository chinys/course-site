import asyncio
from sqlmodel import Session, select
from database import engine, create_db_and_tables
from models import User
from routers.auth import get_password_hash

def create_initial_admin():
    create_db_and_tables()
    with Session(engine) as session:
        admin_email = "admin@example.com"
        admin = session.exec(select(User).where(User.email == admin_email)).first()
        if not admin:
            print(f"Creating default admin user: {admin_email} / password123")
            hashed_pw = get_password_hash("password123")
            new_admin = User(email=admin_email, hashed_password=hashed_pw, role="ADMIN")
            session.add(new_admin)
            session.commit()
            print("Admin created successfully.")
        else:
            print(f"Admin {admin_email} already exists.")

if __name__ == "__main__":
    create_initial_admin()
