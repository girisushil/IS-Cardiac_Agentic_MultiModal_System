
import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# Default to a local SQLite DB if DATABASE_URL is not set.
# In Docker/cloud dev, DATABASE_URL will point to PostgreSQL.
DEFAULT_DB_URL = "sqlite:///./local.db"
DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_DB_URL)

engine = create_engine(
    DATABASE_URL,
    future=True,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    future=True,
)


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency that yields a SQLAlchemy Session and closes it afterwards.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

