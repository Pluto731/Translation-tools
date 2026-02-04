from __future__ import annotations

import hashlib
from unittest.mock import MagicMock, patch

import pytest

from src.translation.models import TranslationRequest
from src.translation.youdao_engine import YoudaoEngine


def test_youdao_engine_name():
    engine = YoudaoEngine("test_key", "test_secret")
    assert engine.name == "youdao"


def test_youdao_engine_truncate():
    engine = YoudaoEngine("test_key", "test_secret")

    short_text = "hello"
    assert engine._truncate(short_text) == "hello"

    long_text = "a" * 50
    truncated = engine._truncate(long_text)
    assert truncated == "a" * 10 + "50" + "a" * 10


def test_youdao_engine_missing_credentials():
    engine = YoudaoEngine("", "")
    request = TranslationRequest(text="hello", from_lang="en", to_lang="zh")

    result = engine.translate(request)

    assert not result.success
    assert "密钥未配置" in result.error
    assert result.source_text == "hello"
    assert result.translated_text == ""


@patch("src.translation.youdao_engine.httpx.Client")
def test_youdao_engine_translate_success(mock_client_class):
    mock_client = MagicMock()
    mock_client_class.return_value = mock_client

    mock_response = MagicMock()
    mock_response.json.return_value = {
        "errorCode": "0",
        "translation": ["你好"],
    }
    mock_client.post.return_value = mock_response

    engine = YoudaoEngine("test_key", "test_secret")
    request = TranslationRequest(text="hello", from_lang="en", to_lang="zh")

    result = engine.translate(request)

    assert result.success
    assert result.source_text == "hello"
    assert result.translated_text == "你好"
    assert result.engine_name == "youdao"
    assert result.is_word is True


@patch("src.translation.youdao_engine.httpx.Client")
def test_youdao_engine_translate_api_error(mock_client_class):
    mock_client = MagicMock()
    mock_client_class.return_value = mock_client

    mock_response = MagicMock()
    mock_response.json.return_value = {
        "errorCode": "108",
    }
    mock_client.post.return_value = mock_response

    engine = YoudaoEngine("test_key", "test_secret")
    request = TranslationRequest(text="hello", from_lang="en", to_lang="zh")

    result = engine.translate(request)

    assert not result.success
    assert "108" in result.error


@patch("src.translation.youdao_engine.httpx.Client")
def test_youdao_engine_translate_network_error(mock_client_class):
    mock_client = MagicMock()
    mock_client_class.return_value = mock_client

    mock_client.post.side_effect = Exception("Network error")

    engine = YoudaoEngine("test_key", "test_secret")
    request = TranslationRequest(text="hello", from_lang="en", to_lang="zh")

    result = engine.translate(request)

    assert not result.success
    assert "网络请求失败" in result.error


@patch("src.translation.youdao_engine.httpx.Client")
def test_youdao_engine_lookup_word(mock_client_class):
    mock_client = MagicMock()
    mock_client_class.return_value = mock_client

    mock_response = MagicMock()
    mock_response.json.return_value = {
        "errorCode": "0",
        "translation": ["苹果"],
        "basic": {
            "phonetic": "ˈæpl",
            "uk-phonetic": "ˈæpl",
            "us-phonetic": "ˈæpl",
            "explains": ["n. 苹果", "n. 苹果树"],
        },
        "web": [
            {"key": "apple pie", "value": ["苹果派"]},
        ],
    }
    mock_client.post.return_value = mock_response

    engine = YoudaoEngine("test_key", "test_secret")
    result = engine.lookup_word("apple", "en", "zh")

    assert result.success
    assert result.is_word is True
    assert result.word_detail is not None
    assert result.word_detail.word == "apple"
    assert result.word_detail.phonetic == "ˈæpl"
    assert len(result.word_detail.explains) == 2
    assert len(result.word_detail.examples) == 1
