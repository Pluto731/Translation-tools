from __future__ import annotations

from typing import Callable

from pynput import keyboard


class HotkeyManager:

    def __init__(self, hotkey_str: str, callback: Callable[[], None]) -> None:
        self._hotkey_str = hotkey_str
        self._callback = callback
        self._listener = None

    def _parse_hotkey(self, hotkey_str: str) -> set:
        keys = set()
        parts = hotkey_str.lower().replace("<", "").replace(">", "").split("+")

        for part in parts:
            part = part.strip()
            if part == "ctrl":
                keys.add(keyboard.Key.ctrl_l)
            elif part == "alt":
                keys.add(keyboard.Key.alt_l)
            elif part == "shift":
                keys.add(keyboard.Key.shift_l)
            elif len(part) == 1:
                keys.add(keyboard.KeyCode.from_char(part))

        return keys

    def start(self) -> None:
        hotkey_keys = self._parse_hotkey(self._hotkey_str)

        def on_press(key):
            pass

        def on_release(key):
            pass

        def for_canonical(f):
            return lambda k: f(self._listener.canonical(k))

        current_keys = set()

        def on_press_canonical(key):
            current_keys.add(key)
            if hotkey_keys.issubset(current_keys):
                self._callback()

        def on_release_canonical(key):
            if key in current_keys:
                current_keys.remove(key)

        self._listener = keyboard.Listener(
            on_press=for_canonical(on_press_canonical),
            on_release=for_canonical(on_release_canonical),
        )
        self._listener.start()

    def stop(self) -> None:
        if self._listener:
            self._listener.stop()
            self._listener = None
