from __future__ import annotations

from typing import Optional

from src.translation.base_engine import TranslationEngine
from src.translation.models import TranslationRequest, TranslationResult


class EngineManager:

    def __init__(self) -> None:
        self._engines: dict[str, TranslationEngine] = {}
        self._current_engine_name: Optional[str] = None

    def register_engine(self, engine: TranslationEngine) -> None:
        self._engines[engine.name] = engine
        if self._current_engine_name is None:
            self._current_engine_name = engine.name

    def set_current_engine(self, name: str) -> None:
        if name not in self._engines:
            raise ValueError(f"引擎 '{name}' 未注册")
        self._current_engine_name = name

    @property
    def current_engine(self) -> TranslationEngine:
        if self._current_engine_name is None:
            raise RuntimeError("没有可用的翻译引擎")
        return self._engines[self._current_engine_name]

    @property
    def current_engine_name(self) -> Optional[str]:
        return self._current_engine_name

    @property
    def available_engines(self) -> list[str]:
        return list(self._engines.keys())

    def translate(self, request: TranslationRequest) -> TranslationResult:
        return self.current_engine.translate(request)

    def lookup_word(self, word: str, from_lang: str, to_lang: str) -> TranslationResult:
        return self.current_engine.lookup_word(word, from_lang, to_lang)

    def close_all(self) -> None:
        for engine in self._engines.values():
            if hasattr(engine, "close"):
                engine.close()
