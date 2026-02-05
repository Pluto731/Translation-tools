from __future__ import annotations

import logging
from typing import Callable

from pynput import keyboard

logger = logging.getLogger(__name__)


class HotkeyManager:

    def __init__(self, hotkey_str: str, callback: Callable[[], None]) -> None:
        self._hotkey_str = hotkey_str
        self._callback = callback
        self._hotkeys: keyboard.GlobalHotKeys | None = None

    def start(self) -> None:
        try:
            self._hotkeys = keyboard.GlobalHotKeys(
                {self._hotkey_str: self._callback}
            )
            self._hotkeys.start()
            logger.info("Global hotkey registered: %s", self._hotkey_str)
        except Exception:
            logger.exception("Failed to register global hotkey: %s", self._hotkey_str)

    def stop(self) -> None:
        if self._hotkeys:
            self._hotkeys.stop()
            self._hotkeys = None
