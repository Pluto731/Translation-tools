from __future__ import annotations

import hashlib
import random
import string

import httpx

from src.config.constants import BAIDU_API_URL, BAIDU_LANGUAGE_CODES
from src.translation.base_engine import TranslationEngine
from src.translation.models import (
    TranslationRequest,
    TranslationResult,
    WordDetail,
)
from src.utils.text_utils import is_single_word


class BaiduEngine(TranslationEngine):

    def __init__(self, app_id: str, secret_key: str, api_url: str = BAIDU_API_URL) -> None:
        self._app_id = app_id
        self._secret_key = secret_key
        self._api_url = api_url
        self._client = httpx.Client(timeout=10.0)

    @property
    def name(self) -> str:
        return "baidu"

    def _generate_sign(self, text: str, salt: str) -> str:
        raw = f"{self._app_id}{text}{salt}{self._secret_key}"
        return hashlib.md5(raw.encode("utf-8")).hexdigest()

    def _map_lang_code(self, lang: str) -> str:
        return BAIDU_LANGUAGE_CODES.get(lang, lang)

    def translate(self, request: TranslationRequest) -> TranslationResult:
        if not self._app_id or not self._secret_key:
            return TranslationResult(
                source_text=request.text,
                translated_text="",
                from_lang=request.from_lang,
                to_lang=request.to_lang,
                engine_name=self.name,
                error="百度翻译 API 密钥未配置",
            )

        salt = "".join(random.choices(string.digits, k=10))
        sign = self._generate_sign(request.text, salt)

        params = {
            "q": request.text,
            "from": self._map_lang_code(request.from_lang),
            "to": self._map_lang_code(request.to_lang),
            "appid": self._app_id,
            "salt": salt,
            "sign": sign,
        }

        try:
            response = self._client.get(self._api_url, params=params)
            response.raise_for_status()
            data = response.json()
        except httpx.HTTPError as exc:
            return TranslationResult(
                source_text=request.text,
                translated_text="",
                from_lang=request.from_lang,
                to_lang=request.to_lang,
                engine_name=self.name,
                error=f"网络请求失败: {exc}",
            )

        if "error_code" in data:
            return TranslationResult(
                source_text=request.text,
                translated_text="",
                from_lang=request.from_lang,
                to_lang=request.to_lang,
                engine_name=self.name,
                error=f"百度API错误 {data['error_code']}: {data.get('error_msg', '')}",
            )

        trans_result = data.get("trans_result", [])
        translated_parts = [item.get("dst", "") for item in trans_result]
        translated_text = "\n".join(translated_parts)

        detected_from = data.get("from", request.from_lang)
        detected_to = data.get("to", request.to_lang)

        word_check = is_single_word(request.text)

        return TranslationResult(
            source_text=request.text,
            translated_text=translated_text,
            from_lang=detected_from,
            to_lang=detected_to,
            engine_name=self.name,
            is_word=word_check,
        )

    def lookup_word(self, word: str, from_lang: str, to_lang: str) -> TranslationResult:
        request = TranslationRequest(text=word, from_lang=from_lang, to_lang=to_lang)
        result = self.translate(request)

        if not result.success:
            return result

        detail = WordDetail(
            word=word,
            explains=(result.translated_text,) if result.translated_text else (),
        )

        return TranslationResult(
            source_text=result.source_text,
            translated_text=result.translated_text,
            from_lang=result.from_lang,
            to_lang=result.to_lang,
            engine_name=self.name,
            is_word=True,
            word_detail=detail,
        )

    def close(self) -> None:
        self._client.close()
