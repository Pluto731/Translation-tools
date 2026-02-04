from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class TranslationRequest(BaseModel, frozen=True):
    text: str
    from_lang: str = "auto"
    to_lang: str = "zh"


class WordExample(BaseModel, frozen=True):
    source: str = ""
    target: str = ""


class WordDetail(BaseModel, frozen=True):
    word: str = ""
    phonetic: str = ""
    uk_phonetic: str = ""
    us_phonetic: str = ""
    explains: tuple[str, ...] = ()
    examples: tuple[WordExample, ...] = ()


class TranslationResult(BaseModel, frozen=True):
    source_text: str
    translated_text: str
    from_lang: str
    to_lang: str
    engine_name: str
    is_word: bool = False
    word_detail: Optional[WordDetail] = None
    error: Optional[str] = None

    @property
    def success(self) -> bool:
        return self.error is None
