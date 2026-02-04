from __future__ import annotations

import csv
from pathlib import Path

from src.history.models import TranslationRecord


class ExportService:

    @staticmethod
    def export_to_csv(records: list[TranslationRecord], output_path: Path) -> None:
        with open(output_path, "w", newline="", encoding="utf-8-sig") as csvfile:
            fieldnames = [
                "ID",
                "原文",
                "译文",
                "源语言",
                "目标语言",
                "引擎",
                "是否单词",
                "创建时间",
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for record in records:
                writer.writerow(
                    {
                        "ID": record.id,
                        "原文": record.source_text,
                        "译文": record.translated_text,
                        "源语言": record.from_lang,
                        "目标语言": record.to_lang,
                        "引擎": record.engine_name,
                        "是否单词": "是" if record.is_word else "否",
                        "创建时间": record.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    }
                )

    @staticmethod
    def export_to_txt(records: list[TranslationRecord], output_path: Path) -> None:
        with open(output_path, "w", encoding="utf-8") as txtfile:
            for i, record in enumerate(records, 1):
                txtfile.write(f"===== 记录 {i} =====\n")
                txtfile.write(f"ID: {record.id}\n")
                txtfile.write(f"原文: {record.source_text}\n")
                txtfile.write(f"译文: {record.translated_text}\n")
                txtfile.write(f"语言: {record.from_lang} -> {record.to_lang}\n")
                txtfile.write(f"引擎: {record.engine_name}\n")
                txtfile.write(
                    f"是否单词: {'是' if record.is_word else '否'}\n"
                )
                txtfile.write(
                    f"时间: {record.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
                )
                txtfile.write("\n")
