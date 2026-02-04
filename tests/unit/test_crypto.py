from __future__ import annotations

import pytest

from src.utils.crypto import SimpleCrypto


def test_encrypt_decrypt():
    original = "Hello世界123"

    encrypted = SimpleCrypto.encrypt(original)
    assert encrypted != original
    assert len(encrypted) > 0

    decrypted = SimpleCrypto.decrypt(encrypted)
    assert decrypted == original


def test_encrypt_empty_string():
    encrypted = SimpleCrypto.encrypt("")
    assert encrypted == ""

    decrypted = SimpleCrypto.decrypt("")
    assert decrypted == ""


def test_encrypt_with_custom_salt():
    original = "test123"

    encrypted1 = SimpleCrypto.encrypt(original, "salt1")
    encrypted2 = SimpleCrypto.encrypt(original, "salt2")

    assert encrypted1 != encrypted2

    decrypted1 = SimpleCrypto.decrypt(encrypted1, "salt1")
    decrypted2 = SimpleCrypto.decrypt(encrypted2, "salt2")

    assert decrypted1 == original
    assert decrypted2 == original


def test_decrypt_invalid_data():
    decrypted = SimpleCrypto.decrypt("invalid base64 !!!")
    assert decrypted == ""


def test_encrypt_special_characters():
    original = "!@#$%^&*()_+-=[]{}|;:',.<>?/`~"

    encrypted = SimpleCrypto.encrypt(original)
    decrypted = SimpleCrypto.decrypt(encrypted)

    assert decrypted == original


def test_encrypt_unicode():
    original = "你好世界🌍测试"

    encrypted = SimpleCrypto.encrypt(original)
    decrypted = SimpleCrypto.decrypt(encrypted)

    assert decrypted == original
