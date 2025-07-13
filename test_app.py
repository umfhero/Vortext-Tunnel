#!/usr/bin/env python3
"""
Test script for Vortex Tunnel application.
Verifies that all components work correctly.
"""

import sys
import os
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    
    try:
        # Initialize QApplication for PyQt6 components
        from PyQt6.QtWidgets import QApplication
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        from main_window import MainWindow
        print("✓ MainWindow imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import MainWindow: {e}")
        return False
        
    try:
        from tabs.drawing_tab import DrawingTab
        print("✓ DrawingTab imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import DrawingTab: {e}")
        return False
        
    try:
        from tabs.chat_tab import ChatTab
        print("✓ ChatTab imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import ChatTab: {e}")
        return False
        
    try:
        from tabs.file_tab import FileTab
        print("✓ FileTab imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import FileTab: {e}")
        return False
        
    try:
        from network.tailscale_manager import TailscaleManager
        print("✓ TailscaleManager imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import TailscaleManager: {e}")
        return False
        
    try:
        from utils.theme_manager import ThemeManager
        print("✓ ThemeManager imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import ThemeManager: {e}")
        return False
        
    try:
        from utils.config_manager import ConfigManager
        print("✓ ConfigManager imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import ConfigManager: {e}")
        return False
        
    return True


def test_config_manager():
    """Test configuration manager functionality."""
    print("\nTesting ConfigManager...")
    
    try:
        from utils.config_manager import ConfigManager
        config = ConfigManager()
        
        # Test settings
        settings = config.load_settings()
        print("✓ Settings loaded successfully")
        
        # Test setting/getting values
        config.set_setting('test_key', 'test_value')
        value = config.get_setting('test_key')
        if value == 'test_value':
            print("✓ Setting/getting values works")
        else:
            print("✗ Setting/getting values failed")
            return False
            
        # Test peer addresses
        address = config.get_peer_address('My Profile')
        print(f"✓ Peer address retrieved: {address}")
        
        return True
        
    except Exception as e:
        print(f"✗ ConfigManager test failed: {e}")
        return False


def test_theme_manager():
    """Test theme manager functionality."""
    print("\nTesting ThemeManager...")
    
    try:
        # Initialize QApplication if not already done
        from PyQt6.QtWidgets import QApplication
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        from utils.theme_manager import ThemeManager
        theme = ThemeManager()
        
        # Test theme switching
        theme.apply_dark_theme()
        if theme.is_dark_mode():
            print("✓ Dark theme applied successfully")
        else:
            print("✗ Dark theme application failed")
            return False
            
        theme.apply_light_theme()
        if not theme.is_dark_mode():
            print("✓ Light theme applied successfully")
        else:
            print("✗ Light theme application failed")
            return False
            
        return True
        
    except Exception as e:
        print(f"✗ ThemeManager test failed: {e}")
        return False


def test_tailscale_manager():
    """Test Tailscale manager functionality."""
    print("\nTesting TailscaleManager...")
    
    try:
        from network.tailscale_manager import TailscaleManager
        manager = TailscaleManager()
        
        # Test status check (will fail if Tailscale not installed)
        status = manager.check_tailscale_status()
        print(f"✓ Tailscale status check: {'Running' if status else 'Not running'}")
        
        # Test peer address retrieval
        address = manager.get_peer_address('My Profile')
        print(f"✓ Peer address: {address}")
        
        return True
        
    except Exception as e:
        print(f"✗ TailscaleManager test failed: {e}")
        return False


def test_file_structure():
    """Test that all required files exist."""
    print("\nTesting file structure...")
    
    required_files = [
        "main.py",
        "requirements.txt",
        "build.py",
        "README.md",
        "src/__init__.py",
        "src/main_window.py",
        "src/tabs/__init__.py",
        "src/tabs/drawing_tab.py",
        "src/tabs/chat_tab.py",
        "src/tabs/file_tab.py",
        "src/tabs/canvas_widget.py",
        "src/network/__init__.py",
        "src/network/tailscale_manager.py",
        "src/utils/__init__.py",
        "src/utils/theme_manager.py",
        "src/utils/config_manager.py"
    ]
    
    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path} - MISSING")
            all_exist = False
            
    return all_exist


def main():
    """Run all tests."""
    print("Vortex Tunnel - Component Tests")
    print("=" * 40)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Imports", test_imports),
        ("Config Manager", test_config_manager),
        ("Theme Manager", test_theme_manager),
        ("Tailscale Manager", test_tailscale_manager)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        if test_func():
            passed += 1
            print(f"✓ {test_name} PASSED")
        else:
            print(f"✗ {test_name} FAILED")
            
    print(f"\n{'='*50}")
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! The application should work correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 