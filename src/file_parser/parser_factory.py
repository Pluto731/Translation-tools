from __future__ import annotations

from pathlib import Path

from src.file_parser.base_parser import FileParser
from src.file_parser.docx_parser import DocxParser
from src.file_parser.pdf_parser import PdfParser
from src.file_parser.txt_parser import TxtParser


class ParserFactory:

    _parsers: list[FileParser] = [
        TxtParser(),
        DocxParser(),
        PdfParser(),
    ]

    @classmethod
    def get_parser(cls, file_path: Path) -> FileParser | None:
        extension = file_path.suffix.lower()

        for parser in cls._parsers:
            if extension in parser.supported_extensions:
                return parser

        return None

    @classmethod
    def is_supported(cls, file_path: Path) -> bool:
        return cls.get_parser(file_path) is not None
