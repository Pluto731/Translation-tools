from __future__ import annotations

from pathlib import Path

import chardet

from src.file_parser.base_parser import FileParser


class TxtParser(FileParser):

    @property
    def supported_extensions(self) -> set[str]:
        return {".txt"}

    def parse(self, file_path: Path) -> str:
        raw_data = file_path.read_bytes()

        detected = chardet.detect(raw_data)
        encoding = detected.get("encoding", "utf-8")

        if encoding is None:
            encoding = "utf-8"

        try:
            return raw_data.decode(encoding)
        except (UnicodeDecodeError, LookupError):
            return raw_data.decode("utf-8", errors="ignore")
