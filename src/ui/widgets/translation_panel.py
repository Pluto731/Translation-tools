from __future__ import annotations

from PyQt5.QtCore import QThreadPool, pyqtSignal
from PyQt5.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from src.translation.models import TranslationRequest, TranslationResult
from src.ui.widgets.language_selector import LanguageSelector
from src.utils.async_worker import AsyncWorker


class TranslationPanel(QWidget):
    translation_requested = pyqtSignal(TranslationRequest)
    translation_completed = pyqtSignal(TranslationResult)

    def __init__(self, translate_fn, parent=None) -> None:
        super().__init__(parent)

        self._translate_fn = translate_fn
        self._thread_pool = QThreadPool.globalInstance()

        self._init_ui()

    def _init_ui(self) -> None:
        layout = QVBoxLayout(self)

        lang_layout = QHBoxLayout()
        lang_layout.addWidget(QLabel("源语言:"))
        self._from_lang_selector = LanguageSelector()
        lang_layout.addWidget(self._from_lang_selector)

        lang_layout.addWidget(QLabel("目标语言:"))
        self._to_lang_selector = LanguageSelector()
        self._to_lang_selector.set_selected_code("zh")
        lang_layout.addWidget(self._to_lang_selector)

        lang_layout.addStretch()
        layout.addLayout(lang_layout)

        layout.addWidget(QLabel("输入文本:"))
        self._input_text = QTextEdit()
        self._input_text.setPlaceholderText("请输入要翻译的文本...")
        self._input_text.setMaximumHeight(150)
        layout.addWidget(self._input_text)

        self._translate_btn = QPushButton("翻译")
        self._translate_btn.clicked.connect(self._on_translate_clicked)
        layout.addWidget(self._translate_btn)

        layout.addWidget(QLabel("翻译结果:"))
        self._output_text = QTextEdit()
        self._output_text.setReadOnly(True)
        self._output_text.setPlaceholderText("翻译结果将显示在这里...")
        layout.addWidget(self._output_text)

        self.setLayout(layout)

    def _on_translate_clicked(self) -> None:
        text = self._input_text.toPlainText().strip()

        if not text:
            QMessageBox.warning(self, "提示", "请输入要翻译的文本")
            return

        from_lang = self._from_lang_selector.get_selected_code()
        to_lang = self._to_lang_selector.get_selected_code()

        request = TranslationRequest(text=text, from_lang=from_lang, to_lang=to_lang)

        self._translate_btn.setEnabled(False)
        self._translate_btn.setText("翻译中...")

        self.translation_requested.emit(request)

        worker = AsyncWorker(self._translate_fn, request)
        worker.signals.finished.connect(self._on_translation_finished)
        worker.signals.error.connect(self._on_translation_error)
        self._thread_pool.start(worker)

    def _on_translation_finished(self, result: TranslationResult) -> None:
        self._translate_btn.setEnabled(True)
        self._translate_btn.setText("翻译")

        if result.success:
            self._output_text.setPlainText(result.translated_text)
            self.translation_completed.emit(result)
        else:
            self._output_text.setPlainText(f"翻译失败: {result.error}")
            QMessageBox.critical(self, "错误", f"翻译失败: {result.error}")

    def _on_translation_error(self, exc: Exception) -> None:
        self._translate_btn.setEnabled(True)
        self._translate_btn.setText("翻译")

        error_msg = f"翻译出错: {str(exc)}"
        self._output_text.setPlainText(error_msg)
        QMessageBox.critical(self, "错误", error_msg)

    def set_languages(self, from_lang: str, to_lang: str) -> None:
        self._from_lang_selector.set_selected_code(from_lang)
        self._to_lang_selector.set_selected_code(to_lang)
