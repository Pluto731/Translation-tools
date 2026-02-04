from __future__ import annotations

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from src.translation.models import TranslationResult
from src.ui.styles.theme import FLOATING_POPUP_STYLE


class FloatingPopup(QWidget):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.setWindowFlags(
            Qt.FramelessWindowHint
            | Qt.WindowStaysOnTopHint
            | Qt.Tool
        )

        self.setAttribute(Qt.WA_TranslucentBackground, False)
        self.setAttribute(Qt.WA_ShowWithoutActivating, True)

        self.setStyleSheet(FLOATING_POPUP_STYLE)

        self._init_ui()

    def _init_ui(self) -> None:
        layout = QVBoxLayout(self)

        header_layout = QHBoxLayout()

        self._title_label = QLabel("翻译结果")
        self._title_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        header_layout.addWidget(self._title_label)

        header_layout.addStretch()

        close_btn = QPushButton("×")
        close_btn.setFixedSize(24, 24)
        close_btn.setStyleSheet("font-size: 18px; padding: 0;")
        close_btn.clicked.connect(self.hide)
        header_layout.addWidget(close_btn)

        layout.addLayout(header_layout)

        self._source_label = QLabel()
        self._source_label.setWordWrap(True)
        self._source_label.setStyleSheet("color: #666; font-size: 12px;")
        layout.addWidget(self._source_label)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setMaximumHeight(200)

        self._result_label = QLabel()
        self._result_label.setWordWrap(True)
        self._result_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        scroll_area.setWidget(self._result_label)

        layout.addWidget(scroll_area)

        self.setLayout(layout)
        self.setMinimumWidth(300)
        self.setMaximumWidth(500)

    def show_translation(self, result: TranslationResult) -> None:
        if not result.success:
            self._title_label.setText("翻译失败")
            self._source_label.setText("")
            self._result_label.setText(result.error or "未知错误")
        else:
            self._title_label.setText(f"翻译 ({result.engine_name})")
            self._source_label.setText(f"原文: {result.source_text}")
            self._result_label.setText(result.translated_text)

        self.adjustSize()

        cursor_pos = QCursor.pos()
        self.move(cursor_pos.x() + 20, cursor_pos.y() + 20)

        self.show()
        self.raise_()
