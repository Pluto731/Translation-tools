from __future__ import annotations

from pathlib import Path

import pytest

from src.file_parser.parser_factory import ParserFactory
from src.file_parser.txt_parser import TxtParser


def test_txt_parser_utf8(tmp_path: Path):
    txt_file = tmp_path / "test.txt"
    txt_file.write_text("Hello world\n你好世界", encoding="utf-8")

    parser = TxtParser()
    content = parser.parse(txt_file)

    assert "Hello world" in content
    assert "你好世界" in content


def test_txt_parser_gbk(tmp_path: Path):
    txt_file = tmp_path / "test_gbk.txt"
    txt_file.write_bytes("你好世界".encode("gbk"))

    parser = TxtParser()
    content = parser.parse(txt_file)

    assert "你好世界" in content


def test_parser_factory_get_txt_parser(tmp_path: Path):
    txt_file = tmp_path / "test.txt"

    parser = ParserFactory.get_parser(txt_file)

    assert parser is not None
    assert isinstance(parser, TxtParser)


def test_parser_factory_unsupported_extension(tmp_path: Path):
    file = tmp_path / "test.xyz"

    parser = ParserFactory.get_parser(file)

    assert parser is None


def test_parser_factory_is_supported(tmp_path: Path):
    txt_file = tmp_path / "test.txt"
    docx_file = tmp_path / "test.docx"
    pdf_file = tmp_path / "test.pdf"
    xyz_file = tmp_path / "test.xyz"

    assert ParserFactory.is_supported(txt_file) is True
    assert ParserFactory.is_supported(docx_file) is True
    assert ParserFactory.is_supported(pdf_file) is True
    assert ParserFactory.is_supported(xyz_file) is False
