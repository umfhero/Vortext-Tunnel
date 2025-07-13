#!/usr/bin/env python3
"""
Test script to debug connection issues.
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

print("🔍 Testing connection setup...")

try:
    from utils.config_manager import ConfigManager
    from network.tailscale_manager import TailscaleManager
    
    # Test configuration
    config = ConfigManager()
    print(f"📋 Current configuration:")
    print(f"   - My Profile IP: {config.get_peer_address('My Profile')}")
    print(f"   - Friend's Profile IP: {config.get_peer_address('Friend\'s Profile')}")
    print(f"   - Connection Role: {config.get_connection_role()}")
    
    # Test Tailscale status
    manager = TailscaleManager()
    print(f"\n🔍 Testing Tailscale status...")
    if manager.check_tailscale_status():
        print("✅ Tailscale is running")
    else:
        print("❌ Tailscale is not running")
        
    print(f"\n🎯 To fix the connection issue:")
    print(f"1. Make sure both computers are running the app")
    print(f"2. On Computer A: Select 'My Profile' and 'Host' role")
    print(f"3. On Computer B: Select 'Friend's Profile' and 'Client' role")
    print(f"4. Click 'Connect' on Computer A first (host)")
    print(f"5. Click 'Connect' on Computer B second (client)")
    print(f"6. Wait for both to show 'Connected!'")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc() 