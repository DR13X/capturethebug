"""SQLAlchemy engine and session helpers."""

from __future__ import annotations

import os
from contextlib import contextmanager
from pathlib import Path
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from .schema import Base

DEFAULT_DB = Path.home() / ".capturethebug" / "ctb.db"
_engine = None
_SessionLocal = None


def get_db_path() -> Path:
    path = os.environ.get("CTB_DB_PATH")
    if path:
        return Path(path)
    DEFAULT_DB.parent.mkdir(parents=True, exist_ok=True)
    return DEFAULT_DB


def get_engine():
    global _engine, _SessionLocal
    if _engine is None:
        db_url = f"sqlite:///{get_db_path()}"
        _engine = create_engine(
            db_url,
            connect_args={"check_same_thread": False},
            echo=False,
        )
        _SessionLocal = sessionmaker(bind=_engine, autoflush=False, autocommit=False)
    return _engine


def init_db() -> None:
    """Create all tables."""
    engine = get_engine()
    Base.metadata.create_all(bind=engine)


@contextmanager
def get_session() -> Generator[Session, None, None]:
    engine = get_engine()
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
