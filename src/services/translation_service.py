from __future__ import annotations

from PyQt5.QtCore import QObject, pyqtSignal

from src.history.repository import TranslationRepository
from src.translation.engine_manager import EngineManager
from src.translation.models import TranslationRequest, TranslationResult


class TranslationService(QObject):
    translation_completed = pyqtSignal(TranslationResult)

    def __init__(
        self,
        engine_manager: EngineManager,
        repository: TranslationRepository,
    ) -> None:
        super().__init__()
        self._engine_manager = engine_manager
        self._repository = repository

    def translate_text(self, text: str, from_lang: str = "auto", to_lang: str = "zh") -> None:
        request = TranslationRequest(text=text, from_lang=from_lang, to_lang=to_lang)

        result = self._engine_manager.translate(request)

        if result.success and result.is_word:
            word_result = self._engine_manager.lookup_word(text, from_lang, to_lang)
            if word_result.success and word_result.word_detail:
                result = word_result

        if result.success:
            self._repository.create_from_result(result)

        self.translation_completed.emit(result)
