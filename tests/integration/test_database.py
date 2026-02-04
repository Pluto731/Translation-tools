from __future__ import annotations

from pathlib import Path

import pytest

from src.database.connection import init_database
from src.database.migrations import create_tables
from src.history.repository import TranslationRepository
from src.translation.models import TranslationResult


@pytest.fixture
def db_setup(tmp_path: Path):
    db_path = tmp_path / "test_integration.db"
    init_database(db_path)
    create_tables()
    yield
    if db_path.exists():
        db_path.unlink()


def test_full_translation_workflow(db_setup):
    repo = TranslationRepository()

    result1 = TranslationResult(
        source_text="hello",
        translated_text="你好",
        from_lang="en",
        to_lang="zh",
        engine_name="baidu",
        is_word=True,
    )

    record1 = repo.create_from_result(result1)
    assert record1.id is not None

    result2 = TranslationResult(
        source_text="world",
        translated_text="世界",
        from_lang="en",
        to_lang="zh",
        engine_name="youdao",
    )

    record2 = repo.create_from_result(result2)
    assert record2.id is not None

    records, total = repo.find_all(page=1, page_size=10)
    assert total == 2
    assert len(records) == 2

    found = repo.find_by_id(record1.id)
    assert found is not None
    assert found.source_text == "hello"

    deleted = repo.delete_by_id(record2.id)
    assert deleted is True

    assert repo.count() == 1

    repo.delete_all()
    assert repo.count() == 0
