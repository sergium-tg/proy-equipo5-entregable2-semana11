
# backend/app/db/session.py
from dotenv import load_dotenv
from sqlmodel import create_engine, Session
import os
from typing import Generator

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

# Para sqlite local: desactivar check_same_thread
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

_engine = create_engine(DATABASE_URL, echo=False, connect_args=connect_args)

def get_engine():
    return _engine

def get_session() -> Generator[Session, None, None]:
    with Session(_engine) as session:
        yield session
        