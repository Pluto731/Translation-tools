from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path

import pytest

from src.history.export_service import ExportService
from src.history.models import TranslationRecord


@pytest.fixture
def sample_records():
    return [
        TranslationRecord(
            id=1,
            source_text="hello",
            translated_text="你好",
            from_lang="en",
            to_lang="zh",
            engine_name="baidu",
            is_word=True,
            created_at=datetime(2024, 1, 1, 12, 0, 0),
        ),
        TranslationRecord(
            id=2,
            source_text="world",
            translated_text="世界",
            from_lang="en",
            to_lang="zh",
            engine_name="youdao",
            is_word=False,
            created_at=datetime(2024, 1, 2, 13, 0, 0),
        ),
    ]


def test_export_to_csv(tmp_path: Path, sample_records):
    output_path = tmp_path / "export.csv"

    ExportService.export_to_csv(sample_records, output_path)

    assert output_path.exists()

    with open(output_path, "r", encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)

    assert len(rows) == 2
    assert rows[0]["ID"] == "1"
    assert rows[0]["原文"] == "hello"
    assert rows[0]["译文"] == "你好"
    assert rows[0]["源语言"] == "en"
    assert rows[0]["目标语言"] == "zh"
    assert rows[0]["引擎"] == "baidu"
    assert rows[0]["是否单词"] == "是"
    assert rows[0]["创建时间"] == "2024-01-01 12:00:00"


def test_export_to_txt(tmp_path: Path, sample_records):
    output_path = tmp_path / "export.txt"

    ExportService.export_to_txt(sample_records, output_path)

    assert output_path.exists()

    content = output_path.read_text(encoding="utf-8")

    assert "===== 记录 1 =====" in content
    assert "ID: 1" in content
    assert "原文: hello" in content
    assert "译文: 你好" in content
    assert "语言: en -> zh" in content
    assert "引擎: baidu" in content
    assert "是否单词: 是" in content

    assert "===== 记录 2 =====" in content
    assert "ID: 2" in content
    assert "原文: world" in content
    assert "译文: 世界" in content
    assert "引擎: youdao" in content
    assert "是否单词: 否" in content


def test_export_empty_list(tmp_path: Path):
    output_path = tmp_path / "empty.csv"

    ExportService.export_to_csv([], output_path)

    assert output_path.exists()

    with open(output_path, "r", encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)

    assert len(rows) == 0
