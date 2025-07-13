#!/usr/bin/env python3
"""
Network test script to diagnose connection issues.
"""

import socket
import subprocess
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

print("🔍 Testing network connectivity...")

try:
    from utils.config_manager import ConfigManager
    
    config = ConfigManager()
    my_ip = config.get_peer_address('My Profile')
    friend_ip = config.get_peer_address('Friend\'s Profile')
    port = 8081  # Changed to 8081
    
    print(f"📋 Network Configuration:")
    print(f"   - Your IP: {my_ip}")
    print(f"   - Friend's IP: {friend_ip}")
    print(f"   - Port: {port}")
    
    # Test 1: Check if we can create a socket
    print(f"\n🔧 Test 1: Creating test socket...")
    try:
        test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        test_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        test_socket.bind(('0.0.0.0', port))
        test_socket.listen(1)
        print("✅ Socket created and listening successfully")
        test_socket.close()
    except Exception as e:
        print(f"❌ Socket test failed: {e}")
    
    # Test 2: Check if port is already in use
    print(f"\n🔧 Test 2: Checking if port {port} is in use...")
    try:
        result = subprocess.run(['netstat', '-an'], capture_output=True, text=True)
        if f":{port}" in result.stdout:
            print(f"⚠️  Port {port} might be in use. Check netstat output:")
            for line in result.stdout.split('\n'):
                if f":{port}" in line:
                    print(f"   {line}")
        else:
            print(f"✅ Port {port} appears to be free")
    except Exception as e:
        print(f"❌ Could not check port usage: {e}")
    
    # Test 3: Check Windows Firewall
    print(f"\n🔧 Test 3: Checking Windows Firewall...")
    try:
        result = subprocess.run(['netsh', 'advfirewall', 'show', 'allprofiles'], 
                              capture_output=True, text=True)
        print("✅ Firewall status checked")
    except Exception as e:
        print(f"❌ Could not check firewall: {e}")
    
    print(f"\n🎯 Troubleshooting steps:")
    print(f"1. Make sure Windows Firewall allows Python/your app")
    print(f"2. Try running the app as Administrator")
    print(f"3. Check if any antivirus is blocking the connection")
    print(f"4. Verify both computers can ping each other's Tailscale IPs")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc() 