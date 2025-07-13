"""
Configuration manager for Vortex Tunnel application.
Handles saving and loading application settings.
"""

import os
import json
from pathlib import Path


class ConfigManager:
    """Manages application configuration and settings."""
    
    def __init__(self):
        self.config_dir = self.get_config_directory()
        self.config_file = self.config_dir / "settings.json"
        self.ensure_config_directory()
        
    def get_config_directory(self):
        """Get the configuration directory path."""
        # Use user's home directory for config storage
        home_dir = Path.home()
        config_dir = home_dir / ".vortex_tunnel"
        return config_dir
        
    def ensure_config_directory(self):
        """Ensure the configuration directory exists."""
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
    def load_settings(self):
        """Load application settings from file."""
        default_settings = {
            'dark_mode': False,
            'always_on_top': False,
            'profile': 'My Profile',
            'connection_role': 'auto',  # 'host', 'client', or 'auto'
            'window_geometry': {
                'x': 100,
                'y': 100,
                'width': 1000,
                'height': 700
            },
            'tailscale_peer_addresses': {
                'My Profile': '100.93.161.73',
                'Friend\'s Profile': '100.69.157.127'
            }
        }
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_settings = json.load(f)
                    # Merge with defaults to handle missing keys
                    for key, value in default_settings.items():
                        if key not in loaded_settings:
                            loaded_settings[key] = value
                    return loaded_settings
            except Exception as e:
                print(f"Error loading settings: {e}")
                return default_settings
        else:
            # Create default settings file
            self.save_settings(default_settings)
            return default_settings
            
    def save_settings(self, settings):
        """Save application settings to file."""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving settings: {e}")
            
    def get_setting(self, key, default=None):
        """Get a specific setting value."""
        settings = self.load_settings()
        return settings.get(key, default)
        
    def set_setting(self, key, value):
        """Set a specific setting value."""
        settings = self.load_settings()
        settings[key] = value
        self.save_settings(settings)
        
    def get_window_geometry(self):
        """Get saved window geometry."""
        settings = self.load_settings()
        return settings.get('window_geometry', {
            'x': 100,
            'y': 100,
            'width': 1000,
            'height': 700
        })
        
    def save_window_geometry(self, x, y, width, height):
        """Save window geometry."""
        geometry = {
            'x': x,
            'y': y,
            'width': width,
            'height': height
        }
        self.set_setting('window_geometry', geometry)
        
    def get_peer_address(self, profile):
        """Get the Tailscale peer address for a profile."""
        settings = self.load_settings()
        addresses = settings.get('tailscale_peer_addresses', {})
        return addresses.get(profile, '100.64.0.1')
        
    def set_peer_address(self, profile, address):
        """Set the Tailscale peer address for a profile."""
        settings = self.load_settings()
        addresses = settings.get('tailscale_peer_addresses', {})
        addresses[profile] = address
        settings['tailscale_peer_addresses'] = addresses
        self.save_settings(settings)
        
    def get_connection_role(self):
        """Get the connection role setting."""
        settings = self.load_settings()
        return settings.get('connection_role', 'auto')
        
    def set_connection_role(self, role):
        """Set the connection role."""
        self.set_setting('connection_role', role)
        
    def reset_settings(self):
        """Reset all settings to defaults."""
        if self.config_file.exists():
            self.config_file.unlink()
        return self.load_settings() 