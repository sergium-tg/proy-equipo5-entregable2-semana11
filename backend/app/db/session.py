
# backend/app/db/session.py
from dotenv import load_dotenv
from sqlmodel import create_engine, Session
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

# Para sqlite local: desactivar check_same_thread
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, echo=False, connect_args=connect_args)

def get_engine():
    return engine

def get_session():
    """Generator simple para dependencias (si quieres usar Depends)."""
    with Session(engine) as session:
        yield session
