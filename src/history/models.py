from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class TranslationRecord(Base):
    __tablename__ = "translation_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    source_text: Mapped[str] = mapped_column(Text, nullable=False)
    translated_text: Mapped[str] = mapped_column(Text, nullable=False)
    from_lang: Mapped[str] = mapped_column(String(10), nullable=False)
    to_lang: Mapped[str] = mapped_column(String(10), nullable=False)
    engine_name: Mapped[str] = mapped_column(String(50), nullable=False)
    is_word: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    word_detail_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )

    def __repr__(self) -> str:
        return f"<TranslationRecord(id={self.id}, source='{self.source_text[:20]}...')>"
