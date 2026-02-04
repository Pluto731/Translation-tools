from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from pydantic import BaseModel

from src.config.constants import BAIDU_API_URL, YOUDAO_API_URL
from src.utils.crypto import SimpleCrypto

_SECRET_FIELDS = ("baidu_secret_key", "youdao_app_secret", "llm_api_key")


class ApiKeys(BaseModel, frozen=True):
    baidu_app_id: str = ""
    baidu_secret_key: str = ""
    baidu_api_url: str = BAIDU_API_URL
    youdao_app_key: str = ""
    youdao_app_secret: str = ""
    youdao_api_url: str = YOUDAO_API_URL
    llm_api_url: str = ""
    llm_api_key: str = ""
    llm_model_name: str = ""


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
                api_keys_data = data.get("api_keys", {})
                for field in _SECRET_FIELDS:
                    raw = api_keys_data.get(field, "")
                    if raw:
                        api_keys_data[field] = SimpleCrypto.decrypt(raw)
                data["api_keys"] = api_keys_data
                return AppSettings(**data)
            except (json.JSONDecodeError, ValueError):
                return AppSettings()
        return AppSettings()

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        data = self.model_dump()
        for field in _SECRET_FIELDS:
            raw = data["api_keys"].get(field, "")
            if raw:
                data["api_keys"][field] = SimpleCrypto.encrypt(raw)
        path.write_text(
            json.dumps(data, indent=2, ensure_ascii=False),
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
