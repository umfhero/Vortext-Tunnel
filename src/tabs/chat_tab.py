"""
Chat tab for real-time text messaging.
Provides instant messaging between connected peers.
"""

import json
from datetime import datetime
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, 
    QLineEdit, QPushButton, QLabel, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QTextCursor


class ChatTab(QWidget):
    """Chat tab with real-time messaging capabilities."""
    
    # Signals
    message_sent = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """Initialize the chat interface."""
        layout = QVBoxLayout(self)
        
        # Chat display
        self.create_chat_display(layout)
        
        # Message input
        self.create_message_input(layout)
        
    def create_chat_display(self, parent_layout):
        """Create the chat message display area."""
        # Chat header
        header = QLabel("💬 Real-time Chat")
        header.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        parent_layout.addWidget(header)
        
        # Chat text area
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setMinimumHeight(400)
        self.chat_display.setFont(QFont("Consolas", 10))
        parent_layout.addWidget(self.chat_display)
        
    def create_message_input(self, parent_layout):
        """Create the message input area."""
        input_frame = QFrame()
        input_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        input_layout = QHBoxLayout(input_frame)
        
        # Message input field
        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Type your message here...")
        self.message_input.returnPressed.connect(self.send_message)
        
        # Send button
        self.send_btn = QPushButton("Send")
        self.send_btn.clicked.connect(self.send_message)
        
        # Clear button
        self.clear_btn = QPushButton("Clear")
        self.clear_btn.clicked.connect(self.clear_chat)
        
        # Add widgets to input layout
        input_layout.addWidget(self.message_input)
        input_layout.addWidget(self.send_btn)
        input_layout.addWidget(self.clear_btn)
        
        parent_layout.addWidget(input_frame)
        
    def send_message(self):
        """Send a message to the peer."""
        message = self.message_input.text().strip()
        if message:
            print(f"💬 Chat tab sending message: {message}")
            # Add message to local display
            self.add_message("You", message, is_local=True)
            
            # Send message to peer
            self.message_sent.emit(message)
            
            # Clear input field
            self.message_input.clear()
            
    def add_message(self, sender, message, is_local=False):
        """Add a message to the chat display."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Format message
        if is_local:
            formatted_message = f"[{timestamp}] <b>{sender}:</b> {message}"
        else:
            formatted_message = f"[{timestamp}] <i>{sender}:</i> {message}"
            
        # Add to chat display
        self.chat_display.append(formatted_message)
        
        # Scroll to bottom
        cursor = self.chat_display.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.chat_display.setTextCursor(cursor)
        
    def receive_message(self, message):
        """Receive a message from the peer."""
        print(f"💬 Chat tab received message: {message}")
        self.add_message("Peer", message, is_local=False)
        
    def clear_chat(self):
        """Clear the chat display."""
        self.chat_display.clear()
        
    def receive_drawing_data(self, data):
        """Handle drawing data (not used in chat tab)."""
        pass 