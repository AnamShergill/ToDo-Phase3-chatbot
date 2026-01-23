from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session
import os
from dotenv import load_dotenv

load_dotenv()

# Use SQLite for local development to avoid PostgreSQL installation issues
# Force SQLite for local development instead of remote PostgreSQL
DATABASE_URL = "sqlite:///./todo_app.db"  # Changed to use local SQLite file

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()