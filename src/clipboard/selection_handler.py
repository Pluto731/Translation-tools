from __future__ import annotations

import time

import pyperclip
from PyQt5.QtCore import QObject, pyqtSignal
from pynput import keyboard


class SelectionHandler(QObject):
    text_selected = pyqtSignal(str)

    def __init__(self) -> None:
        super().__init__()
        self._kb_controller = keyboard.Controller()

    def capture_selection(self) -> None:
        original_clipboard = ""
        try:
            original_clipboard = pyperclip.paste()
        except Exception:
            pass

        time.sleep(0.1)

        self._release_modifier_keys()

        time.sleep(0.1)

        self._simulate_copy()

        time.sleep(0.2)

        selected_text = ""
        try:
            selected_text = pyperclip.paste()
        except Exception:
            pass

        try:
            if selected_text != original_clipboard:
                pyperclip.copy(original_clipboard)
        except Exception:
            pass

        if selected_text and selected_text.strip():
            self.text_selected.emit(selected_text.strip())

    def _release_modifier_keys(self) -> None:
        try:
            self._kb_controller.release(keyboard.Key.ctrl_l)
            self._kb_controller.release(keyboard.Key.alt_l)
            self._kb_controller.release(keyboard.Key.shift_l)
        except Exception:
            pass

    def _simulate_copy(self) -> None:
        try:
            with self._kb_controller.pressed(keyboard.Key.ctrl_l):
                self._kb_controller.press("c")
                self._kb_controller.release("c")
        except Exception:
            pass
