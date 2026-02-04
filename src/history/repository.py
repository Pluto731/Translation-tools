from __future__ import annotations

import json
from datetime import datetime
from typing import Optional

from sqlalchemy import desc, func, or_

from src.database.connection import get_session
from src.history.models import TranslationRecord
from src.translation.models import TranslationResult


class TranslationRepository:

    def create_from_result(self, result: TranslationResult) -> TranslationRecord:
        session = get_session()

        word_detail_json = None
        if result.word_detail:
            word_detail_json = result.word_detail.model_dump_json()

        record = TranslationRecord(
            source_text=result.source_text,
            translated_text=result.translated_text,
            from_lang=result.from_lang,
            to_lang=result.to_lang,
            engine_name=result.engine_name,
            is_word=result.is_word,
            word_detail_json=word_detail_json,
            created_at=datetime.utcnow(),
        )

        try:
            session.add(record)
            session.commit()
            session.refresh(record)
            return record
        finally:
            session.close()

    def find_by_id(self, record_id: int) -> Optional[TranslationRecord]:
        session = get_session()
        try:
            return session.query(TranslationRecord).filter_by(id=record_id).first()
        finally:
            session.close()

    def find_all(
        self, page: int = 1, page_size: int = 20, search_query: str = ""
    ) -> tuple[list[TranslationRecord], int]:
        session = get_session()

        try:
            query = session.query(TranslationRecord)

            if search_query:
                search_pattern = f"%{search_query}%"
                query = query.filter(
                    or_(
                        TranslationRecord.source_text.like(search_pattern),
                        TranslationRecord.translated_text.like(search_pattern),
                    )
                )

            total = query.count()

            records = (
                query.order_by(desc(TranslationRecord.created_at))
                .offset((page - 1) * page_size)
                .limit(page_size)
                .all()
            )

            return records, total
        finally:
            session.close()

    def count(self) -> int:
        session = get_session()
        try:
            return session.query(func.count(TranslationRecord.id)).scalar()
        finally:
            session.close()

    def delete_by_id(self, record_id: int) -> bool:
        session = get_session()
        try:
            record = session.query(TranslationRecord).filter_by(id=record_id).first()
            if record:
                session.delete(record)
                session.commit()
                return True
            return False
        finally:
            session.close()

    def delete_all(self) -> int:
        session = get_session()
        try:
            count = session.query(TranslationRecord).count()
            session.query(TranslationRecord).delete()
            session.commit()
            return count
        finally:
            session.close()
