from __future__ import annotations

import sys
from pathlib import Path

from PyQt5.QtCore import QThreadPool
from PyQt5.QtWidgets import QApplication

from src.clipboard.hotkey_manager import HotkeyManager
from src.clipboard.selection_handler import SelectionHandler
from src.config.constants import DB_NAME, SETTINGS_FILE
from src.config.settings import get_settings, init_settings
from src.database.connection import init_database
from src.database.migrations import create_tables
from src.history.repository import TranslationRepository
from src.services.translation_service import TranslationService
from src.translation.engine_factory import EngineFactory
from src.translation.engine_manager import EngineManager
from src.ui.floating_popup import FloatingPopup
from src.ui.main_window import MainWindow
from src.ui.system_tray import SystemTray
from src.utils.async_worker import AsyncWorker


class TranslationApp:

    def __init__(self) -> None:
        self._app = QApplication(sys.argv)
        self._app.setApplicationName("桌面翻译工具")
        self._app.setQuitOnLastWindowClosed(False)

        self._data_dir = Path.home() / ".translation_tool"
        self._data_dir.mkdir(parents=True, exist_ok=True)

        self._settings_path = self._data_dir / SETTINGS_FILE
        self._db_path = self._data_dir / DB_NAME

        init_settings(self._settings_path)
        self._settings = get_settings()

        init_database(self._db_path)
        create_tables()

        self._engine_manager = EngineManager()
        self._init_engines()

        self._repository = TranslationRepository()

        self._translation_service = TranslationService(
            self._engine_manager,
            self._repository,
        )

        self._main_window = MainWindow(self._engine_manager, self._repository)

        self._system_tray = SystemTray(self._main_window)
        self._system_tray.show()

        self._floating_popup = FloatingPopup()

        self._selection_handler = SelectionHandler()

        self._hotkey_manager = HotkeyManager(
            hotkey_str=self._settings.preferences.hotkey,
            callback=self._on_hotkey_pressed,
        )

        self._thread_pool = QThreadPool.globalInstance()

        self._connect_signals()

        self._hotkey_manager.start()

    def _init_engines(self) -> None:
        engines = EngineFactory.create_all_engines(self._settings.api_keys)

        for engine in engines:
            self._engine_manager.register_engine(engine)

        engine_name = self._settings.preferences.default_engine
        if engine_name in self._engine_manager.available_engines:
            self._engine_manager.set_current_engine(engine_name)

    def _connect_signals(self) -> None:
        translation_panel = self._main_window.get_translation_panel()

        translation_panel.translation_completed.connect(
            self._on_translation_completed
        )

        self._selection_handler.text_selected.connect(
            self._on_text_selected
        )

        self._translation_service.translation_completed.connect(
            self._floating_popup.show_translation
        )

    def _on_translation_completed(self, result) -> None:
        if result.success:
            self._repository.create_from_result(result)

    def _on_hotkey_pressed(self) -> None:
        worker = AsyncWorker(self._selection_handler.capture_selection)
        self._thread_pool.start(worker)

    def _on_text_selected(self, text: str) -> None:
        worker = AsyncWorker(
            self._translation_service.translate_text,
            text,
            self._settings.preferences.default_from_lang,
            self._settings.preferences.default_to_lang,
        )
        self._thread_pool.start(worker)

    def run(self) -> int:
        self._main_window.show()
        return self._app.exec_()

    def cleanup(self) -> None:
        self._hotkey_manager.stop()
        self._engine_manager.close_all()
