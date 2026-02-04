from __future__ import annotations

from pathlib import Path

import pytest

from src.database.connection import init_database
from src.database.migrations import create_tables, drop_tables
from src.history.repository import TranslationRepository
from src.translation.models import TranslationResult, WordDetail


@pytest.fixture
def test_db(tmp_path: Path):
    db_path = tmp_path / "test.db"
    init_database(db_path)
    create_tables()
    yield
    drop_tables()


def test_create_from_result(test_db):
    repo = TranslationRepository()

    result = TranslationResult(
        source_text="hello",
        translated_text="你好",
        from_lang="en",
        to_lang="zh",
        engine_name="baidu",
        is_word=True,
    )

    record = repo.create_from_result(result)

    assert record.id is not None
    assert record.source_text == "hello"
    assert record.translated_text == "你好"
    assert record.from_lang == "en"
    assert record.to_lang == "zh"
    assert record.engine_name == "baidu"
    assert record.is_word is True


def test_create_with_word_detail(test_db):
    repo = TranslationRepository()

    detail = WordDetail(
        word="apple",
        phonetic="ˈæpl",
        explains=("n. 苹果", "n. 苹果树"),
    )

    result = TranslationResult(
        source_text="apple",
        translated_text="苹果",
        from_lang="en",
        to_lang="zh",
        engine_name="youdao",
        is_word=True,
        word_detail=detail,
    )

    record = repo.create_from_result(result)

    assert record.word_detail_json is not None
    assert "apple" in record.word_detail_json


def test_find_by_id(test_db):
    repo = TranslationRepository()

    result = TranslationResult(
        source_text="test",
        translated_text="测试",
        from_lang="en",
        to_lang="zh",
        engine_name="baidu",
    )

    created = repo.create_from_result(result)
    found = repo.find_by_id(created.id)

    assert found is not None
    assert found.id == created.id
    assert found.source_text == "test"


def test_find_by_id_not_found(test_db):
    repo = TranslationRepository()
    found = repo.find_by_id(99999)

    assert found is None


def test_find_all_pagination(test_db):
    repo = TranslationRepository()

    for i in range(25):
        result = TranslationResult(
            source_text=f"text{i}",
            translated_text=f"文本{i}",
            from_lang="en",
            to_lang="zh",
            engine_name="baidu",
        )
        repo.create_from_result(result)

    records, total = repo.find_all(page=1, page_size=10)

    assert total == 25
    assert len(records) == 10

    records, total = repo.find_all(page=3, page_size=10)

    assert total == 25
    assert len(records) == 5


def test_find_all_search(test_db):
    repo = TranslationRepository()

    repo.create_from_result(
        TranslationResult(
            source_text="hello world",
            translated_text="你好世界",
            from_lang="en",
            to_lang="zh",
            engine_name="baidu",
        )
    )

    repo.create_from_result(
        TranslationResult(
            source_text="goodbye",
            translated_text="再见",
            from_lang="en",
            to_lang="zh",
            engine_name="baidu",
        )
    )

    records, total = repo.find_all(search_query="hello")

    assert total == 1
    assert records[0].source_text == "hello world"

    records, total = repo.find_all(search_query="再见")

    assert total == 1
    assert records[0].translated_text == "再见"


def test_count(test_db):
    repo = TranslationRepository()

    assert repo.count() == 0

    for i in range(5):
        result = TranslationResult(
            source_text=f"text{i}",
            translated_text=f"文本{i}",
            from_lang="en",
            to_lang="zh",
            engine_name="baidu",
        )
        repo.create_from_result(result)

    assert repo.count() == 5


def test_delete_by_id(test_db):
    repo = TranslationRepository()

    result = TranslationResult(
        source_text="delete me",
        translated_text="删除我",
        from_lang="en",
        to_lang="zh",
        engine_name="baidu",
    )

    record = repo.create_from_result(result)

    assert repo.count() == 1

    deleted = repo.delete_by_id(record.id)

    assert deleted is True
    assert repo.count() == 0


def test_delete_by_id_not_found(test_db):
    repo = TranslationRepository()

    deleted = repo.delete_by_id(99999)

    assert deleted is False


def test_delete_all(test_db):
    repo = TranslationRepository()

    for i in range(10):
        result = TranslationResult(
            source_text=f"text{i}",
            translated_text=f"文本{i}",
            from_lang="en",
            to_lang="zh",
            engine_name="baidu",
        )
        repo.create_from_result(result)

    assert repo.count() == 10

    deleted_count = repo.delete_all()

    assert deleted_count == 10
    assert repo.count() == 0
