from __future__ import annotations

import re

from src.config.constants import MAX_TEXT_CHUNK_SIZE


def is_single_word(text: str) -> bool:
    stripped = text.strip()
    if not stripped:
        return False
    if re.fullmatch(r"[\u4e00-\u9fff]{1,4}", stripped):
        return True
    if re.fullmatch(r"[a-zA-Z]+(?:-[a-zA-Z]+)?", stripped):
        return True
    return False


def split_text_chunks(text: str, max_size: int = MAX_TEXT_CHUNK_SIZE) -> list[str]:
    if len(text) <= max_size:
        return [text]

    chunks: list[str] = []
    paragraphs = text.split("\n")
    current_chunk = ""

    for paragraph in paragraphs:
        if len(current_chunk) + len(paragraph) + 1 > max_size:
            if current_chunk:
                chunks.append(current_chunk)
            if len(paragraph) > max_size:
                for i in range(0, len(paragraph), max_size):
                    chunks.append(paragraph[i:i + max_size])
                current_chunk = ""
            else:
                current_chunk = paragraph
        else:
            if current_chunk:
                current_chunk += "\n" + paragraph
            else:
                current_chunk = paragraph

    if current_chunk:
        chunks.append(current_chunk)

    return chunks
