from __future__ import annotations

from PyQt5.QtWidgets import (
    QAction,
    QMainWindow,
    QMenuBar,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from src.history.repository import TranslationRepository
from src.translation.engine_manager import EngineManager
from src.ui.styles.theme import MAIN_WINDOW_STYLE
from src.ui.widgets.file_translate_panel import FileTranslatePanel
from src.ui.widgets.history_panel import HistoryPanel
from src.ui.widgets.settings_dialog import SettingsDialog
from src.ui.widgets.translation_panel import TranslationPanel


class MainWindow(QMainWindow):

    def __init__(
        self,
        engine_manager: EngineManager,
        repository: TranslationRepository,
    ) -> None:
        super().__init__()

        self._engine_manager = engine_manager
        self._repository = repository

        self._init_ui()
        self._create_menu()

    def _init_ui(self) -> None:
        self.setWindowTitle("桌面翻译工具")
        self.setMinimumSize(800, 600)
        self.setStyleSheet(MAIN_WINDOW_STYLE)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        self._tab_widget = QTabWidget()

        self._translation_panel = TranslationPanel(
            translate_fn=self._engine_manager.translate
        )
        self._tab_widget.addTab(self._translation_panel, "文本翻译")

        self._file_translate_panel = FileTranslatePanel(self._engine_manager)
        self._tab_widget.addTab(self._file_translate_panel, "文件翻译")

        self._history_panel = HistoryPanel(self._repository)
        self._tab_widget.addTab(self._history_panel, "翻译历史")

        layout.addWidget(self._tab_widget)

        central_widget.setLayout(layout)

    def _create_menu(self) -> None:
        menubar = self.menuBar()

        file_menu = menubar.addMenu("文件")

        exit_action = QAction("退出", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        settings_menu = menubar.addMenu("设置")

        preferences_action = QAction("偏好设置", self)
        preferences_action.triggered.connect(self._open_settings)
        settings_menu.addAction(preferences_action)

        help_menu = menubar.addMenu("帮助")

        about_action = QAction("关于", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)

    def _open_settings(self) -> None:
        dialog = SettingsDialog(self)
        dialog.exec_()

    def _show_about(self) -> None:
        from PyQt5.QtWidgets import QMessageBox

        QMessageBox.about(
            self,
            "关于",
            "桌面翻译工具 v1.0\n\n"
            "支持文本翻译、文件翻译和框选翻译\n"
            "使用百度翻译和有道翻译API",
        )

    def get_translation_panel(self) -> TranslationPanel:
        return self._translation_panel
