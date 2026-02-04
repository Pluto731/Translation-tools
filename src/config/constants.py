BAIDU_API_URL = "https://fanyi-api.baidu.com/api/trans/vip/translate"

YOUDAO_API_URL = "https://openapi.youdao.com/api"

DEFAULT_HOTKEY = "<ctrl>+<alt>+t"

LANGUAGE_MAP = {
    "中文": "zh",
    "英语": "en",
    "日语": "jp",
    "韩语": "kor",
    "法语": "fra",
    "德语": "de",
    "俄语": "ru",
    "西班牙语": "spa",
    "葡萄牙语": "pt",
    "意大利语": "it",
    "自动检测": "auto",
}

LANGUAGE_DISPLAY_NAMES = {v: k for k, v in LANGUAGE_MAP.items()}

BAIDU_LANGUAGE_CODES = {
    "zh": "zh",
    "en": "en",
    "jp": "jp",
    "kor": "kor",
    "fra": "fra",
    "de": "de",
    "ru": "ru",
    "spa": "spa",
    "pt": "pt",
    "it": "it",
    "auto": "auto",
}

YOUDAO_LANGUAGE_CODES = {
    "zh": "zh-CHS",
    "en": "en",
    "jp": "ja",
    "kor": "ko",
    "fra": "fr",
    "de": "de",
    "ru": "ru",
    "spa": "es",
    "pt": "pt",
    "it": "it",
    "auto": "auto",
}

SUPPORTED_FILE_EXTENSIONS = {".txt", ".docx", ".pdf"}

MAX_TEXT_CHUNK_SIZE = 5000

DB_NAME = "translation_history.db"

SETTINGS_FILE = "settings.json"
