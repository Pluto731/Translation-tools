from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from pydantic import BaseModel


class ApiKeys(BaseModel, frozen=True):
    baidu_app_id: str = ""
    baidu_secret_key: str = ""
    youdao_app_key: str = ""
    youdao_app_secret: str = ""


class Preferences(BaseModel, frozen=True):
    default_engine: str = "baidu"
    default_from_lang: str = "auto"
    default_to_lang: str = "zh"
    hotkey: str = "<ctrl>+<alt>+t"
    show_word_detail: bool = True
    history_page_size: int = 20
    auto_copy_result: bool = False
    start_minimized: bool = False


class AppSettings(BaseModel, frozen=True):
    api_keys: ApiKeys = ApiKeys()
    preferences: Preferences = Preferences()

    @staticmethod
    def load(path: Path) -> AppSettings:
        if path.exists():
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
                return AppSettings(**data)
            except (json.JSONDecodeError, ValueError):
                return AppSettings()
        return AppSettings()

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(self.model_dump(), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    def with_api_keys(self, **kwargs: str) -> AppSettings:
        new_keys = ApiKeys(**{**self.api_keys.model_dump(), **kwargs})
        return AppSettings(api_keys=new_keys, preferences=self.preferences)

    def with_preferences(self, **kwargs) -> AppSettings:
        new_prefs = Preferences(**{**self.preferences.model_dump(), **kwargs})
        return AppSettings(api_keys=self.api_keys, preferences=new_prefs)


_settings_path: Optional[Path] = None
_current_settings: Optional[AppSettings] = None


def init_settings(path: Path) -> AppSettings:
    global _settings_path, _current_settings
    _settings_path = path
    _current_settings = AppSettings.load(path)
    return _current_settings


def get_settings() -> AppSettings:
    if _current_settings is None:
        raise RuntimeError("Settings not initialized. Call init_settings() first.")
    return _current_settings


def update_settings(new_settings: AppSettings) -> AppSettings:
    global _current_settings
    if _settings_path is None:
        raise RuntimeError("Settings not initialized. Call init_settings() first.")
    new_settings.save(_settings_path)
    _current_settings = new_settings
    return _current_settings
