from __future__ import annotations

import pytest

from src.translation.baidu_engine import BaiduEngine
from src.translation.engine_manager import EngineManager
from src.translation.models import TranslationRequest


def test_engine_manager_register_and_set():
    manager = EngineManager()
    engine1 = BaiduEngine("id1", "key1")

    manager.register_engine(engine1)

    assert manager.current_engine_name == "baidu"
    assert manager.current_engine is engine1
    assert "baidu" in manager.available_engines


def test_engine_manager_multiple_engines():
    manager = EngineManager()
    engine1 = BaiduEngine("id1", "key1")
    engine2 = BaiduEngine("id2", "key2")

    manager.register_engine(engine1)
    manager.register_engine(engine2)

    assert manager.current_engine_name == "baidu"


def test_engine_manager_set_current_engine():
    manager = EngineManager()
    engine1 = BaiduEngine("id1", "key1")

    manager.register_engine(engine1)
    manager.set_current_engine("baidu")

    assert manager.current_engine_name == "baidu"


def test_engine_manager_set_invalid_engine():
    manager = EngineManager()
    engine1 = BaiduEngine("id1", "key1")

    manager.register_engine(engine1)

    with pytest.raises(ValueError, match="未注册"):
        manager.set_current_engine("nonexistent")


def test_engine_manager_no_engines():
    manager = EngineManager()

    with pytest.raises(RuntimeError, match="没有可用的翻译引擎"):
        _ = manager.current_engine


def test_engine_manager_translate_delegates():
    manager = EngineManager()
    engine = BaiduEngine("", "")

    manager.register_engine(engine)

    request = TranslationRequest(text="hello", from_lang="en", to_lang="zh")
    result = manager.translate(request)

    assert result.engine_name == "baidu"
    assert not result.success


def test_engine_manager_lookup_word_delegates():
    manager = EngineManager()
    engine = BaiduEngine("", "")

    manager.register_engine(engine)

    result = manager.lookup_word("hello", "en", "zh")

    assert result.engine_name == "baidu"
    assert result.is_word is True
