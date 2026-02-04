from __future__ import annotations

import hashlib
import time
import uuid

import httpx

from src.config.constants import YOUDAO_API_URL, YOUDAO_LANGUAGE_CODES
from src.translation.base_engine import TranslationEngine
from src.translation.models import (
    TranslationRequest,
    TranslationResult,
    WordDetail,
    WordExample,
)
from src.utils.text_utils import is_single_word


class YoudaoEngine(TranslationEngine):

    def __init__(self, app_key: str, app_secret: str, api_url: str = YOUDAO_API_URL) -> None:
        self._app_key = app_key
        self._app_secret = app_secret
        self._api_url = api_url
        self._client = httpx.Client(timeout=10.0)

    @property
    def name(self) -> str:
        return "youdao"

    def _generate_sign(self, text: str, salt: str, cur_time: str) -> str:
        truncated = self._truncate(text)
        raw = f"{self._app_key}{truncated}{salt}{cur_time}{self._app_secret}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def _truncate(self, text: str) -> str:
        if len(text) <= 20:
            return text
        return text[:10] + str(len(text)) + text[-10:]

    def _map_lang_code(self, lang: str) -> str:
        return YOUDAO_LANGUAGE_CODES.get(lang, lang)

    def translate(self, request: TranslationRequest) -> TranslationResult:
        if not self._app_key or not self._app_secret:
            return TranslationResult(
                source_text=request.text,
                translated_text="",
                from_lang=request.from_lang,
                to_lang=request.to_lang,
                engine_name=self.name,
                error="有道翻译 API 密钥未配置",
            )

        salt = str(uuid.uuid4())
        cur_time = str(int(time.time()))
        sign = self._generate_sign(request.text, salt, cur_time)

        data = {
            "q": request.text,
            "from": self._map_lang_code(request.from_lang),
            "to": self._map_lang_code(request.to_lang),
            "appKey": self._app_key,
            "salt": salt,
            "sign": sign,
            "signType": "v3",
            "curtime": cur_time,
        }

        try:
            response = self._client.post(self._api_url, data=data)
            response.raise_for_status()
            result_data = response.json()
        except httpx.HTTPError as exc:
            return TranslationResult(
                source_text=request.text,
                translated_text="",
                from_lang=request.from_lang,
                to_lang=request.to_lang,
                engine_name=self.name,
                error=f"网络请求失败: {exc}",
            )

        error_code = result_data.get("errorCode")
        if error_code and error_code != "0":
            return TranslationResult(
                source_text=request.text,
                translated_text="",
                from_lang=request.from_lang,
                to_lang=request.to_lang,
                engine_name=self.name,
                error=f"有道API错误 {error_code}",
            )

        translation = result_data.get("translation", [])
        translated_text = "\n".join(translation) if translation else ""

        word_check = is_single_word(request.text)

        return TranslationResult(
            source_text=request.text,
            translated_text=translated_text,
            from_lang=request.from_lang,
            to_lang=request.to_lang,
            engine_name=self.name,
            is_word=word_check,
        )

    def lookup_word(self, word: str, from_lang: str, to_lang: str) -> TranslationResult:
        if not self._app_key or not self._app_secret:
            return TranslationResult(
                source_text=word,
                translated_text="",
                from_lang=from_lang,
                to_lang=to_lang,
                engine_name=self.name,
                error="有道翻译 API 密钥未配置",
            )

        salt = str(uuid.uuid4())
        cur_time = str(int(time.time()))
        sign = self._generate_sign(word, salt, cur_time)

        data = {
            "q": word,
            "from": self._map_lang_code(from_lang),
            "to": self._map_lang_code(to_lang),
            "appKey": self._app_key,
            "salt": salt,
            "sign": sign,
            "signType": "v3",
            "curtime": cur_time,
        }

        try:
            response = self._client.post(self._api_url, data=data)
            response.raise_for_status()
            result_data = response.json()
        except httpx.HTTPError as exc:
            return TranslationResult(
                source_text=word,
                translated_text="",
                from_lang=from_lang,
                to_lang=to_lang,
                engine_name=self.name,
                is_word=True,
                error=f"网络请求失败: {exc}",
            )

        error_code = result_data.get("errorCode")
        if error_code and error_code != "0":
            return TranslationResult(
                source_text=word,
                translated_text="",
                from_lang=from_lang,
                to_lang=to_lang,
                engine_name=self.name,
                is_word=True,
                error=f"有道API错误 {error_code}",
            )

        translation = result_data.get("translation", [])
        translated_text = "\n".join(translation) if translation else ""

        basic = result_data.get("basic", {})
        phonetic = basic.get("phonetic", "")
        uk_phonetic = basic.get("uk-phonetic", "")
        us_phonetic = basic.get("us-phonetic", "")
        explains = tuple(basic.get("explains", []))

        web = result_data.get("web", [])
        examples = []
        for item in web[:3]:
            key = item.get("key", "")
            values = item.get("value", [])
            if key and values:
                examples.append(WordExample(source=key, target="; ".join(values)))

        detail = WordDetail(
            word=word,
            phonetic=phonetic,
            uk_phonetic=uk_phonetic,
            us_phonetic=us_phonetic,
            explains=explains,
            examples=tuple(examples),
        )

        return TranslationResult(
            source_text=word,
            translated_text=translated_text,
            from_lang=from_lang,
            to_lang=to_lang,
            engine_name=self.name,
            is_word=True,
            word_detail=detail,
        )

    def close(self) -> None:
        self._client.close()
