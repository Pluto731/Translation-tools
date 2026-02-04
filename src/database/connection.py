from __future__ import annotations

from pathlib import Path
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

_engine = None
_session_factory: Optional[sessionmaker] = None


def init_database(db_path: Path) -> None:
    global _engine, _session_factory

    db_path.parent.mkdir(parents=True, exist_ok=True)

    _engine = create_engine(
        f"sqlite:///{db_path}",
        connect_args={"check_same_thread": False},
        echo=False,
    )

    _session_factory = sessionmaker(bind=_engine, expire_on_commit=False)


def get_session() -> Session:
    if _session_factory is None:
        raise RuntimeError("Database not initialized. Call init_database() first.")
    return _session_factory()


def get_engine():
    if _engine is None:
        raise RuntimeError("Database not initialized. Call init_database() first.")
    return _engine
