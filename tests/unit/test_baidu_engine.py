from __future__ import annotations

import hashlib
from unittest.mock import MagicMock, patch

import pytest

from src.translation.baidu_engine import BaiduEngine
from src.translation.models import TranslationRequest


def test_baidu_engine_name():
    engine = BaiduEngine("test_id", "test_key")
    assert engine.name == "baidu"


def test_baidu_engine_generate_sign():
    engine = BaiduEngine("20240101000000001", "test_secret")
    sign = engine._generate_sign("hello", "1234567890")

    expected_raw = "20240101000000001hello1234567890test_secret"
    expected_sign = hashlib.md5(expected_raw.encode("utf-8")).hexdigest()

    assert sign == expected_sign


def test_baidu_engine_missing_credentials():
    engine = BaiduEngine("", "")
    request = TranslationRequest(text="hello", from_lang="en", to_lang="zh")

    result = engine.translate(request)

    assert not result.success
    assert "密钥未配置" in result.error
    assert result.source_text == "hello"
    assert result.translated_text == ""


@patch("src.translation.baidu_engine.httpx.Client")
def test_baidu_engine_translate_success(mock_client_class):
    mock_client = MagicMock()
    mock_client_class.return_value = mock_client

    mock_response = MagicMock()
    mock_response.json.return_value = {
        "from": "en",
        "to": "zh",
        "trans_result": [{"src": "hello", "dst": "你好"}],
    }
    mock_client.get.return_value = mock_response

    engine = BaiduEngine("test_id", "test_key")
    request = TranslationRequest(text="hello", from_lang="en", to_lang="zh")

    result = engine.translate(request)

    assert result.success
    assert result.source_text == "hello"
    assert result.translated_text == "你好"
    assert result.from_lang == "en"
    assert result.to_lang == "zh"
    assert result.engine_name == "baidu"
    assert result.is_word is True


@patch("src.translation.baidu_engine.httpx.Client")
def test_baidu_engine_translate_api_error(mock_client_class):
    mock_client = MagicMock()
    mock_client_class.return_value = mock_client

    mock_response = MagicMock()
    mock_response.json.return_value = {
        "error_code": "52001",
        "error_msg": "请求超时",
    }
    mock_client.get.return_value = mock_response

    engine = BaiduEngine("test_id", "test_key")
    request = TranslationRequest(text="hello", from_lang="en", to_lang="zh")

    result = engine.translate(request)

    assert not result.success
    assert "52001" in result.error
    assert "请求超时" in result.error


@patch("src.translation.baidu_engine.httpx.Client")
def test_baidu_engine_translate_network_error(mock_client_class):
    mock_client = MagicMock()
    mock_client_class.return_value = mock_client

    mock_client.get.side_effect = Exception("Network error")

    engine = BaiduEngine("test_id", "test_key")
    request = TranslationRequest(text="hello", from_lang="en", to_lang="zh")

    result = engine.translate(request)

    assert not result.success
    assert "网络请求失败" in result.error


@patch("src.translation.baidu_engine.httpx.Client")
def test_baidu_engine_lookup_word(mock_client_class):
    mock_client = MagicMock()
    mock_client_class.return_value = mock_client

    mock_response = MagicMock()
    mock_response.json.return_value = {
        "from": "en",
        "to": "zh",
        "trans_result": [{"src": "apple", "dst": "苹果"}],
    }
    mock_client.get.return_value = mock_response

    engine = BaiduEngine("test_id", "test_key")
    result = engine.lookup_word("apple", "en", "zh")

    assert result.success
    assert result.is_word is True
    assert result.word_detail is not None
    assert result.word_detail.word == "apple"
    assert "苹果" in result.word_detail.explains
