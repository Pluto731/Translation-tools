MAIN_WINDOW_STYLE = """
QMainWindow {
    background-color: #f5f5f5;
}

QTabWidget::pane {
    border: 1px solid #dcdcdc;
    background-color: #ffffff;
}

QTabBar::tab {
    background-color: #e0e0e0;
    color: #333333;
    padding: 8px 20px;
    margin-right: 2px;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
}

QTabBar::tab:selected {
    background-color: #ffffff;
    color: #1976d2;
    font-weight: bold;
}

QTabBar::tab:hover {
    background-color: #eeeeee;
}

QPushButton {
    background-color: #1976d2;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    font-size: 14px;
}

QPushButton:hover {
    background-color: #1565c0;
}

QPushButton:pressed {
    background-color: #0d47a1;
}

QPushButton:disabled {
    background-color: #bdbdbd;
    color: #757575;
}

QLineEdit, QTextEdit, QPlainTextEdit {
    background-color: #ffffff;
    border: 1px solid #dcdcdc;
    border-radius: 4px;
    padding: 6px;
    font-size: 13px;
}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
    border: 2px solid #1976d2;
}

QComboBox {
    background-color: #ffffff;
    border: 1px solid #dcdcdc;
    border-radius: 4px;
    padding: 6px;
    font-size: 13px;
}

QComboBox:hover {
    border: 1px solid #1976d2;
}

QComboBox::drop-down {
    border: none;
}

QLabel {
    color: #333333;
    font-size: 13px;
}

QProgressBar {
    border: 1px solid #dcdcdc;
    border-radius: 4px;
    text-align: center;
    background-color: #f5f5f5;
}

QProgressBar::chunk {
    background-color: #1976d2;
    border-radius: 3px;
}
"""

FLOATING_POPUP_STYLE = """
QWidget {
    background-color: #ffffff;
    border: 2px solid #1976d2;
    border-radius: 8px;
}

QLabel {
    color: #333333;
    font-size: 13px;
    padding: 8px;
}

QPushButton {
    background-color: #1976d2;
    color: white;
    border: none;
    padding: 6px 12px;
    border-radius: 4px;
    font-size: 12px;
}

QPushButton:hover {
    background-color: #1565c0;
}
"""
