from __future__ import annotations

from pathlib import Path

from PyQt5.QtCore import QThreadPool
from PyQt5.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from src.file_parser.parser_factory import ParserFactory
from src.services.file_translation_service import FileTranslationService
from src.translation.engine_manager import EngineManager
from src.ui.widgets.language_selector import LanguageSelector
from src.utils.async_worker import AsyncWorker


class FileTranslatePanel(QWidget):

    def __init__(self, engine_manager: EngineManager, parent=None) -> None:
        super().__init__(parent)

        self._engine_manager = engine_manager
        self._thread_pool = QThreadPool.globalInstance()
        self._current_file_path = None

        self._init_ui()

    def _init_ui(self) -> None:
        layout = QVBoxLayout(self)

        file_layout = QHBoxLayout()
        self._file_label = QLabel("未选择文件")
        file_layout.addWidget(self._file_label)

        select_file_btn = QPushButton("选择文件")
        select_file_btn.clicked.connect(self._on_select_file)
        file_layout.addWidget(select_file_btn)

        layout.addLayout(file_layout)

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

        self._translate_btn = QPushButton("翻译文件")
        self._translate_btn.clicked.connect(self._on_translate_clicked)
        self._translate_btn.setEnabled(False)
        layout.addWidget(self._translate_btn)

        self._progress_bar = QProgressBar()
        self._progress_bar.setVisible(False)
        layout.addWidget(self._progress_bar)

        layout.addWidget(QLabel("翻译结果:"))
        self._result_text = QTextEdit()
        self._result_text.setReadOnly(True)
        self._result_text.setPlaceholderText("翻译结果将显示在这里...")
        layout.addWidget(self._result_text)

        save_btn = QPushButton("保存翻译结果")
        save_btn.clicked.connect(self._on_save_clicked)
        layout.addWidget(save_btn)

        self.setLayout(layout)

    def _on_select_file(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择文件",
            "",
            "支持的文件 (*.txt *.docx *.pdf);;所有文件 (*.*)",
        )

        if file_path:
            path = Path(file_path)
            if ParserFactory.is_supported(path):
                self._current_file_path = path
                self._file_label.setText(f"已选择: {path.name}")
                self._translate_btn.setEnabled(True)
            else:
                QMessageBox.warning(self, "提示", "不支持的文件格式")
                self._current_file_path = None
                self._file_label.setText("未选择文件")
                self._translate_btn.setEnabled(False)

    def _on_translate_clicked(self) -> None:
        if not self._current_file_path:
            return

        from_lang = self._from_lang_selector.get_selected_code()
        to_lang = self._to_lang_selector.get_selected_code()

        self._translate_btn.setEnabled(False)
        self._progress_bar.setVisible(True)
        self._progress_bar.setValue(0)
        self._result_text.clear()

        service = FileTranslationService(self._engine_manager)

        service.progress_updated.connect(self._on_progress_updated)
        service.translation_completed.connect(self._on_translation_completed)
        service.error_occurred.connect(self._on_error_occurred)

        worker = AsyncWorker(
            service.translate_file,
            self._current_file_path,
            from_lang,
            to_lang,
        )

        self._thread_pool.start(worker)

    def _on_progress_updated(self, current: int, total: int) -> None:
        self._progress_bar.setMaximum(total)
        self._progress_bar.setValue(current)

    def _on_translation_completed(self, translated_text: str) -> None:
        self._translate_btn.setEnabled(True)
        self._progress_bar.setVisible(False)
        self._result_text.setPlainText(translated_text)
        QMessageBox.information(self, "完成", "文件翻译完成！")

    def _on_error_occurred(self, error_msg: str) -> None:
        self._translate_btn.setEnabled(True)
        self._progress_bar.setVisible(False)
        QMessageBox.critical(self, "错误", error_msg)

    def _on_save_clicked(self) -> None:
        text = self._result_text.toPlainText()

        if not text:
            QMessageBox.warning(self, "提示", "没有可保存的内容")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "保存翻译结果",
            "",
            "文本文件 (*.txt);;所有文件 (*.*)",
        )

        if file_path:
            try:
                Path(file_path).write_text(text, encoding="utf-8")
                QMessageBox.information(self, "成功", "翻译结果已保存")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"保存失败: {str(e)}")
