"""
Tailscale manager for peer-to-peer networking.
Handles connection establishment and data transmission between peers.
"""

import os
import json
import socket
import threading
import time
from PyQt6.QtCore import QObject, pyqtSignal, QThread
from PyQt6.QtWidgets import QMessageBox


class TailscaleManager(QObject):
    """Manages Tailscale connections and peer communication."""
    
    # Signals
    connection_status_changed = pyqtSignal(bool)
    message_received = pyqtSignal(str)
    drawing_data_received = pyqtSignal(dict)
    file_received = pyqtSignal(str, bytes)
    
    def __init__(self):
        super().__init__()
        self.connected = False
        self.peer_socket = None
        self.listener_socket = None
        self.listener_thread = None
        self.peer_address = None
        self.local_port = 8081
        
    def connect(self, profile):
        """Connect to peer using Tailscale."""
        try:
            import time  # Move import to top of function
            print(f"🔗 Starting connection process for profile: {profile}")
            
            # Check if Tailscale is running
            if not self.check_tailscale_status():
                raise Exception("Tailscale is not running. Please start Tailscale first.")
            print("✅ Tailscale is running")
                
            # Get peer address based on profile
            self.peer_address = self.get_peer_address(profile)
            print(f"📍 Peer address: {self.peer_address}")
            
            # Get connection role from config
            from utils.config_manager import ConfigManager
            config = ConfigManager()
            role = config.get_connection_role()
            print(f"🎭 Connection role: {role}")
            
            if role == 'host':
                # Act as host - listen for connections
                print("🎧 Acting as HOST - listening for connections...")
                self.start_listener()
                print("✅ Host listener started - waiting for peer to connect")
                print(f"⏳ Host is now listening on port {self.local_port}...")
                # Wait for connection to be established
                self.wait_for_connection()
                return
            elif role == 'client':
                # Act as client - connect to host
                print("🔌 Acting as CLIENT - connecting to host...")
                # Wait a moment for host to start listening
                print("⏳ Waiting 2 seconds for host to start listening...")
                time.sleep(2)
                self.connect_to_peer()
                print("✅ Client connection successful")
            else:
                # Auto mode - try both approaches
                print("🔄 Auto mode - trying both host and client...")
                self.start_listener()
                time.sleep(0.5)
                try:
                    self.connect_to_peer()
                    print("✅ Auto connection successful")
                except Exception as connect_error:
                    print(f"❌ Auto connection failed: {connect_error}")
                    print("👂 Waiting for peer to connect to us...")
                    self.wait_for_connection()
                    return
                
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            raise Exception(f"Connection failed: {str(e)}")
            
    def wait_for_connection(self):
        """Wait for connection to be established (for host mode)."""
        print("⏳ Waiting for peer connection...")
        max_wait = 30  # Wait up to 30 seconds
        wait_time = 0
        while not self.connected and wait_time < max_wait:
            time.sleep(0.5)
            wait_time += 0.5
            print(f"⏳ Still waiting... ({wait_time:.1f}s) - connected: {self.connected}, socket: {self.peer_socket is not None}")
            
        if self.connected:
            print("✅ Connection established!")
            print(f"🔍 Final connection state - connected: {self.connected}, socket: {self.peer_socket is not None}")
        else:
            print("❌ Connection timeout - no peer connected")
            raise Exception("Connection timeout - no peer connected within 30 seconds")
            
    def disconnect(self):
        """Disconnect from peer."""
        self.connected = False
        
        if self.peer_socket:
            try:
                self.peer_socket.close()
            except:
                pass
            self.peer_socket = None
            
        if self.listener_socket:
            try:
                self.listener_socket.close()
            except:
                pass
            self.listener_socket = None
            
        if self.listener_thread and self.listener_thread.is_alive():
            self.listener_thread.join(timeout=1)
            
        self.connection_status_changed.emit(False)
        
    def check_tailscale_status(self):
        """Check if Tailscale is running and accessible."""
        try:
            # Try to get Tailscale status using full path
            import subprocess
            import os
            
            # Try different possible paths for tailscale
            possible_paths = [
                'tailscale',  # If in PATH
                r'C:\Program Files\Tailscale\tailscale.exe',
                r'C:\Program Files (x86)\Tailscale\tailscale.exe'
            ]
            
            for path in possible_paths:
                try:
                    result = subprocess.run(
                        [path, 'status'], 
                        capture_output=True, 
                        text=True, 
                        timeout=5
                    )
                    if result.returncode == 0:
                        return True
                except:
                    continue
                    
            return False
        except:
            return False
            
    def get_peer_address(self, profile):
        """Get the peer's Tailscale IP address."""
        # Get the configured peer address from settings
        from utils.config_manager import ConfigManager
        config = ConfigManager()
        return config.get_peer_address(profile)
            
    def start_listener(self):
        """Start listening for incoming connections."""
        try:
            print(f"🔧 Creating socket for port {self.local_port}...")
            self.listener_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.listener_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            print(f"🔧 Binding socket to 0.0.0.0:{self.local_port}...")
            self.listener_socket.bind(('0.0.0.0', self.local_port))
            
            print(f"🔧 Starting to listen on port {self.local_port}...")
            self.listener_socket.listen(1)
            print(f"✅ Successfully listening on port {self.local_port}")
            
            # Start listener thread
            self.listener_thread = threading.Thread(target=self.listen_for_connections)
            self.listener_thread.daemon = True
            self.listener_thread.start()
            print("✅ Listener thread started")
            
        except Exception as e:
            print(f"❌ Failed to start listener: {e}")
            raise Exception(f"Failed to start listener: {str(e)}")
            
    def listen_for_connections(self):
        """Listen for incoming connections in a separate thread."""
        print("👂 Listening for incoming connections...")
        while True:  # Keep listening until we get a connection
            try:
                client_socket, address = self.listener_socket.accept()
                print(f"✅ Peer connected from {address}")
                self.peer_socket = client_socket
                self.connected = True
                self.connection_status_changed.emit(True)
                print("✅ Connection state set to True (listener)")
                self.handle_peer_connection()
                break  # Exit the loop once we have a connection
            except Exception as e:
                print(f"❌ Listener error: {e}")
                break
                
    def connect_to_peer(self):
        """Connect to the peer."""
        try:
            print(f"🔌 Connecting to {self.peer_address}:{self.local_port}")
            self.peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.peer_socket.connect((self.peer_address, self.local_port))
            print("✅ Socket connected successfully")
            
            # Set connection state
            self.connected = True
            self.connection_status_changed.emit(True)
            print("✅ Connection state set to True")
            
            # Start receiving thread
            receive_thread = threading.Thread(target=self.receive_data)
            receive_thread.daemon = True
            receive_thread.start()
            print("✅ Receive thread started")
            
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            raise Exception(f"Failed to connect to peer: {str(e)}")
            
    def handle_peer_connection(self):
        """Handle incoming peer connection."""
        print("🤝 Handling incoming peer connection...")
        # Start receiving thread
        receive_thread = threading.Thread(target=self.receive_data)
        receive_thread.daemon = True
        receive_thread.start()
        print("✅ Receive thread started for incoming connection")
        
    def receive_data(self):
        """Receive data from peer."""
        print("📥 Starting receive data loop...")
        while self.connected and self.peer_socket:
            try:
                print("📥 Waiting for data length...")
                # Receive data length first
                length_data = self.peer_socket.recv(8)
                if not length_data:
                    print("❌ No length data received, connection closed")
                    break
                    
                data_length = int.from_bytes(length_data, 'big')
                print(f"📥 Received data length: {data_length} bytes")
                
                # Receive actual data
                data = b''
                while len(data) < data_length:
                    chunk = self.peer_socket.recv(data_length - len(data))
                    if not chunk:
                        print("❌ Connection closed while receiving data")
                        break
                    data += chunk
                    
                if data:
                    print(f"📥 Received {len(data)} bytes of data")
                    self.process_received_data(data)
                else:
                    print("❌ No data received")
                    
            except Exception as e:
                print(f"❌ Error receiving data: {e}")
                break
                
        print("📥 Receive data loop ended")
        self.disconnect()
        
    def process_received_data(self, data):
        """Process received data and emit appropriate signals."""
        try:
            print(f"🔍 Processing received data: {data[:100]}...")  # Show first 100 chars
            message = json.loads(data.decode('utf-8'))
            message_type = message.get('type')
            content = message.get('content', '')
            
            print(f"📥 Processing received data - type: {message_type}, content: {content}")
            
            if message_type == 'chat':
                print(f"💬 Emitting chat message: {content}")
                self.message_received.emit(content)
            elif message_type == 'drawing':
                print(f"🎨 Emitting drawing data")
                self.drawing_data_received.emit(message.get('data', {}))
            elif message_type == 'file':
                file_name = message.get('name', 'unknown')
                file_data = message.get('data', b'')
                print(f"📁 Emitting file: {file_name}")
                self.file_received.emit(file_name, file_data)
            else:
                print(f"❓ Unknown message type: {message_type}")
                
        except Exception as e:
            print(f"❌ Error processing received data: {e}")
            print(f"❌ Raw data: {data}")
            
    def send_message(self, message):
        """Send a chat message to the peer."""
        print(f"🔤 Sending chat message: {message}")
        print(f"🔍 Connection status - connected: {self.connected}, socket: {self.peer_socket is not None}")
        
        # Force check connection status
        if self.peer_socket and self.peer_socket.fileno() != -1:
            print("✅ Socket is valid and connected")
            self.connected = True
        else:
            print("❌ Socket is invalid or disconnected")
            self.connected = False
            
        if self.connected and self.peer_socket:
            data = {
                'type': 'chat',
                'content': message
            }
            print(f"📤 Sending data: {data}")
            self.send_data(data)
            print(f"✅ Chat message sent successfully")
        else:
            print(f"❌ Cannot send message - connected: {self.connected}, socket: {self.peer_socket is not None}")
            
    def send_drawing_data(self, drawing_data):
        """Send drawing data to the peer."""
        print(f"🎨 Sending drawing data: {len(drawing_data)} points")
        if self.connected and self.peer_socket:
            data = {
                'type': 'drawing',
                'data': drawing_data
            }
            self.send_data(data)
            print(f"✅ Drawing data sent successfully")
        else:
            print(f"❌ Cannot send drawing - connected: {self.connected}, socket: {self.peer_socket is not None}")
            
    def send_file(self, file_path, file_name):
        """Send a file to the peer."""
        print(f"📁 Sending file: {file_name}")
        if self.connected and self.peer_socket and os.path.exists(file_path):
            try:
                with open(file_path, 'rb') as f:
                    file_data = f.read()
                    
                data = {
                    'type': 'file',
                    'name': file_name,
                    'data': file_data
                }
                self.send_data(data)
                print(f"✅ File sent successfully")
                
            except Exception as e:
                print(f"Error sending file: {e}")
        else:
            print(f"❌ Cannot send file - connected: {self.connected}, socket: {self.peer_socket is not None}")
            
    def send_data(self, data):
        """Send data to the peer."""
        try:
            json_data = json.dumps(data).encode('utf-8')
            data_length = len(json_data)
            
            print(f"📦 Sending {data_length} bytes of data")
            
            # Send length first
            self.peer_socket.send(data_length.to_bytes(8, 'big'))
            
            # Send data
            self.peer_socket.send(json_data)
            
            print(f"✅ Data sent successfully")
            
        except Exception as e:
            print(f"❌ Error sending data: {e}")
            self.disconnect() 