# Quick Start Guide - Wispr-Flow Clone

Get up and running in 5 minutes!

## Prerequisites

You need Ubuntu 20.04+ with X11. This application does **not** work on headless servers without a display.

## Step 1: Install System Dependencies

```bash
sudo apt update
sudo apt install -y xdotool portaudio19-dev python3-pyaudio python3-venv
```

## Step 2: Setup Project

If you need to set up the project:

```bash
# Navigate to project
cd ~/projects/wispr-flow-clone

# Virtual environment is already created
# Dependencies are already installed
```

## Step 3: Verify Setup

Run the verification script:

```bash
./verify_setup.py
```

You should see all checks pass with ✓ marks.

## Step 4: Run the Application

```bash
./run.sh
```

Or directly:

```bash
.venv/bin/python -m src.main
```

## Step 5: Use It!

1. **The application is now listening for your hotkey**
2. **Press and HOLD Ctrl+Alt** (both keys together)
3. **Speak clearly** while holding the keys
4. **Release the keys** when done speaking
5. **Your speech will be transcribed** where your cursor is

## Example Usage

1. Open any text editor (gedit, vim, VS Code, etc.)
2. Click in a text field
3. Hold Ctrl+Alt
4. Say: "Hello world, this is a test of the voice transcription system"
5. Release Ctrl+Alt
6. The text appears where your cursor was!

## First Run Notes

### Model Download
On the first run, Whisper will download the model (200MB-3GB depending on size). This is one-time and takes a few minutes.

### Audio Warnings
You may see ALSA warnings like:
```
ALSA lib pcm_dsnoop.c:567:(snd_pcm_dsnoop_open) unable to open slave
```

These are normal and can be ignored. The application will still work.

## Configuration

Edit `config.yaml` to customize:

### Change Hotkey
```yaml
hotkey:
  modifiers: ["ctrl", "shift"]  # Use Ctrl+Shift instead
  key: ""
```

### Use Different Model Size
```yaml
model:
  size: "small"  # Options: tiny, base, small, medium, large-v3
```

### Enable GPU (if you have NVIDIA GPU)
```yaml
model:
  device: "cuda"  # Much faster!
```

## Troubleshooting

### "No module named 'faster_whisper'"
```bash
cd ~/projects/wispr-flow-clone
.venv/bin/pip install -r requirements.txt
```

### "xdotool not found"
```bash
sudo apt install xdotool
```

### Hotkey Not Working
- Ensure you're on X11 (not Wayland)
- Check if another application is using the same hotkey
- Try a different key combination in `config.yaml`

### Slow Transcription
- Use a smaller model: `model.size: "tiny"` or `"base"`
- Enable GPU if available: `model.device: "cuda"`

### No Audio Input
```bash
# List audio devices
.venv/bin/python verify_setup.py
```

Then set the device index in `config.yaml`:
```yaml
audio:
  device_index: 4  # Use the device number from the list
```

## Stopping the Application

Press **Ctrl+C** in the terminal to stop.

## Tips for Best Results

1. **Speak clearly** and at a normal pace
2. **Use a good microphone** for better accuracy
3. **Minimize background noise**
4. **Wait a moment** after releasing the keys for transcription
5. **Start with short phrases** to test, then try longer sentences

## What's Happening Behind the Scenes

1. You press Ctrl+Alt → Audio recording starts
2. You speak → Audio is captured in memory
3. You release keys → Recording stops
4. Audio is transcribed using Whisper (locally, no internet needed!)
5. Text is injected at cursor position using xdotool

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Adjust `config.yaml` for your preferences
- Try different model sizes to balance speed and accuracy
- Consider enabling GPU acceleration for real-time performance

## Privacy Note

**Everything runs locally on your machine.** Your voice never leaves your computer. No internet connection required (except for the initial model download).

---

**Enjoy your local voice-to-text system!** 🎙️✨
