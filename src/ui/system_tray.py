from __future__ import annotations

from PyQt5.QtWidgets import QAction, QMenu, QSystemTrayIcon

from src.ui.styles.theme import create_app_icon


class SystemTray(QSystemTrayIcon):

    def __init__(self, main_window, parent=None) -> None:
        super().__init__(parent)

        self._main_window = main_window

        self.setIcon(create_app_icon())
        self.setToolTip("桌面翻译工具")

        self._create_menu()

        self.activated.connect(self._on_activated)

    def _create_menu(self) -> None:
        menu = QMenu()

        show_action = QAction("显示主窗口", self)
        show_action.triggered.connect(self._main_window.show)
        menu.addAction(show_action)

        hide_action = QAction("隐藏主窗口", self)
        hide_action.triggered.connect(self._main_window.hide)
        menu.addAction(hide_action)

        menu.addSeparator()

        quit_action = QAction("退出", self)
        quit_action.triggered.connect(self._on_quit)
        menu.addAction(quit_action)

        self.setContextMenu(menu)

    def _on_activated(self, reason) -> None:
        if reason == QSystemTrayIcon.DoubleClick:
            if self._main_window.isVisible():
                self._main_window.hide()
            else:
                self._main_window.show()
                self._main_window.raise_()
                self._main_window.activateWindow()

    def _on_quit(self) -> None:
        from PyQt5.QtWidgets import QApplication

        QApplication.instance().quit()
