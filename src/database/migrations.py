from __future__ import annotations

from src.database.connection import get_engine
from src.history.models import Base


def create_tables() -> None:
    engine = get_engine()
    Base.metadata.create_all(engine)


def drop_tables() -> None:
    engine = get_engine()
    Base.metadata.drop_all(engine)
