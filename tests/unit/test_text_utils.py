from __future__ import annotations

import pytest

from src.utils.text_utils import is_single_word, split_text_chunks


@pytest.mark.parametrize(
    "text,expected",
    [
        ("hello", True),
        ("world", True),
        ("apple-pie", True),
        ("你好", True),
        ("中国", True),
        ("测试", True),
        ("hello world", False),
        ("你好世界", False),
        ("", False),
        ("   ", False),
        ("hello123", False),
        ("中国人民", False),
        ("测试一下看看", False),
        ("test-case-multiple", False),
    ],
)
def test_is_single_word(text: str, expected: bool):
    assert is_single_word(text) == expected


def test_split_text_chunks_short_text():
    text = "This is a short text."
    chunks = split_text_chunks(text, max_size=100)

    assert len(chunks) == 1
    assert chunks[0] == text


def test_split_text_chunks_by_paragraphs():
    text = "Line 1\nLine 2\nLine 3"
    chunks = split_text_chunks(text, max_size=10)

    assert len(chunks) == 3
    assert chunks[0] == "Line 1"
    assert chunks[1] == "Line 2"
    assert chunks[2] == "Line 3"


def test_split_text_chunks_long_paragraph():
    text = "a" * 150
    chunks = split_text_chunks(text, max_size=50)

    assert len(chunks) == 3
    assert all(len(chunk) <= 50 for chunk in chunks)


def test_split_text_chunks_mixed():
    text = "Short\n" + ("a" * 80) + "\nAnother short"
    chunks = split_text_chunks(text, max_size=50)

    assert len(chunks) == 3
    assert chunks[0] == "Short"
    assert chunks[2] == "Another short"


def test_split_text_chunks_empty():
    text = ""
    chunks = split_text_chunks(text, max_size=100)

    assert len(chunks) == 1
    assert chunks[0] == ""
