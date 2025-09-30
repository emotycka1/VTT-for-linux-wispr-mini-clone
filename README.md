# Wispr-Flow Clone for Ubuntu

A local voice-to-text application for Ubuntu that allows you to hold a hotkey combination (Ctrl+Alt by default), speak, and have your speech transcribed directly where your cursor is positioned. Privacy-first with 100% local processing.

**Now with GPU acceleration and NVIDIA Parakeet for near real-time, ultra-accurate transcription!**

## Quick Start

**Already installed?** Just double-click the **"Wispr-Flow Clone"** icon on your Desktop!

**New installation?** Follow the Installation section below, then run `./setup-launcher.sh` to create the desktop icon.

## Features

- **Global Hotkey Activation**: Press and hold Ctrl+Alt (configurable) to record
- **Visual Feedback**: Ubuntu's native microphone indicator shows recording status
- **GPU Accelerated**: NVIDIA Parakeet model with CUDA for near-instant transcription
- **Best-in-Class Accuracy**: 98-99% accuracy (1.93 WER on LibriSpeech)
- **Universal Text Injection**: Works in any text field (terminals, browsers, editors, etc.)
- **Privacy-First**: All processing happens locally on your machine
- **Configurable**: Easy YAML configuration for models, hotkeys, and audio settings
- **Modular Design**: Clean architecture with separate components (<300 lines per file)
- **Easy Startup**: Desktop icon and application menu integration

## Requirements

### System Requirements
- Ubuntu 20.04 or later with X11
- Python 3.9 - 3.12
- Microphone access
- NVIDIA GPU with CUDA (recommended for GPU-accelerated models)
  - Tested on: RTX 20/30/40 series GPUs
  - Works with: Any CUDA-compatible NVIDIA GPU with 4GB+ VRAM

### System Dependencies
```bash
# Install required system packages
sudo apt update
sudo apt install -y xdotool portaudio19-dev python3-pyaudio python3-venv
```

## Installation

### 1. Clone or Download
```bash
cd ~/projects
# If you have this as a git repo, clone it
# Otherwise, ensure you're in the wispr-flow-clone directory
cd wispr-flow-clone
```

### 2. Create Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Python Dependencies

**Basic Installation** (Whisper CPU):
```bash
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt
```

**GPU-Accelerated Installation** (Recommended):
```bash
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt

# Install PyTorch with CUDA 12.1
.venv/bin/pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# Install NeMo with Parakeet support
.venv/bin/pip install nemo_toolkit[asr] soundfile
```

**What gets installed:**

Base packages:
- `pynput` - Global hotkey detection
- `pyaudio` - Audio recording
- `faster-whisper` - Fast Whisper transcription
- `PyYAML` - Configuration management
- `numpy` - Audio processing

GPU packages (optional but recommended):
- `torch` with CUDA - GPU acceleration (~2.5GB)
- `nemo_toolkit[asr]` - NVIDIA Parakeet support (~4GB)
- `soundfile` - Audio file handling
- 100+ supporting packages

**Total disk space**: ~7GB for full GPU setup, ~500MB for basic Whisper

## Configuration

Edit `config.yaml` to customize settings:

```yaml
# Choose transcription model
model:
  type: "parakeet"  # Currently using GPU-accelerated Parakeet
  size: "parakeet"  # For Whisper: tiny, base, small, medium, large-v3
  device: "cuda"    # GPU acceleration (or "cpu" for CPU-only)
  language: "en"    # or "auto" for detection

# Customize hotkey
hotkey:
  modifiers: ["ctrl", "alt"]  # Press both together
  key: ""  # empty for modifier-only

# Audio settings
audio:
  sample_rate: 16000  # Target rate for transcription (auto-resamples from device)
  channels: 1         # Mono for speech
  device_index: null  # null = auto-follow system default (USB/Bluetooth/built-in)
```

### Model Selection Guide

**NVIDIA Parakeet** (Currently Active - Best Choice):
- **Accuracy**: 98-99% (1.93 WER on LibriSpeech) - Best available!
- **Speed**: Near real-time with GPU (0.2-0.5s for 5s audio)
- **Requirements**: NVIDIA GPU + CUDA, ~4GB disk space
- **Perfect for**: All use cases with excellent quality
- Model: `nvidia/parakeet-tdt-0.6b-v3`

**Whisper Models** (Alternative - No GPU Required):
- `tiny` - Fastest, ~85% accuracy (~1GB RAM, CPU-friendly)
- `base` - Good balance, ~90% accuracy (~1GB RAM)
- `small` - Better accuracy, ~95% (~2GB RAM)
- `medium` - High accuracy, ~97% (~5GB RAM)
- `large-v3` - Excellent accuracy, ~98% (~10GB RAM)

**Which to Choose:**
- **Have NVIDIA GPU?** → Use Parakeet (already configured!)
- **CPU only?** → Use Whisper `base` or `small`
- **Want faster on GPU?** → Whisper works great on GPU too!

## Usage

### Quick Start

**Option 1: Desktop Icon** (Easiest!)
- Look for **"Wispr-Flow Clone"** icon on your Desktop
- Double-click it to start
- First time: Right-click → "Allow Launching"

**Option 2: Application Menu**
- Press **Super** key
- Type "Wispr"
- Click "Wispr-Flow Clone"

**Option 3: Terminal**
```bash
cd ~/projects/wispr-flow-clone
./start-wispr.sh    # Pretty launcher with status
# or
./run.sh           # Simple launcher
# or
.venv/bin/python -m src.main  # Direct execution
```

### How to Use
1. Start the application (desktop icon or terminal)
2. Click in any text field where you want to type
3. Press and hold **Ctrl+Alt**
4. Speak clearly while holding the keys
5. Release the keys when done speaking
6. The transcribed text appears instantly at your cursor!

### Visual Feedback

When you press and hold the hotkey, Ubuntu's **native microphone indicator** automatically appears in your system tray (top bar). This is a built-in privacy feature of Ubuntu 22.04+ that shows whenever any application is actively recording audio.

**What you'll see:**
- 🎤 **Microphone icon appears** in the top bar = Recording is active
- **Icon disappears** when you release the hotkey = Recording stopped

This system-level indicator provides instant visual confirmation without requiring any custom implementation. It's the same indicator you see when using Zoom, Discord, or any other application that accesses your microphone, ensuring consistent user experience across all apps.

### First Run
On the first run with Parakeet, the model will be downloaded automatically (~600MB). This takes 2-5 minutes. Subsequent runs load the model from cache in ~5-10 seconds.

### Setting Up Desktop Icon
If you don't have the desktop icon yet:
```bash
./setup-launcher.sh
```

This creates:
- Desktop icon (double-click to start)
- Application menu entry (search "Wispr-Flow")

**First time using the desktop icon:**
Right-click → "Allow Launching" (Ubuntu security prompt)

## Troubleshooting

### Check if Running
```bash
pgrep -f "src.main" && echo "✅ Running" || echo "❌ Stopped"

# Or use the management script
./manage-wispr.sh status
```

### Control the Application
```bash
# Stop
pkill -f "python -m src.main"

# Start
./run.sh

# Management commands
./manage-wispr.sh start   # Start in background
./manage-wispr.sh stop    # Stop
./manage-wispr.sh status  # Check status
```

### "xdotool not found"
```bash
sudo apt install xdotool
```

### "No module named 'pyaudio'"
```bash
sudo apt install portaudio19-dev python3-pyaudio
.venv/bin/pip install pyaudio
```

### GPU Not Being Used
```bash
# Verify CUDA is available
.venv/bin/python -c "import torch; print(f'CUDA: {torch.cuda.is_available()}')"

# Check config.yaml
device: "cuda"  # Make sure it says cuda, not cpu

# Monitor GPU during transcription
watch -n 1 nvidia-smi
```

### Audio Device Issues

**Automatic Device Detection:**
The app automatically follows your system's default input device. To switch microphones:
1. Open System Settings → Sound → Input
2. Select your desired microphone (USB, Bluetooth, built-in)
3. Restart the app - it will use the new device automatically

**Supported Devices:**
- ✅ USB microphones (Blue Yeti, etc.)
- ✅ Bluetooth headsets (auto-resamples from 44100Hz to 16000Hz)
- ✅ Built-in laptop microphones
- ✅ Any device your system recognizes

**Manual Device Selection:**
If you want to lock to a specific device, list available devices:
```bash
.venv/bin/python -c "
from src.audio_recorder import AudioRecorder
recorder = AudioRecorder()
devices = recorder.list_devices()
for dev in devices:
    print(f\"Device {dev['index']}: {dev['name']}\")
recorder.close()
"
```

Then set `device_index: <number>` in `config.yaml` to lock to that device.

### Permission Issues with Microphone
Ensure your user has access to audio devices:
```bash
sudo usermod -a -G audio $USER
# Log out and log back in for changes to take effect
```

### Slow Transcription
**Current setup (Parakeet + GPU) is already optimized!**

If still slow:
- First transcription is always slower (GPU warmup)
- Check GPU is being used: `nvidia-smi`
- Ensure no other GPU-intensive apps running
- Verify config: `device: "cuda"`

To switch to faster Whisper models:
```yaml
model:
  type: "whisper"
  size: "tiny"  # or "base"
  device: "cuda"  # Keep GPU for speed
```

### X11 Required
This application requires X11. If you're using Wayland, you may need to switch to X11 or use XWayland compatibility.

## Project Structure

```
wispr-flow-clone/
├── .venv/                   # Virtual environment
├── src/
│   ├── main.py              # Application orchestrator
│   ├── config.py            # Configuration management
│   ├── hotkey_listener.py   # Global hotkey detection
│   ├── audio_recorder.py    # Audio recording
│   ├── transcriber.py       # Transcription interface
│   ├── text_injector.py     # Text injection via xdotool
│   └── models/
│       ├── whisper_model.py  # Whisper integration
│       └── parakeet_model.py # Parakeet integration
├── config.yaml              # User configuration
├── requirements.txt         # Python dependencies
├── run.sh                   # Convenience launcher
└── README.md               # This file
```

## Development

### Running in Debug Mode
Enable debug logging in `config.yaml`:
```yaml
app:
  debug: true
```

### Code Standards
- Maximum 300 lines per file
- Type hints for all functions
- Docstrings for all public methods
- All development uses `.venv`

## Performance Tips

**Current Setup (Parakeet + GPU):**
- ✅ Already optimized for best performance!
- ⚡ Near real-time transcription (0.2-0.5s for 5s audio)
- 🎯 Best accuracy available (98-99%)
- 🚀 10-25x real-time factor

**Additional Tips:**
1. **Keep app running** - First transcription is slower (GPU warmup)
2. **Good microphone** - Quality matters for accuracy
3. **Minimize background noise** - Even with excellent noise handling
4. **Short recordings** - 5-15 seconds per recording works best
5. **Monitor GPU**: `watch -n 1 nvidia-smi` to see usage

## Comparison with Wispr-Flow

| Feature | Wispr-Flow | This Clone |
|---------|-----------|------------|
| Platform | macOS | Ubuntu (Linux) |
| Processing | Cloud/Local | 100% Local |
| Privacy | Requires account | Fully private |
| Cost | $7-15/month | Free (open source) |
| Models | Proprietary | Parakeet (best accuracy) |
| Speed | Fast | Near real-time (GPU) |
| Accuracy | Excellent | 98-99% (best available) |
| Customization | Limited | Fully customizable |
| GPU Support | Yes | Yes (NVIDIA CUDA) |

## License

This is an educational project demonstrating local voice-to-text capabilities. Check individual library licenses:
- faster-whisper: MIT License
- Whisper: MIT License
- NeMo/Parakeet: Apache 2.0 License

## Contributing

This is a personal/educational project, but suggestions and improvements are welcome!

## Acknowledgments

- OpenAI Whisper team for the excellent ASR models
- NVIDIA for the Parakeet models
- SYSTRAN for faster-whisper optimization
- Wispr team for the inspiration

## Additional Documentation

- **`START_HERE.md`** - Quick start guide for new users
- **`QUICK_REFERENCE.md`** - Command cheat sheet
- **`AUTOSTART_GUIDE.md`** - Setup desktop icon and auto-start options
- **`GPU_UPGRADE_COMPLETE.md`** - GPU acceleration setup details
- **`TESTING.md`** - Testing and debugging guide
- **`CHANGELOG.md`** - Version history and changes
- **`INDEX.md`** - Complete documentation navigation

## Quick Commands

```bash
# Start with desktop icon
# → Double-click "Wispr-Flow Clone" on Desktop

# Start from terminal
./start-wispr.sh          # Pretty launcher
./run.sh                  # Simple launcher

# Management
./manage-wispr.sh status  # Check if running
./manage-wispr.sh stop    # Stop
./manage-wispr.sh start   # Start in background

# Setup
./setup-launcher.sh       # Create desktop icon
./test_parakeet.sh        # Verify GPU setup
./verify_setup.py         # Check installation
```

## Current Configuration

**Default Setup:**
- Model: NVIDIA Parakeet TDT 0.6B
- Device: CUDA (GPU acceleration)
- Accuracy: 98-99%
- Speed: Near real-time (0.2-0.5s)
- Hotkey: Ctrl+Alt

## Support

**Documentation:**
1. `START_HERE.md` - Begin here
2. `QUICK_REFERENCE.md` - Commands and tips
3. This README - Complete reference
4. `TROUBLESHOOTING` section above

**Scripts:**
- `./verify_setup.py` - Verify installation
- `./manage-wispr.sh status` - Check status
- `./test_parakeet.sh` - Test GPU setup

**For Issues:**
1. Check the Troubleshooting section above
2. Verify GPU with: `nvidia-smi`
3. Check if running: `pgrep -f "src.main"`
4. Enable debug mode: `app.debug: true` in config.yaml
5. View logs: `./manage-wispr.sh logs`
