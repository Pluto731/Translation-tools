from __future__ import annotations

from PyQt5.QtWidgets import QComboBox

from src.config.constants import LANGUAGE_MAP


class LanguageSelector(QComboBox):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setSizeAdjustPolicy(QComboBox.AdjustToContents)

        for display_name, code in LANGUAGE_MAP.items():
            self.addItem(display_name, code)

        self._adjust_width()

    def _adjust_width(self) -> None:
        fm = self.fontMetrics()
        max_width = max(
            fm.horizontalAdvance(self.itemText(i))
            for i in range(self.count())
        )
        self.setMinimumWidth(max_width + 50)

    def get_selected_code(self) -> str:
        return self.currentData()

    def set_selected_code(self, code: str) -> None:
        for i in range(self.count()):
            if self.itemData(i) == code:
                self.setCurrentIndex(i)
                break
