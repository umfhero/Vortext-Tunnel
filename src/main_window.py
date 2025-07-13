"""
Main window for Vortex Tunnel application.
Contains the tabbed interface with drawing, chat, and file sharing capabilities.
"""

import os
import json
from PyQt6.QtWidgets import (
    QMainWindow, QTabWidget, QVBoxLayout, QHBoxLayout, 
    QWidget, QPushButton, QLabel, QComboBox, QCheckBox,
    QMessageBox, QFileDialog, QSplitter, QFrame
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QIcon, QPalette, QColor, QFont

from tabs.drawing_tab import DrawingTab
from tabs.chat_tab import ChatTab
from tabs.file_tab import FileTab
from network.tailscale_manager import TailscaleManager
from utils.theme_manager import ThemeManager
from utils.config_manager import ConfigManager


class MainWindow(QMainWindow):
    """Main application window with tabbed interface."""
    
    # Signals
    connection_status_changed = pyqtSignal(bool)
    
    def __init__(self):
        super().__init__()
        print("🔧 Initializing MainWindow...")
        self.config_manager = ConfigManager()
        self.theme_manager = ThemeManager()
        self.tailscale_manager = TailscaleManager()
        print("✅ Managers initialized")
        
        self.init_ui()
        print("✅ UI initialized")
        self.setup_connections()
        print("✅ Signal connections setup")
        self.load_settings()
        print("✅ Settings loaded")
        
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("Vortex Tunnel")
        self.setMinimumSize(800, 600)
        self.resize(1000, 700)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Top toolbar
        self.create_toolbar(main_layout)
        
        # Tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabPosition(QTabWidget.TabPosition.North)
        main_layout.addWidget(self.tab_widget)
        
        # Create tabs
        self.create_tabs()
        
        # Status bar
        self.statusBar().showMessage("Ready")
        
    def create_toolbar(self, parent_layout):
        """Create the top toolbar with controls."""
        toolbar_frame = QFrame()
        toolbar_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        toolbar_layout = QHBoxLayout(toolbar_frame)
        
        # Profile selection
        profile_label = QLabel("Profile:")
        self.profile_combo = QComboBox()
        self.profile_combo.addItems(["My Profile", "Friend's Profile"])
        self.profile_combo.currentTextChanged.connect(self.on_profile_changed)
        
        # Connection button
        self.connect_btn = QPushButton("Connect")
        self.connect_btn.clicked.connect(self.toggle_connection)
        
        # Theme toggle
        self.theme_btn = QPushButton("🌙")
        self.theme_btn.setToolTip("Toggle Dark/Light Mode")
        self.theme_btn.clicked.connect(self.toggle_theme)
        
        # Always on top toggle
        self.always_top_checkbox = QCheckBox("Always on Top")
        self.always_top_checkbox.toggled.connect(self.toggle_always_on_top)
        
        # Add widgets to toolbar
        toolbar_layout.addWidget(profile_label)
        toolbar_layout.addWidget(self.profile_combo)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(self.connect_btn)
        toolbar_layout.addWidget(self.theme_btn)
        toolbar_layout.addWidget(self.always_top_checkbox)
        
        parent_layout.addWidget(toolbar_frame)
        
    def create_tabs(self):
        """Create the main application tabs."""
        # Drawing tab
        self.drawing_tab = DrawingTab()
        self.tab_widget.addTab(self.drawing_tab, "🎨 Drawing")
        
        # Chat tab
        self.chat_tab = ChatTab()
        self.tab_widget.addTab(self.chat_tab, "💬 Chat")
        
        # File sharing tab
        self.file_tab = FileTab()
        self.tab_widget.addTab(self.file_tab, "📁 Files")
        
    def setup_connections(self):
        """Setup signal connections."""
        print("🔗 Setting up signal connections...")
        
        # Connect network signals
        self.tailscale_manager.connection_status_changed.connect(
            self.on_connection_status_changed
        )
        print("✅ Connection status signal connected")
        
        # Connect network received signals to tabs
        self.tailscale_manager.message_received.connect(
            self.chat_tab.receive_message
        )
        print("✅ Chat message signal connected")
        
        self.tailscale_manager.drawing_data_received.connect(
            self.drawing_tab.receive_drawing_data
        )
        print("✅ Drawing data signal connected")
        
        self.tailscale_manager.file_received.connect(
            self.file_tab.receive_file
        )
        print("✅ File received signal connected")
        
        # Connect tab signals to network manager
        self.drawing_tab.drawing_data_sent.connect(
            self.tailscale_manager.send_drawing_data
        )
        print("✅ Drawing data sent signal connected")
        
        self.chat_tab.message_sent.connect(
            self.tailscale_manager.send_message
        )
        print("✅ Chat message sent signal connected")
        
        self.file_tab.file_sent.connect(
            self.tailscale_manager.send_file
        )
        print("✅ File sent signal connected")
        
        print("🎉 All signal connections established!")
        
    def load_settings(self):
        """Load application settings."""
        settings = self.config_manager.load_settings()
        
        # Apply theme
        if settings.get('dark_mode', False):
            self.theme_manager.apply_dark_theme()
        else:
            self.theme_manager.apply_light_theme()
            
        # Apply always on top setting
        always_on_top = settings.get('always_on_top', False)
        self.always_top_checkbox.setChecked(always_on_top)
        self.setWindowFlags(
            self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint
            if always_on_top else self.windowFlags() & ~Qt.WindowType.WindowStaysOnTopHint
        )
        
    def save_settings(self):
        """Save application settings."""
        settings = {
            'dark_mode': self.theme_manager.is_dark_mode(),
            'always_on_top': self.always_top_checkbox.isChecked(),
            'profile': self.profile_combo.currentText()
        }
        self.config_manager.save_settings(settings)
        
    def toggle_connection(self):
        """Toggle connection to peer."""
        if self.connect_btn.text() == "Connect":
            self.connect_to_peer()
        else:
            self.disconnect_from_peer()
            
    def connect_to_peer(self):
        """Connect to the peer using Tailscale."""
        profile = self.profile_combo.currentText()
        print(f"🔌 Attempting to connect as {profile}...")
        self.statusBar().showMessage(f"Connecting as {profile}...")
        
        try:
            self.tailscale_manager.connect(profile)
            self.connect_btn.setText("Disconnect")
            self.statusBar().showMessage("Connected!")
            print("✅ Connection successful!")
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            QMessageBox.critical(self, "Connection Error", str(e))
            self.statusBar().showMessage("Connection failed")
            
    def disconnect_from_peer(self):
        """Disconnect from the peer."""
        try:
            self.tailscale_manager.disconnect()
            self.connect_btn.setText("Connect")
            self.statusBar().showMessage("Disconnected")
        except Exception as e:
            QMessageBox.warning(self, "Disconnect Error", str(e))
            
    def toggle_theme(self):
        """Toggle between dark and light themes."""
        if self.theme_manager.is_dark_mode():
            self.theme_manager.apply_light_theme()
            self.theme_btn.setText("🌙")
        else:
            self.theme_manager.apply_dark_theme()
            self.theme_btn.setText("☀️")
            
    def toggle_always_on_top(self, checked):
        """Toggle always on top window behavior."""
        if checked:
            self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowStaysOnTopHint)
        self.show()
        
    def on_profile_changed(self, profile):
        """Handle profile selection change."""
        self.statusBar().showMessage(f"Profile changed to: {profile}")
        
    def on_connection_status_changed(self, connected):
        """Handle connection status changes."""
        if connected:
            self.statusBar().showMessage("Connected to peer")
        else:
            self.statusBar().showMessage("Disconnected from peer")
            
    def closeEvent(self, event):
        """Handle application close event."""
        self.save_settings()
        self.tailscale_manager.disconnect()
        event.accept() 