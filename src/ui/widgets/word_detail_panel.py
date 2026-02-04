from __future__ import annotations

from PyQt5.QtWidgets import (
    QGroupBox,
    QLabel,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from src.translation.models import WordDetail


class WordDetailPanel(QWidget):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self) -> None:
        layout = QVBoxLayout(self)

        self._word_label = QLabel()
        self._word_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(self._word_label)

        phonetic_group = QGroupBox("音标")
        phonetic_layout = QVBoxLayout()
        self._phonetic_label = QLabel()
        phonetic_layout.addWidget(self._phonetic_label)
        phonetic_group.setLayout(phonetic_layout)
        layout.addWidget(phonetic_group)

        explains_group = QGroupBox("释义")
        explains_layout = QVBoxLayout()
        self._explains_text = QTextEdit()
        self._explains_text.setReadOnly(True)
        self._explains_text.setMaximumHeight(150)
        explains_layout.addWidget(self._explains_text)
        explains_group.setLayout(explains_layout)
        layout.addWidget(explains_group)

        examples_group = QGroupBox("例句")
        examples_layout = QVBoxLayout()
        self._examples_text = QTextEdit()
        self._examples_text.setReadOnly(True)
        self._examples_text.setMaximumHeight(150)
        examples_layout.addWidget(self._examples_text)
        examples_group.setLayout(examples_layout)
        layout.addWidget(examples_group)

        layout.addStretch()
        self.setLayout(layout)

    def display_word_detail(self, detail: WordDetail) -> None:
        self._word_label.setText(detail.word)

        phonetic_parts = []
        if detail.phonetic:
            phonetic_parts.append(f"/{detail.phonetic}/")
        if detail.uk_phonetic:
            phonetic_parts.append(f"英: /{detail.uk_phonetic}/")
        if detail.us_phonetic:
            phonetic_parts.append(f"美: /{detail.us_phonetic}/")

        self._phonetic_label.setText(" ".join(phonetic_parts) if phonetic_parts else "无音标")

        explains_text = "\n".join(detail.explains) if detail.explains else "无释义"
        self._explains_text.setPlainText(explains_text)

        if detail.examples:
            examples_text = "\n\n".join(
                f"• {ex.source}\n  {ex.target}" for ex in detail.examples
            )
        else:
            examples_text = "无例句"

        self._examples_text.setPlainText(examples_text)

    def clear(self) -> None:
        self._word_label.setText("")
        self._phonetic_label.setText("")
        self._explains_text.clear()
        self._examples_text.clear()
