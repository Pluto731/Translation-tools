from __future__ import annotations

from pathlib import Path

from PyQt5.QtCore import QObject, pyqtSignal

from src.file_parser.parser_factory import ParserFactory
from src.translation.engine_manager import EngineManager
from src.translation.models import TranslationRequest
from src.utils.text_utils import split_text_chunks


class FileTranslationService(QObject):
    progress_updated = pyqtSignal(int, int)
    translation_completed = pyqtSignal(str)
    error_occurred = pyqtSignal(str)

    def __init__(self, engine_manager: EngineManager) -> None:
        super().__init__()
        self._engine_manager = engine_manager

    def translate_file(
        self,
        file_path: Path,
        from_lang: str,
        to_lang: str,
    ) -> None:
        try:
            parser = ParserFactory.get_parser(file_path)
            if parser is None:
                self.error_occurred.emit(f"不支持的文件格式: {file_path.suffix}")
                return

            text = parser.parse(file_path)

            if not text.strip():
                self.error_occurred.emit("文件内容为空")
                return

            chunks = split_text_chunks(text)
            total_chunks = len(chunks)

            translated_chunks = []

            for i, chunk in enumerate(chunks):
                request = TranslationRequest(
                    text=chunk,
                    from_lang=from_lang,
                    to_lang=to_lang,
                )

                result = self._engine_manager.translate(request)

                if result.success:
                    translated_chunks.append(result.translated_text)
                else:
                    translated_chunks.append(f"[翻译失败: {result.error}]")

                self.progress_updated.emit(i + 1, total_chunks)

            translated_text = "\n\n".join(translated_chunks)

            self.translation_completed.emit(translated_text)

        except Exception as e:
            self.error_occurred.emit(f"文件翻译出错: {str(e)}")
