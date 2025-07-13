"""
File sharing tab for real-time file transfer.
Provides drag-and-drop file sharing between connected peers.
"""

import os
import json
from datetime import datetime
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QListWidget, QListWidgetItem, QFileDialog,
    QProgressBar, QFrame, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal, QThread, pyqtSlot
from PyQt6.QtGui import QFont, QDragEnterEvent, QDropEvent


class FileTab(QWidget):
    """File sharing tab with drag-and-drop and transfer capabilities."""
    
    # Signals
    file_sent = pyqtSignal(str, str)  # file_path, file_name
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setup_drag_drop()
        
    def init_ui(self):
        """Initialize the file sharing interface."""
        layout = QVBoxLayout(self)
        
        # Header
        self.create_header(layout)
        
        # File lists
        self.create_file_lists(layout)
        
        # Transfer controls
        self.create_transfer_controls(layout)
        
    def create_header(self, parent_layout):
        """Create the file sharing header."""
        header = QLabel("📁 File Sharing")
        header.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        parent_layout.addWidget(header)
        
    def create_file_lists(self, parent_layout):
        """Create the file list areas."""
        lists_layout = QHBoxLayout()
        
        # Local files
        local_frame = QFrame()
        local_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        local_layout = QVBoxLayout(local_frame)
        
        local_label = QLabel("Local Files")
        local_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        self.local_files_list = QListWidget()
        self.local_files_list.setMinimumHeight(300)
        
        local_layout.addWidget(local_label)
        local_layout.addWidget(self.local_files_list)
        
        # Remote files
        remote_frame = QFrame()
        remote_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        remote_layout = QVBoxLayout(remote_frame)
        
        remote_label = QLabel("Received Files")
        remote_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        self.remote_files_list = QListWidget()
        self.remote_files_list.setMinimumHeight(300)
        
        remote_layout.addWidget(remote_label)
        remote_layout.addWidget(self.remote_files_list)
        
        # Add frames to layout
        lists_layout.addWidget(local_frame)
        lists_layout.addWidget(remote_frame)
        
        parent_layout.addLayout(lists_layout)
        
    def create_transfer_controls(self, parent_layout):
        """Create file transfer controls."""
        controls_frame = QFrame()
        controls_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        controls_layout = QHBoxLayout(controls_frame)
        
        # Add file button
        self.add_file_btn = QPushButton("Add File")
        self.add_file_btn.clicked.connect(self.add_file)
        
        # Send file button
        self.send_file_btn = QPushButton("Send Selected")
        self.send_file_btn.clicked.connect(self.send_selected_file)
        
        # Save file button
        self.save_file_btn = QPushButton("Save Selected")
        self.save_file_btn.clicked.connect(self.save_selected_file)
        
        # Clear lists button
        self.clear_btn = QPushButton("Clear Lists")
        self.clear_btn.clicked.connect(self.clear_lists)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        
        # Add widgets to controls
        controls_layout.addWidget(self.add_file_btn)
        controls_layout.addWidget(self.send_file_btn)
        controls_layout.addWidget(self.save_file_btn)
        controls_layout.addWidget(self.clear_btn)
        controls_layout.addStretch()
        controls_layout.addWidget(self.progress_bar)
        
        parent_layout.addWidget(controls_frame)
        
    def setup_drag_drop(self):
        """Setup drag and drop functionality."""
        self.setAcceptDrops(True)
        
    def dragEnterEvent(self, event: QDragEnterEvent):
        """Handle drag enter events."""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            
    def dropEvent(self, event: QDropEvent):
        """Handle drop events."""
        files = []
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if os.path.isfile(file_path):
                files.append(file_path)
                
        for file_path in files:
            self.add_file_to_list(file_path)
            
    def add_file(self):
        """Open file dialog to add files."""
        files, _ = QFileDialog.getOpenFileNames(
            self, "Select Files to Share", "", "All Files (*.*)"
        )
        
        for file_path in files:
            self.add_file_to_list(file_path)
            
    def add_file_to_list(self, file_path):
        """Add a file to the local files list."""
        if os.path.exists(file_path):
            file_name = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)
            
            # Create list item
            item = QListWidgetItem()
            item.setText(f"{file_name} ({self.format_file_size(file_size)})")
            item.setData(Qt.ItemDataRole.UserRole, file_path)
            
            self.local_files_list.addItem(item)
            
    def send_selected_file(self):
        """Send the selected file to the peer."""
        current_item = self.local_files_list.currentItem()
        if current_item:
            file_path = current_item.data(Qt.ItemDataRole.UserRole)
            file_name = os.path.basename(file_path)
            
            # Send file to peer
            self.file_sent.emit(file_path, file_name)
            
            # Show progress
            self.progress_bar.setVisible(True)
            self.progress_bar.setValue(0)
            
            # Simulate progress (in real implementation, this would track actual transfer)
            self.simulate_transfer_progress()
            
    def save_selected_file(self):
        """Save the selected received file."""
        current_item = self.remote_files_list.currentItem()
        if current_item:
            file_data = current_item.data(Qt.ItemDataRole.UserRole)
            if isinstance(file_data, dict):
                file_name = file_data.get('name', 'unknown')
                
                # Open save dialog
                save_path, _ = QFileDialog.getSaveFileName(
                    self, "Save File", file_name, "All Files (*.*)"
                )
                
                if save_path:
                    try:
                        # In real implementation, this would save the actual file data
                        with open(save_path, 'wb') as f:
                            f.write(file_data.get('data', b''))
                        QMessageBox.information(self, "Success", f"File saved as {save_path}")
                    except Exception as e:
                        QMessageBox.critical(self, "Error", f"Failed to save file: {str(e)}")
                        
    def clear_lists(self):
        """Clear both file lists."""
        self.local_files_list.clear()
        self.remote_files_list.clear()
        
    def receive_file(self, file_name, file_data):
        """Receive a file from the peer."""
        # Create list item for received file
        item = QListWidgetItem()
        item.setText(f"📥 {file_name}")
        item.setData(Qt.ItemDataRole.UserRole, {
            'name': file_name,
            'data': file_data
        })
        
        self.remote_files_list.addItem(item)
        
    def format_file_size(self, size_bytes):
        """Format file size in human readable format."""
        if size_bytes == 0:
            return "0B"
        
        size_names = ["B", "KB", "MB", "GB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
            
        return f"{size_bytes:.1f}{size_names[i]}"
        
    def simulate_transfer_progress(self):
        """Simulate file transfer progress."""
        # In real implementation, this would track actual transfer progress
        import time
        for i in range(101):
            self.progress_bar.setValue(i)
            time.sleep(0.01)  # Simulate transfer time
            
        self.progress_bar.setVisible(False)
        QMessageBox.information(self, "Success", "File sent successfully!") 