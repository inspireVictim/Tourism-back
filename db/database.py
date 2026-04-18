import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from Core.env_loader import load_env_file

load_env_file()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./sqlite3.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

