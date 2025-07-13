#!/usr/bin/env python3
"""
Reset Vortex Tunnel settings with correct IP addresses.
"""

import json
import os
from pathlib import Path

def reset_settings():
    """Reset settings with correct IP addresses."""
    config_dir = Path.home() / ".vortex_tunnel"
    config_file = config_dir / "settings.json"
    
    # Create config directory if it doesn't exist
    config_dir.mkdir(parents=True, exist_ok=True)
    
    # New settings with correct IP addresses
    settings = {
        'dark_mode': False,
        'always_on_top': False,
        'profile': 'My Profile',
        'connection_role': 'auto',
        'window_geometry': {
            'x': 100,
            'y': 100,
            'width': 1000,
            'height': 700
        },
        'tailscale_peer_addresses': {
            'My Profile': '100.93.161.73',
            'Friend\'s Profile': '100.122.120.65'
        }
    }
    
    # Write settings
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(settings, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Settings reset to: {config_file}")
    print("📋 Current IP addresses:")
    print(f"   My Profile: {settings['tailscale_peer_addresses']['My Profile']}")
    print(f"   Friend's Profile: {settings['tailscale_peer_addresses']['Friend\'s Profile']}")

if __name__ == "__main__":
    reset_settings() 