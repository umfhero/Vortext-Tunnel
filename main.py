#!/usr/bin/env python3
"""
Vortex Tunnel - Real-time collaborative desktop app
Connects two PCs over the internet using Tailscale for peer-to-peer communication.
"""

import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from src.main_window import MainWindow


def main():
    """Main entry point for Vortex Tunnel application."""
    app = QApplication(sys.argv)
    app.setApplicationName("Vortex Tunnel")
    app.setApplicationVersion("0.2")
    app.setOrganizationName("Vortex Tunnel")
    
    # Set application icon and style
    app.setStyle('Fusion')
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Start the event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main() 