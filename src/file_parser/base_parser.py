from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path


class FileParser(ABC):

    @abstractmethod
    def parse(self, file_path: Path) -> str:
        ...

    @property
    @abstractmethod
    def supported_extensions(self) -> set[str]:
        ...
