"""
Theme manager for Vortex Tunnel application.
Handles dark and light theme switching.
"""

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import QObject


class ThemeManager(QObject):
    """Manages application themes and styling."""
    
    def __init__(self):
        super().__init__()
        self.dark_mode = False
        
    def apply_dark_theme(self):
        """Apply dark theme to the application."""
        self.dark_mode = True
        
        # Create dark palette
        dark_palette = QPalette()
        
        # Set color roles for dark theme
        dark_palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ColorRole.ToolTipText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ColorRole.Text, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ColorRole.ButtonText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 0, 0))
        dark_palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
        
        # Apply palette to application
        QApplication.instance().setPalette(dark_palette)
        
        # Apply dark stylesheet
        self.apply_dark_stylesheet()
        
    def apply_light_theme(self):
        """Apply light theme to the application."""
        self.dark_mode = False
        
        # Reset to default palette
        QApplication.instance().setPalette(QApplication.instance().style().standardPalette())
        
        # Apply light stylesheet
        self.apply_light_stylesheet()
        
    def apply_dark_stylesheet(self):
        """Apply dark mode stylesheet."""
        stylesheet = """
        QMainWindow {
            background-color: #353535;
            color: #ffffff;
        }
        
        QTabWidget::pane {
            border: 1px solid #555555;
            background-color: #353535;
        }
        
        QTabBar::tab {
            background-color: #555555;
            color: #ffffff;
            padding: 8px 16px;
            margin-right: 2px;
        }
        
        QTabBar::tab:selected {
            background-color: #42a2da;
        }
        
        QTabBar::tab:hover {
            background-color: #666666;
        }
        
        QPushButton {
            background-color: #555555;
            color: #ffffff;
            border: 1px solid #777777;
            padding: 5px 10px;
            border-radius: 3px;
        }
        
        QPushButton:hover {
            background-color: #666666;
        }
        
        QPushButton:pressed {
            background-color: #444444;
        }
        
        QLineEdit {
            background-color: #252525;
            color: #ffffff;
            border: 1px solid #555555;
            padding: 5px;
            border-radius: 3px;
        }
        
        QTextEdit {
            background-color: #252525;
            color: #ffffff;
            border: 1px solid #555555;
        }
        
        QListWidget {
            background-color: #252525;
            color: #ffffff;
            border: 1px solid #555555;
        }
        
        QListWidget::item {
            padding: 5px;
        }
        
        QListWidget::item:selected {
            background-color: #42a2da;
        }
        
        QSpinBox {
            background-color: #252525;
            color: #ffffff;
            border: 1px solid #555555;
            padding: 3px;
        }
        
        QComboBox {
            background-color: #252525;
            color: #ffffff;
            border: 1px solid #555555;
            padding: 5px;
        }
        
        QComboBox::drop-down {
            border: none;
        }
        
        QComboBox::down-arrow {
            image: none;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 5px solid #ffffff;
        }
        
        QCheckBox {
            color: #ffffff;
        }
        
        QCheckBox::indicator {
            width: 16px;
            height: 16px;
        }
        
        QCheckBox::indicator:unchecked {
            border: 1px solid #555555;
            background-color: #252525;
        }
        
        QCheckBox::indicator:checked {
            border: 1px solid #42a2da;
            background-color: #42a2da;
        }
        
        QProgressBar {
            border: 1px solid #555555;
            border-radius: 3px;
            text-align: center;
        }
        
        QProgressBar::chunk {
            background-color: #42a2da;
            border-radius: 2px;
        }
        """
        
        QApplication.instance().setStyleSheet(stylesheet)
        
    def apply_light_stylesheet(self):
        """Apply light mode stylesheet."""
        stylesheet = """
        QMainWindow {
            background-color: #f0f0f0;
            color: #000000;
        }
        
        QTabWidget::pane {
            border: 1px solid #c0c0c0;
            background-color: #ffffff;
        }
        
        QTabBar::tab {
            background-color: #e0e0e0;
            color: #000000;
            padding: 8px 16px;
            margin-right: 2px;
        }
        
        QTabBar::tab:selected {
            background-color: #42a2da;
            color: #ffffff;
        }
        
        QTabBar::tab:hover {
            background-color: #d0d0d0;
        }
        
        QPushButton {
            background-color: #e0e0e0;
            color: #000000;
            border: 1px solid #c0c0c0;
            padding: 5px 10px;
            border-radius: 3px;
        }
        
        QPushButton:hover {
            background-color: #d0d0d0;
        }
        
        QPushButton:pressed {
            background-color: #c0c0c0;
        }
        
        QLineEdit {
            background-color: #ffffff;
            color: #000000;
            border: 1px solid #c0c0c0;
            padding: 5px;
            border-radius: 3px;
        }
        
        QTextEdit {
            background-color: #ffffff;
            color: #000000;
            border: 1px solid #c0c0c0;
        }
        
        QListWidget {
            background-color: #ffffff;
            color: #000000;
            border: 1px solid #c0c0c0;
        }
        
        QListWidget::item {
            padding: 5px;
        }
        
        QListWidget::item:selected {
            background-color: #42a2da;
            color: #ffffff;
        }
        
        QSpinBox {
            background-color: #ffffff;
            color: #000000;
            border: 1px solid #c0c0c0;
            padding: 3px;
        }
        
        QComboBox {
            background-color: #ffffff;
            color: #000000;
            border: 1px solid #c0c0c0;
            padding: 5px;
        }
        
        QComboBox::drop-down {
            border: none;
        }
        
        QComboBox::down-arrow {
            image: none;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 5px solid #000000;
        }
        
        QCheckBox {
            color: #000000;
        }
        
        QCheckBox::indicator {
            width: 16px;
            height: 16px;
        }
        
        QCheckBox::indicator:unchecked {
            border: 1px solid #c0c0c0;
            background-color: #ffffff;
        }
        
        QCheckBox::indicator:checked {
            border: 1px solid #42a2da;
            background-color: #42a2da;
        }
        
        QProgressBar {
            border: 1px solid #c0c0c0;
            border-radius: 3px;
            text-align: center;
        }
        
        QProgressBar::chunk {
            background-color: #42a2da;
            border-radius: 2px;
        }
        """
        
        QApplication.instance().setStyleSheet(stylesheet)
        
    def is_dark_mode(self):
        """Check if dark mode is currently active."""
        return self.dark_mode 