#!/usr/bin/env python3
"""
Debug script to test chat functionality.
"""

import sys
import json
import socket
import threading
import time
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton, QTextEdit
from PyQt6.QtCore import QObject, pyqtSignal

class DebugChat(QObject):
    message_received = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.connected = False
        self.peer_socket = None
        self.listener_socket = None
        
    def start_listener(self):
        """Start listening for connections."""
        try:
            self.listener_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.listener_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.listener_socket.bind(('0.0.0.0', 8080))
            self.listener_socket.listen(1)
            print("✅ Listener started on port 8080")
            
            # Start listener thread
            self.listener_thread = threading.Thread(target=self.listen_for_connections)
            self.listener_thread.daemon = True
            self.listener_thread.start()
            
        except Exception as e:
            print(f"❌ Failed to start listener: {e}")
            
    def listen_for_connections(self):
        """Listen for incoming connections."""
        while True:
            try:
                client_socket, address = self.listener_socket.accept()
                print(f"✅ Peer connected from {address}")
                self.peer_socket = client_socket
                self.connected = True
                
                # Start receiving thread
                receive_thread = threading.Thread(target=self.receive_data)
                receive_thread.daemon = True
                receive_thread.start()
                
            except Exception as e:
                print(f"❌ Listener error: {e}")
                break
                
    def connect_to_peer(self, peer_address):
        """Connect to peer."""
        try:
            self.peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.peer_socket.connect((peer_address, 8080))
            print(f"✅ Connected to {peer_address}")
            self.connected = True
            
            # Start receiving thread
            receive_thread = threading.Thread(target=self.receive_data)
            receive_thread.daemon = True
            receive_thread.start()
            
        except Exception as e:
            print(f"❌ Failed to connect: {e}")
            
    def receive_data(self):
        """Receive data from peer."""
        while self.connected and self.peer_socket:
            try:
                # Receive data length first
                length_data = self.peer_socket.recv(8)
                if not length_data:
                    break
                    
                data_length = int.from_bytes(length_data, 'big')
                print(f"📥 Receiving {data_length} bytes")
                
                # Receive actual data
                data = b''
                while len(data) < data_length:
                    chunk = self.peer_socket.recv(data_length - len(data))
                    if not chunk:
                        break
                    data += chunk
                    
                if data:
                    print(f"📥 Received data: {data.decode('utf-8')}")
                    self.process_received_data(data)
                    
            except Exception as e:
                print(f"❌ Error receiving data: {e}")
                break
                
        print("❌ Connection closed")
        self.connected = False
        
    def process_received_data(self, data):
        """Process received data."""
        try:
            message = json.loads(data.decode('utf-8'))
            message_type = message.get('type')
            content = message.get('content', '')
            
            print(f"📥 Processing {message_type}: {content}")
            
            if message_type == 'chat':
                self.message_received.emit(content)
                
        except Exception as e:
            print(f"❌ Error processing data: {e}")
            
    def send_message(self, message):
        """Send a chat message."""
        if self.connected and self.peer_socket:
            data = {
                'type': 'chat',
                'content': message
            }
            self.send_data(data)
            print(f"📤 Sent message: {message}")
        else:
            print("❌ Not connected, cannot send message")
            
    def send_data(self, data):
        """Send data to peer."""
        try:
            json_data = json.dumps(data).encode('utf-8')
            data_length = len(json_data)
            
            print(f"📤 Sending {data_length} bytes")
            
            # Send length first
            self.peer_socket.send(data_length.to_bytes(8, 'big'))
            
            # Send data
            self.peer_socket.send(json_data)
            
        except Exception as e:
            print(f"❌ Error sending data: {e}")

class DebugChatWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.debug_chat = DebugChat()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Debug Chat")
        self.setGeometry(100, 100, 400, 300)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Chat display
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        layout.addWidget(self.chat_display)
        
        # Message input
        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Type a message...")
        self.message_input.returnPressed.connect(self.send_message)
        layout.addWidget(self.message_input)
        
        # Buttons
        self.send_btn = QPushButton("Send")
        self.send_btn.clicked.connect(self.send_message)
        layout.addWidget(self.send_btn)
        
        self.listen_btn = QPushButton("Start Listener")
        self.listen_btn.clicked.connect(self.start_listener)
        layout.addWidget(self.listen_btn)
        
        self.connect_btn = QPushButton("Connect to Peer")
        self.connect_btn.clicked.connect(self.connect_to_peer)
        layout.addWidget(self.connect_btn)
        
        # Connect signals
        self.debug_chat.message_received.connect(self.receive_message)
        
    def send_message(self):
        message = self.message_input.text().strip()
        if message:
            self.debug_chat.send_message(message)
            self.add_message("You", message)
            self.message_input.clear()
            
    def receive_message(self, message):
        self.add_message("Peer", message)
        
    def add_message(self, sender, message):
        self.chat_display.append(f"[{sender}]: {message}")
        
    def start_listener(self):
        self.debug_chat.start_listener()
        self.chat_display.append("🔊 Started listener on port 8080")
        
    def connect_to_peer(self):
        # You can change this IP address
        peer_address = "100.69.157.127"  # Your friend's IP
        self.debug_chat.connect_to_peer(peer_address)
        self.chat_display.append(f"🔗 Connecting to {peer_address}...")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DebugChatWindow()
    window.show()
    sys.exit(app.exec()) 