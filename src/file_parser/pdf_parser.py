from __future__ import annotations

from pathlib import Path

import fitz

from src.file_parser.base_parser import FileParser


class PdfParser(FileParser):

    @property
    def supported_extensions(self) -> set[str]:
        return {".pdf"}

    def parse(self, file_path: Path) -> str:
        try:
            doc = fitz.open(file_path)
        except Exception as exc:
            raise ValueError(f"无法打开 PDF 文件: {exc}") from exc

        try:
            text_parts = []
            for page in doc:
                text = page.get_text()
                if text.strip():
                    text_parts.append(text)
            return "\n".join(text_parts)
        except Exception as exc:
            raise ValueError(f"PDF 解析失败: {exc}") from exc
        finally:
            doc.close()
