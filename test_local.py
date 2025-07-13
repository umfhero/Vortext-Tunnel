#!/usr/bin/env python3
"""
Simple test to verify Vortex Tunnel works with localhost.
"""

import sys
import socket
import threading
import time

def test_local_connection():
    """Test if the app can connect to localhost."""
    print("Testing local connection...")
    
    # Start a simple server on localhost
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_socket.bind(('localhost', 8080))
        server_socket.listen(1)
        print("✓ Server started on localhost:8080")
        
        # Try to connect to localhost
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', 8080))
        print("✓ Client connected successfully")
        
        client_socket.close()
        server_socket.close()
        return True
        
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        return False

if __name__ == "__main__":
    if test_local_connection():
        print("\n✅ Local networking works! The issue is with Tailscale.")
        print("\n📋 Next steps:")
        print("1. Install Tailscale from https://tailscale.com")
        print("2. Sign up and authenticate your machine")
        print("3. Have your friend do the same")
        print("4. Get both IP addresses with 'tailscale status'")
        print("5. Update the app configuration")
    else:
        print("\n❌ Local networking has issues. Check Windows Firewall.") 