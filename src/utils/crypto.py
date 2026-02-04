from __future__ import annotations

import base64
import hashlib


class SimpleCrypto:

    @staticmethod
    def _get_key(salt: str = "translation_tool") -> bytes:
        return hashlib.sha256(salt.encode()).digest()

    @staticmethod
    def encrypt(text: str, salt: str = "translation_tool") -> str:
        if not text:
            return ""

        key = SimpleCrypto._get_key(salt)
        encoded = text.encode("utf-8")

        encrypted = bytes(b ^ key[i % len(key)] for i, b in enumerate(encoded))

        return base64.b64encode(encrypted).decode("ascii")

    @staticmethod
    def decrypt(encrypted_text: str, salt: str = "translation_tool") -> str:
        if not encrypted_text:
            return ""

        try:
            key = SimpleCrypto._get_key(salt)
            encrypted = base64.b64decode(encrypted_text.encode("ascii"))

            decrypted = bytes(b ^ key[i % len(key)] for i, b in enumerate(encrypted))

            return decrypted.decode("utf-8")
        except Exception:
            return ""
