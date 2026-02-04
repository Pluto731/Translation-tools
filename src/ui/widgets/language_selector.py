from __future__ import annotations

from PyQt5.QtWidgets import QComboBox

from src.config.constants import LANGUAGE_MAP


class LanguageSelector(QComboBox):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        for display_name, code in LANGUAGE_MAP.items():
            self.addItem(display_name, code)

    def get_selected_code(self) -> str:
        return self.currentData()

    def set_selected_code(self, code: str) -> None:
        for i in range(self.count()):
            if self.itemData(i) == code:
                self.setCurrentIndex(i)
                break
