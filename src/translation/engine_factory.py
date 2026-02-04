from __future__ import annotations

from src.config.settings import ApiKeys
from src.translation.baidu_engine import BaiduEngine
from src.translation.base_engine import TranslationEngine
from src.translation.llm_engine import LlmEngine
from src.translation.youdao_engine import YoudaoEngine


class EngineFactory:

    @staticmethod
    def create_baidu_engine(api_keys: ApiKeys) -> BaiduEngine:
        return BaiduEngine(
            app_id=api_keys.baidu_app_id,
            secret_key=api_keys.baidu_secret_key,
            api_url=api_keys.baidu_api_url,
        )

    @staticmethod
    def create_youdao_engine(api_keys: ApiKeys) -> YoudaoEngine:
        return YoudaoEngine(
            app_key=api_keys.youdao_app_key,
            app_secret=api_keys.youdao_app_secret,
            api_url=api_keys.youdao_api_url,
        )

    @staticmethod
    def create_llm_engine(api_keys: ApiKeys) -> LlmEngine:
        return LlmEngine(
            api_url=api_keys.llm_api_url,
            api_key=api_keys.llm_api_key,
            model_name=api_keys.llm_model_name,
        )

    @staticmethod
    def create_all_engines(api_keys: ApiKeys) -> list[TranslationEngine]:
        return [
            EngineFactory.create_baidu_engine(api_keys),
            EngineFactory.create_youdao_engine(api_keys),
            EngineFactory.create_llm_engine(api_keys),
        ]
