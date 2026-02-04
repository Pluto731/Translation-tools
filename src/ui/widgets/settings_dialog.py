from __future__ import annotations

from PyQt5.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QGroupBox,
    QLabel,
    QLineEdit,
    QMessageBox,
    QVBoxLayout,
)

from src.config.settings import AppSettings, get_settings, update_settings
from src.ui.widgets.language_selector import LanguageSelector


class SettingsDialog(QDialog):

    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.setWindowTitle("设置")
        self.setMinimumWidth(500)

        self._init_ui()
        self._load_settings()

    def _init_ui(self) -> None:
        layout = QVBoxLayout(self)

        api_group = QGroupBox("API 密钥")
        api_layout = QFormLayout()

        self._baidu_app_id_input = QLineEdit()
        api_layout.addRow("百度翻译 APP ID:", self._baidu_app_id_input)

        self._baidu_secret_key_input = QLineEdit()
        self._baidu_secret_key_input.setEchoMode(QLineEdit.Password)
        api_layout.addRow("百度翻译 密钥:", self._baidu_secret_key_input)

        self._youdao_app_key_input = QLineEdit()
        api_layout.addRow("有道翻译 APP Key:", self._youdao_app_key_input)

        self._youdao_app_secret_input = QLineEdit()
        self._youdao_app_secret_input.setEchoMode(QLineEdit.Password)
        api_layout.addRow("有道翻译 密钥:", self._youdao_app_secret_input)

        api_group.setLayout(api_layout)
        layout.addWidget(api_group)

        prefs_group = QGroupBox("偏好设置")
        prefs_layout = QFormLayout()

        self._engine_selector = QComboBox()
        self._engine_selector.addItem("百度翻译", "baidu")
        self._engine_selector.addItem("有道翻译", "youdao")
        prefs_layout.addRow("默认引擎:", self._engine_selector)

        self._from_lang_selector = LanguageSelector()
        prefs_layout.addRow("默认源语言:", self._from_lang_selector)

        self._to_lang_selector = LanguageSelector()
        prefs_layout.addRow("默认目标语言:", self._to_lang_selector)

        self._hotkey_input = QLineEdit()
        prefs_layout.addRow("全局快捷键:", self._hotkey_input)

        prefs_layout.addRow(
            QLabel("注意: 修改快捷键需要重启应用生效")
        )

        prefs_group.setLayout(prefs_layout)
        layout.addWidget(prefs_group)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(self._on_save)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)

    def _load_settings(self) -> None:
        settings = get_settings()

        self._baidu_app_id_input.setText(settings.api_keys.baidu_app_id)
        self._baidu_secret_key_input.setText(settings.api_keys.baidu_secret_key)
        self._youdao_app_key_input.setText(settings.api_keys.youdao_app_key)
        self._youdao_app_secret_input.setText(settings.api_keys.youdao_app_secret)

        for i in range(self._engine_selector.count()):
            if self._engine_selector.itemData(i) == settings.preferences.default_engine:
                self._engine_selector.setCurrentIndex(i)
                break

        self._from_lang_selector.set_selected_code(settings.preferences.default_from_lang)
        self._to_lang_selector.set_selected_code(settings.preferences.default_to_lang)
        self._hotkey_input.setText(settings.preferences.hotkey)

    def _on_save(self) -> None:
        try:
            current_settings = get_settings()

            new_settings = current_settings.with_api_keys(
                baidu_app_id=self._baidu_app_id_input.text().strip(),
                baidu_secret_key=self._baidu_secret_key_input.text().strip(),
                youdao_app_key=self._youdao_app_key_input.text().strip(),
                youdao_app_secret=self._youdao_app_secret_input.text().strip(),
            )

            new_settings = new_settings.with_preferences(
                default_engine=self._engine_selector.currentData(),
                default_from_lang=self._from_lang_selector.get_selected_code(),
                default_to_lang=self._to_lang_selector.get_selected_code(),
                hotkey=self._hotkey_input.text().strip(),
            )

            update_settings(new_settings)

            QMessageBox.information(
                self,
                "成功",
                "设置已保存。部分设置需要重启应用才能生效。",
            )

            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存设置失败: {str(e)}")
