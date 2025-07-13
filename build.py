#!/usr/bin/env python3
"""
Build script for Vortex Tunnel application.
Creates a single executable file using PyInstaller.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def build_executable():
    """Build the Vortex Tunnel executable."""
    print("Building Vortex Tunnel...")
    
    # Clean previous builds
    try:
        if os.path.exists("dist"):
            shutil.rmtree("dist")
        if os.path.exists("build"):
            shutil.rmtree("build")
    except PermissionError:
        print("Warning: Could not remove dist/build folders. Continuing...")
        
    # PyInstaller command
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        "--name=VortexTunnel",
        "--add-data=src;src",
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=src",
        "--hidden-import=src.tabs",
        "--hidden-import=src.tabs.drawing_tab",
        "--hidden-import=src.tabs.chat_tab",
        "--hidden-import=src.tabs.file_tab",
        "--hidden-import=src.tabs.canvas_widget",
        "--hidden-import=src.network",
        "--hidden-import=src.network.tailscale_manager",
        "--hidden-import=src.utils",
        "--hidden-import=src.utils.theme_manager",
        "--hidden-import=src.utils.config_manager",
        "--collect-all=PyQt6",
        "main.py"
    ]
    
    try:
        # Run PyInstaller
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("Build completed successfully!")
        print(f"Executable created at: {os.path.abspath('dist/VortexTunnel.exe')}")
        
    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}")
        print(f"Error output: {e.stderr}")
        return False
        
    return True


def create_installer():
    """Create a simple installer script."""
    installer_content = '''@echo off
echo Installing Vortex Tunnel...
echo.

REM Check if Tailscale is installed
tailscale --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Warning: Tailscale is not installed or not in PATH.
    echo Please install Tailscale from https://tailscale.com/
    echo.
    pause
)

REM Copy executable to Program Files
set "INSTALL_DIR=%PROGRAMFILES%\\VortexTunnel"
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

copy "VortexTunnel.exe" "%INSTALL_DIR%\\"

REM Create desktop shortcut
set "DESKTOP=%USERPROFILE%\\Desktop"
set "SHORTCUT=%DESKTOP%\\VortexTunnel.lnk"

echo @echo off > "%TEMP%\\create_shortcut.vbs"
echo Set oWS = WScript.CreateObject("WScript.Shell") >> "%TEMP%\\create_shortcut.vbs"
echo sLinkFile = "%SHORTCUT%" >> "%TEMP%\\create_shortcut.vbs"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%TEMP%\\create_shortcut.vbs"
echo oLink.TargetPath = "%INSTALL_DIR%\\VortexTunnel.exe" >> "%TEMP%\\create_shortcut.vbs"
echo oLink.WorkingDirectory = "%INSTALL_DIR%" >> "%TEMP%\\create_shortcut.vbs"
echo oLink.Save >> "%TEMP%\\create_shortcut.vbs"

cscript //nologo "%TEMP%\\create_shortcut.vbs"
del "%TEMP%\\create_shortcut.vbs"

echo.
echo Vortex Tunnel has been installed successfully!
echo You can find it on your desktop and in the Start menu.
echo.
pause
'''
    
    with open("install.bat", "w") as f:
        f.write(installer_content)
    
    print("Installer script created: install.bat")


def main():
    """Main build function."""
    print("Vortex Tunnel Build Script")
    print("=" * 40)
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
    except ImportError:
        print("PyInstaller not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Build the executable
    if build_executable():
        # Create installer
        create_installer()
        
        print("\nBuild Summary:")
        print("- Executable: dist/VortexTunnel.exe")
        print("- Installer: install.bat")
        print("\nTo install, run: install.bat")
        print("To run directly: dist/VortexTunnel.exe")
    else:
        print("Build failed!")
        sys.exit(1)


if __name__ == "__main__":
    main() 