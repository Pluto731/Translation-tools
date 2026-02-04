from __future__ import annotations

from src.config.settings import ApiKeys
from src.translation.baidu_engine import BaiduEngine
from src.translation.base_engine import TranslationEngine
from src.translation.youdao_engine import YoudaoEngine


class EngineFactory:

    @staticmethod
    def create_baidu_engine(api_keys: ApiKeys) -> BaiduEngine:
        return BaiduEngine(
            app_id=api_keys.baidu_app_id,
            secret_key=api_keys.baidu_secret_key,
        )

    @staticmethod
    def create_youdao_engine(api_keys: ApiKeys) -> YoudaoEngine:
        return YoudaoEngine(
            app_key=api_keys.youdao_app_key,
            app_secret=api_keys.youdao_app_secret,
        )

    @staticmethod
    def create_all_engines(api_keys: ApiKeys) -> list[TranslationEngine]:
        return [
            EngineFactory.create_baidu_engine(api_keys),
            EngineFactory.create_youdao_engine(api_keys),
        ]
