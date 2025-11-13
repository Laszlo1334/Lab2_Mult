# Desktop Media Player

A simple desktop media player application built with Python, Tkinter, and VLC. This application supports playing local audio and video files as well as streaming media from URLs.

## Features

- 🎵 **Audio and Video Playback**: Support for various formats (MP3, MP4, AVI, MKV, WAV, FLAC, MOV)
- 🌐 **Stream Playback**: Play media from URLs (HTTP, HTTPS, RTSP, etc.)
- ⏯️ **Standard Controls**: Play/Pause, Stop, Forward (10s), Backward (10s)
- 📊 **Progress Visualization**: Slider showing playback progress
- ⏱️ **Time Display**: Current and total playback time
- 🎬 **Video Display**: Embedded video playback window

## Requirements

- Python 3.10 or higher
- VLC Media Player (must be installed on your system)
- python-vlc library

## Installation

### 1. Install VLC Media Player

#### Windows
Download and install VLC from [https://www.videolan.org/vlc/](https://www.videolan.org/vlc/)

#### macOS
```bash
brew install --cask vlc
```

Or download from [https://www.videolan.org/vlc/](https://www.videolan.org/vlc/)

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install vlc
```

#### Linux (Fedora)
```bash
sudo dnf install vlc
```

### 2. Install Python Dependencies

Create and activate a virtual environment (recommended):

**Windows (PowerShell):**
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Application

```bash
python main.py
```

Or on some systems:
```bash
python3 main.py
```

### Using the Player

#### Opening Media Files
1. Click **File → Open File...** in the menu
2. Select an audio or video file from your computer
3. Click the **Play** button to start playback

#### Playing Streams
1. Click **File → Open Stream...** in the menu
2. Enter the URL of the media stream (e.g., `http://example.com/stream.m3u8`)
3. Click OK to start streaming

#### Playback Controls
- **▶ Play / ⏸ Pause**: Toggle between play and pause
- **⏹ Stop**: Stop playback and reset to the beginning
- **⏮ Back**: Skip backward 10 seconds
- **Forward ⏭**: Skip forward 10 seconds
- **Progress Slider**: Drag to seek to a specific position
- **Time Display**: Shows current time / total duration

### Supported Formats

#### Audio
- MP3, WAV, FLAC, AAC, OGG, and more

#### Video
- MP4, AVI, MKV, MOV, WMV, FLV, and more

#### Streaming Protocols
- HTTP/HTTPS
- RTSP
- MMS
- And other protocols supported by VLC

## Troubleshooting

### "No module named 'tkinter'" Error
Tkinter is usually included with Python, but if it's missing:

**Linux:**
```bash
sudo apt-get install python3-tk
```

### "Failed to initialize VLC" Error
Ensure VLC Media Player is properly installed on your system. The python-vlc library requires VLC to be installed.

### Video Not Displaying
- Make sure the video format is supported by VLC
- Try playing the file directly in VLC to verify it's not corrupted
- Check that VLC is properly installed

### Stream Not Working
- Verify the URL is correct and accessible
- Check your internet connection
- Some streams may require specific codecs or protocols

## Development

### Project Structure
```
.
├── main.py              # Main application entry point
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── pyproject.toml      # Project metadata
└── src/
    └── lab2_mult/      # Python package (for future extensions)
```

### Contributing
Feel free to submit issues and enhancement requests!

## License

See LICENSE file for details.

## Acknowledgments

- Built with [python-vlc](https://pypi.org/project/python-vlc/)
- Powered by [VLC Media Player](https://www.videolan.org/vlc/)
- GUI framework: [Tkinter](https://docs.python.org/3/library/tkinter.html)


