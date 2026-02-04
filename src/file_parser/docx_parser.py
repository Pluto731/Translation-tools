from __future__ import annotations

from pathlib import Path

from docx import Document

from src.file_parser.base_parser import FileParser


class DocxParser(FileParser):

    @property
    def supported_extensions(self) -> set[str]:
        return {".docx"}

    def parse(self, file_path: Path) -> str:
        doc = Document(file_path)

        paragraphs = []
        for para in doc.paragraphs:
            text = para.text.strip()
            if text:
                paragraphs.append(text)

        return "\n".join(paragraphs)
