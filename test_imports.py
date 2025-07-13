#!/usr/bin/env python3
"""
Test script to check if all imports work correctly.
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

print("Testing imports...")

try:
    print("1. Testing PyQt6...")
    from PyQt6.QtWidgets import QApplication
    print("✅ PyQt6 imported successfully")
    
    print("2. Testing main window...")
    from main_window import MainWindow
    print("✅ MainWindow imported successfully")
    
    print("3. Testing tabs...")
    from tabs.drawing_tab import DrawingTab
    from tabs.chat_tab import ChatTab
    from tabs.file_tab import FileTab
    print("✅ All tabs imported successfully")
    
    print("4. Testing network...")
    from network.tailscale_manager import TailscaleManager
    print("✅ TailscaleManager imported successfully")
    
    print("5. Testing utils...")
    from utils.theme_manager import ThemeManager
    from utils.config_manager import ConfigManager
    print("✅ All utils imported successfully")
    
    print("6. Testing canvas widget...")
    from tabs.canvas_widget import CanvasWidget
    print("✅ CanvasWidget imported successfully")
    
    print("\n🎉 All imports successful! The application should work.")
    
except Exception as e:
    print(f"❌ Import error: {e}")
    import traceback
    traceback.print_exc() 

# Run the build with debug output and show the logs
os.system("python -m PyInstaller --onefile --windowed --name=VortexTunnel --add-data=src;src --hidden-import=PyQt6 --hidden-import=PyQt6.QtCore --hidden-import=PyQt6.QtWidgets --hidden-import=PyQt6.QtGui --collect-all=PyQt6 main.py --log-level=DEBUG")