from __future__ import annotations

from abc import ABC, abstractmethod

from src.translation.models import TranslationRequest, TranslationResult


class TranslationEngine(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @abstractmethod
    def translate(self, request: TranslationRequest) -> TranslationResult:
        ...

    @abstractmethod
    def lookup_word(self, word: str, from_lang: str, to_lang: str) -> TranslationResult:
        ...
