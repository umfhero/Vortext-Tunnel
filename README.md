# Vortex Tunnel

A real-time collaborative desktop application that connects your PC to your friend's over the internet using Tailscale. Draw together, chat, and share files in real-time without any server setup or port forwarding.

## Features

- **🎨 Real-time Drawing**: Collaborative whiteboard where both users can draw simultaneously
- **💬 Live Chat**: Instant messaging between connected peers
- **📁 File Sharing**: Drag-and-drop file transfer with progress tracking
- **🌙 Dark/Light Mode**: Toggle between themes for comfortable viewing
- **🔝 Always on Top**: Keep the app floating above other windows
- **🔒 Secure**: Uses Tailscale for encrypted peer-to-peer communication
- **🚀 No Servers**: Direct connection between computers

## Prerequisites

Before using Vortex Tunnel, you need to:

1. **Install Tailscale** on both computers:

   - Download from [tailscale.com](https://tailscale.com/)
   - Sign up for a free account
   - Install and authenticate on both machines

2. **Get Tailscale IP Addresses**:
   - Run `tailscale status` on both computers
   - Note the IP addresses (they look like `100.64.x.x`)

## Installation

### Option 1: Download Pre-built Executable

1. Download the latest `VortexTunnel.exe` from releases
2. Double-click to run (no installation required)

### Option 2: Build from Source

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/vortex-tunnel.git
   cd vortex-tunnel
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:

   ```bash
   python main.py
   ```

4. **Build executable** (optional):
   ```bash
   python build.py
   ```

## Usage

### First Time Setup

1. **Start Tailscale** on both computers
2. **Launch Vortex Tunnel** on both computers
3. **Configure Peer Addresses**:
   - In the app, go to Settings
   - Enter your friend's Tailscale IP address
   - Have your friend enter your Tailscale IP address

### Connecting

1. **Choose Profile**: Select "My Profile" or "Friend's Profile"
2. **Click Connect**: The app will establish a peer-to-peer connection
3. **Start Collaborating**: Use any of the three tabs:
   - **Drawing**: Click and drag to draw together
   - **Chat**: Type messages in real-time
   - **Files**: Drag files to share them

### Features Guide

#### Drawing Tab

- **Color Picker**: Click the color button to choose drawing color
- **Brush Size**: Adjust the size spinner to change line thickness
- **Clear Canvas**: Click "Clear Canvas" to start fresh
- **Real-time Sync**: Both users see each other's strokes instantly

#### Chat Tab

- **Send Messages**: Type and press Enter or click Send
- **Message History**: All messages are displayed with timestamps
- **Clear Chat**: Click "Clear" to remove all messages

#### File Sharing Tab

- **Add Files**: Click "Add File" or drag-and-drop files
- **Send Files**: Select a file and click "Send Selected"
- **Receive Files**: Files appear in the "Received Files" list
- **Save Files**: Select a received file and click "Save Selected"

#### App Settings

- **Theme Toggle**: Click the moon/sun button to switch themes
- **Always on Top**: Check the box to keep the app floating
- **Profile Selection**: Choose which profile to use for connection

## Configuration

### Tailscale Setup

1. **Install Tailscale** on both computers
2. **Authenticate** with your Tailscale account
3. **Get IP Addresses**:
   ```bash
   tailscale status
   ```
4. **Configure in App**: Enter the peer's IP address in the app settings

### Advanced Configuration

The app stores settings in `~/.vortex_tunnel/settings.json`:

```json
{
  "dark_mode": false,
  "always_on_top": false,
  "profile": "My Profile",
  "tailscale_peer_addresses": {
    "My Profile": "100.64.0.2",
    "Friend's Profile": "100.64.0.1"
  }
}
```

## Troubleshooting

### Connection Issues

1. **Check Tailscale Status**:

   ```bash
   tailscale status
   ```

   Ensure both computers show as "Connected"

2. **Verify IP Addresses**: Make sure you're using the correct Tailscale IP addresses

3. **Firewall**: Ensure Windows Firewall allows the app through

4. **Port 8080**: The app uses port 8080 for communication

### Common Problems

- **"Tailscale not running"**: Start Tailscale before launching the app
- **"Connection failed"**: Check that both computers are on the same Tailscale network
- **"File transfer failed"**: Ensure you have write permissions in the save directory

## Development

### Project Structure

```
vortex-tunnel/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── build.py               # Build script
├── src/
│   ├── main_window.py     # Main application window
│   ├── tabs/              # Tab components
│   │   ├── drawing_tab.py
│   │   ├── chat_tab.py
│   │   ├── file_tab.py
│   │   └── canvas_widget.py
│   ├── network/           # Networking components
│   │   └── tailscale_manager.py
│   └── utils/             # Utility components
│       ├── theme_manager.py
│       └── config_manager.py
```

### Building

To create a standalone executable:

```bash
python build.py
```

This creates:

- `dist/VortexTunnel.exe` - The main executable
- `install.bat` - Simple installer script

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

- **Issues**: Report bugs on GitHub
- **Discussions**: Ask questions in GitHub Discussions
- **Documentation**: Check the wiki for detailed guides

## Acknowledgments

- **Tailscale** for providing the secure networking layer
- **PyQt6** for the cross-platform GUI framework
- **PyInstaller** for creating standalone executables

---

**Vortex Tunnel** - Connect, Collaborate, Create
