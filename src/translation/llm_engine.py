from __future__ import annotations

import httpx

from src.config.constants import LLM_LANGUAGE_NAMES
from src.translation.base_engine import TranslationEngine
from src.translation.models import (
    TranslationRequest,
    TranslationResult,
    WordDetail,
)
from src.utils.text_utils import is_single_word

_SYSTEM_PROMPT = (
    "You are a professional translator. "
    "Translate the user's text from {from_lang} to {to_lang}. "
    "Output ONLY the translated text, nothing else."
)


class LlmEngine(TranslationEngine):

    def __init__(self, api_url: str, api_key: str, model_name: str) -> None:
        self._api_url = api_url.rstrip("/")
        self._api_key = api_key
        self._model_name = model_name
        self._client = httpx.Client(timeout=30.0)

    @property
    def name(self) -> str:
        return "llm"

    def _lang_name(self, code: str) -> str:
        return LLM_LANGUAGE_NAMES.get(code, code)

    def _chat(self, system: str, user_text: str) -> str:
        url = f"{self._api_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }
        body = {
            "model": self._model_name,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user_text},
            ],
            "temperature": 0.3,
        }

        response = self._client.post(url, json=body, headers=headers)

        if response.status_code != 200:
            try:
                detail = response.json().get("error", {}).get("message", response.text)
            except Exception:
                detail = response.text
            raise httpx.HTTPStatusError(
                f"状态码 {response.status_code}: {detail}",
                request=response.request,
                response=response,
            )

        data = response.json()
        return data["choices"][0]["message"]["content"].strip()

    def translate(self, request: TranslationRequest) -> TranslationResult:
        if not self._api_url or not self._api_key or not self._model_name:
            return TranslationResult(
                source_text=request.text,
                translated_text="",
                from_lang=request.from_lang,
                to_lang=request.to_lang,
                engine_name=self.name,
                error="LLM API 未配置（需要地址、密钥和模型名）",
            )

        from_name = self._lang_name(request.from_lang)
        to_name = self._lang_name(request.to_lang)
        system = _SYSTEM_PROMPT.format(from_lang=from_name, to_lang=to_name)

        try:
            translated = self._chat(system, request.text)
        except httpx.HTTPError as exc:
            return TranslationResult(
                source_text=request.text,
                translated_text="",
                from_lang=request.from_lang,
                to_lang=request.to_lang,
                engine_name=self.name,
                error=f"LLM 请求失败: {exc}",
            )
        except (KeyError, IndexError):
            return TranslationResult(
                source_text=request.text,
                translated_text="",
                from_lang=request.from_lang,
                to_lang=request.to_lang,
                engine_name=self.name,
                error="LLM 返回数据格式异常",
            )

        return TranslationResult(
            source_text=request.text,
            translated_text=translated,
            from_lang=request.from_lang,
            to_lang=request.to_lang,
            engine_name=self.name,
            is_word=is_single_word(request.text),
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
