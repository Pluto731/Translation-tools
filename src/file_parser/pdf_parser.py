from __future__ import annotations

from pathlib import Path

import fitz

from src.file_parser.base_parser import FileParser


class PdfParser(FileParser):

    @property
    def supported_extensions(self) -> set[str]:
        return {".pdf"}

    def parse(self, file_path: Path) -> str:
        doc = fitz.open(file_path)

        text_parts = []
        for page in doc:
            text = page.get_text()
            if text.strip():
                text_parts.append(text)

        doc.close()

        return "\n".join(text_parts)
