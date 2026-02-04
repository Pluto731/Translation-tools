from __future__ import annotations

import json
from pathlib import Path

import pytest

from src.config.settings import AppSettings, ApiKeys, Preferences


def test_api_keys_immutable():
    keys = ApiKeys(baidu_app_id="test_id", baidu_secret_key="test_key")
    with pytest.raises(Exception):
        keys.baidu_app_id = "new_id"


def test_preferences_immutable():
    prefs = Preferences(default_engine="baidu")
    with pytest.raises(Exception):
        prefs.default_engine = "youdao"


def test_app_settings_defaults():
    settings = AppSettings()
    assert settings.api_keys.baidu_app_id == ""
    assert settings.preferences.default_engine == "baidu"
    assert settings.preferences.hotkey == "<ctrl>+<alt>+t"


def test_app_settings_immutable():
    settings = AppSettings()
    with pytest.raises(Exception):
        settings.api_keys = ApiKeys()


def test_save_and_load_settings(tmp_path: Path):
    settings_file = tmp_path / "settings.json"

    original = AppSettings(
        api_keys=ApiKeys(baidu_app_id="test_id", baidu_secret_key="test_key"),
        preferences=Preferences(default_engine="youdao", default_to_lang="en"),
    )

    original.save(settings_file)
    assert settings_file.exists()

    loaded = AppSettings.load(settings_file)
    assert loaded.api_keys.baidu_app_id == "test_id"
    assert loaded.api_keys.baidu_secret_key == "test_key"
    assert loaded.preferences.default_engine == "youdao"
    assert loaded.preferences.default_to_lang == "en"


def test_load_nonexistent_file(tmp_path: Path):
    settings_file = tmp_path / "nonexistent.json"
    loaded = AppSettings.load(settings_file)
    assert loaded == AppSettings()


def test_load_invalid_json(tmp_path: Path):
    settings_file = tmp_path / "invalid.json"
    settings_file.write_text("invalid json content")
    loaded = AppSettings.load(settings_file)
    assert loaded == AppSettings()


def test_with_api_keys():
    original = AppSettings()
    updated = original.with_api_keys(baidu_app_id="new_id", baidu_secret_key="new_key")

    assert original.api_keys.baidu_app_id == ""
    assert updated.api_keys.baidu_app_id == "new_id"
    assert updated.api_keys.baidu_secret_key == "new_key"
    assert updated.api_keys.youdao_app_key == ""


def test_with_preferences():
    original = AppSettings()
    updated = original.with_preferences(default_engine="youdao", hotkey="<ctrl>+<shift>+t")

    assert original.preferences.default_engine == "baidu"
    assert updated.preferences.default_engine == "youdao"
    assert updated.preferences.hotkey == "<ctrl>+<shift>+t"
    assert updated.preferences.default_to_lang == "zh"
