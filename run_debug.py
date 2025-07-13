#!/usr/bin/env python3
"""
Run Vortex Tunnel with debug output.
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Set debug environment variable
os.environ['VORTEX_DEBUG'] = '1'

# Import and run the main application
from main_window import MainWindow
from PyQt6.QtWidgets import QApplication

if __name__ == "__main__":
    print("🚀 Starting Vortex Tunnel with debug output...")
    app = QApplication(sys.argv)
    print("✅ QApplication created")
    window = MainWindow()
    print("✅ MainWindow created")
    window.show()
    print("✅ Window shown - app should be visible now")
    print("🔍 Debug output will appear here when you interact with the app")
    sys.exit(app.exec()) 