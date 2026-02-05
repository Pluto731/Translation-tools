from __future__ import annotations

from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from src.history.export_service import ExportService
from src.history.repository import TranslationRepository


class HistoryPanel(QWidget):

    def __init__(self, repository: TranslationRepository, parent=None) -> None:
        super().__init__(parent)

        self._repository = repository
        self._current_page = 1
        self._page_size = 20
        self._search_query = ""

        self._init_ui()
        self._load_data()

    def _init_ui(self) -> None:
        layout = QVBoxLayout(self)

        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("搜索:"))

        self._search_input = QLineEdit()
        self._search_input.setPlaceholderText("输入关键词搜索...")
        self._search_input.returnPressed.connect(self._on_search)
        search_layout.addWidget(self._search_input)

        search_btn = QPushButton("搜索")
        search_btn.clicked.connect(self._on_search)
        search_layout.addWidget(search_btn)

        clear_btn = QPushButton("清除")
        clear_btn.clicked.connect(self._on_clear_search)
        search_layout.addWidget(clear_btn)

        layout.addLayout(search_layout)

        self._table = QTableWidget()
        self._table.setColumnCount(6)
        self._table.setHorizontalHeaderLabels(
            ["ID", "原文", "译文", "语言", "引擎", "时间"]
        )

        header = self._table.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.Stretch)

        self._table.setSelectionBehavior(QTableWidget.SelectRows)
        self._table.setEditTriggers(QTableWidget.NoEditTriggers)
        self._table.doubleClicked.connect(self._on_double_click)

        layout.addWidget(self._table)

        pagination_layout = QHBoxLayout()

        self._page_label = QLabel("第 1 页")
        pagination_layout.addWidget(self._page_label)

        pagination_layout.addStretch()

        prev_btn = QPushButton("上一页")
        prev_btn.clicked.connect(self._on_prev_page)
        pagination_layout.addWidget(prev_btn)

        next_btn = QPushButton("下一页")
        next_btn.clicked.connect(self._on_next_page)
        pagination_layout.addWidget(next_btn)

        layout.addLayout(pagination_layout)

        button_layout = QHBoxLayout()

        refresh_btn = QPushButton("刷新")
        refresh_btn.clicked.connect(self._load_data)
        button_layout.addWidget(refresh_btn)

        export_csv_btn = QPushButton("导出CSV")
        export_csv_btn.clicked.connect(self._on_export_csv)
        button_layout.addWidget(export_csv_btn)

        export_txt_btn = QPushButton("导出TXT")
        export_txt_btn.clicked.connect(self._on_export_txt)
        button_layout.addWidget(export_txt_btn)

        delete_btn = QPushButton("删除选中")
        delete_btn.clicked.connect(self._on_delete_selected)
        button_layout.addWidget(delete_btn)

        delete_all_btn = QPushButton("清空历史")
        delete_all_btn.clicked.connect(self._on_delete_all)
        button_layout.addWidget(delete_all_btn)

        button_layout.addStretch()
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def _load_data(self) -> None:
        records, total = self._repository.find_all(
            page=self._current_page,
            page_size=self._page_size,
            search_query=self._search_query,
        )

        self._table.setRowCount(len(records))

        for row, record in enumerate(records):
            self._table.setItem(row, 0, QTableWidgetItem(str(record.id)))

            source_display = record.source_text[:50] + "..." if len(record.source_text) > 50 else record.source_text
            source_item = QTableWidgetItem(source_display)
            source_item.setToolTip(record.source_text)
            self._table.setItem(row, 1, source_item)

            translated_display = record.translated_text[:50] + "..." if len(record.translated_text) > 50 else record.translated_text
            translated_item = QTableWidgetItem(translated_display)
            translated_item.setToolTip(record.translated_text)
            self._table.setItem(row, 2, translated_item)

            lang_item = QTableWidgetItem(f"{record.from_lang} → {record.to_lang}")
            self._table.setItem(row, 3, lang_item)

            self._table.setItem(row, 4, QTableWidgetItem(record.engine_name))

            time_str = record.created_at.strftime("%Y-%m-%d %H:%M")
            self._table.setItem(row, 5, QTableWidgetItem(time_str))

        total_pages = (total + self._page_size - 1) // self._page_size
        self._page_label.setText(f"第 {self._current_page} / {total_pages} 页 (共 {total} 条)")

    def _on_search(self) -> None:
        self._search_query = self._search_input.text().strip()
        self._current_page = 1
        self._load_data()

    def _on_clear_search(self) -> None:
        self._search_input.clear()
        self._search_query = ""
        self._current_page = 1
        self._load_data()

    def _on_prev_page(self) -> None:
        if self._current_page > 1:
            self._current_page -= 1
            self._load_data()

    def _on_next_page(self) -> None:
        _, total = self._repository.find_all(
            page=1,
            page_size=self._page_size,
            search_query=self._search_query,
        )
        total_pages = (total + self._page_size - 1) // self._page_size

        if self._current_page < total_pages:
            self._current_page += 1
            self._load_data()

    def _on_export_csv(self) -> None:
        records, _ = self._repository.find_all(
            page=1, page_size=999999, search_query=self._search_query
        )

        if not records:
            QMessageBox.warning(self, "提示", "没有可导出的记录")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, "导出CSV", "", "CSV文件 (*.csv)"
        )

        if file_path:
            try:
                ExportService.export_to_csv(records, Path(file_path))
                QMessageBox.information(self, "成功", f"已导出 {len(records)} 条记录")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"导出失败: {str(e)}")

    def _on_export_txt(self) -> None:
        records, _ = self._repository.find_all(
            page=1, page_size=999999, search_query=self._search_query
        )

        if not records:
            QMessageBox.warning(self, "提示", "没有可导出的记录")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, "导出TXT", "", "文本文件 (*.txt)"
        )

        if file_path:
            try:
                ExportService.export_to_txt(records, Path(file_path))
                QMessageBox.information(self, "成功", f"已导出 {len(records)} 条记录")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"导出失败: {str(e)}")

    def _on_double_click(self, index) -> None:
        row = index.row()
        record_id = int(self._table.item(row, 0).text())
        record = self._repository.find_by_id(record_id)
        if record:
            QMessageBox.information(
                self,
                "翻译详情",
                f"原文:\n{record.source_text}\n\n"
                f"译文:\n{record.translated_text}\n\n"
                f"语言: {record.from_lang} → {record.to_lang}\n"
                f"引擎: {record.engine_name}\n"
                f"时间: {record.created_at.strftime('%Y-%m-%d %H:%M:%S')}",
            )

    def _on_delete_selected(self) -> None:
        selected_rows = self._table.selectionModel().selectedRows()

        if not selected_rows:
            QMessageBox.warning(self, "提示", "请先选择要删除的记录")
            return

        reply = QMessageBox.question(
            self,
            "确认",
            f"确定要删除选中的 {len(selected_rows)} 条记录吗？",
            QMessageBox.Yes | QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            for index in selected_rows:
                row = index.row()
                record_id = int(self._table.item(row, 0).text())
                self._repository.delete_by_id(record_id)

            self._load_data()
            QMessageBox.information(self, "成功", "删除成功")

    def _on_delete_all(self) -> None:
        reply = QMessageBox.question(
            self,
            "确认",
            "确定要清空所有翻译历史吗？此操作不可恢复！",
            QMessageBox.Yes | QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            count = self._repository.delete_all()
            self._current_page = 1
            self._load_data()
            QMessageBox.information(self, "成功", f"已删除 {count} 条记录")
