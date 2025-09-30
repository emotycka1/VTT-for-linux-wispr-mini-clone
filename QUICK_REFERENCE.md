# Quick Reference Card

## ✅ Your App is Running in Background!

### Check Status
```bash
# Is it running?
pgrep -f "python -m src.main" && echo "✅ Running" || echo "❌ Stopped"

# Or use the manager
./manage-wispr.sh status
```

### Control Commands

```bash
# Start
./start-wispr.sh          # Interactive with status
./run.sh                  # Simple start

# Stop
pkill -f "python -m src.main"

# Restart
pkill -f "python -m src.main" && sleep 2 && ./run.sh

# Or use the manager
./manage-wispr.sh stop
./manage-wispr.sh start
./manage-wispr.sh restart
```

### How to Use (While Running)

1. **Click in any text field** (terminal, browser, editor, etc.)
2. **Press and HOLD Ctrl+Alt**
3. **Speak clearly**
4. **Release keys**
5. **Text appears!** ✨

### Quick Tips

**Recording:**
- Hold keys for entire sentence
- Speak naturally at normal pace
- Don't rush or go too slow

**Best For:**
- Emails and messages
- Documentation
- Notes and journaling
- Social media posts
- Comments (in code or documents)

**Works In:**
- Terminal ✅
- VS Code ✅
- Browsers ✅
- Text editors ✅
- Any text input field ✅

### Current Setup

**Model**: NVIDIA Parakeet TDT 0.6B  
**Device**: RTX 4090 GPU  
**Accuracy**: 98-99% (best possible!)  
**Speed**: Near real-time (0.2-0.5s for 5s audio)  
**Hotkey**: Ctrl+Alt  

### Monitoring

```bash
# Watch GPU usage
watch -n 1 nvidia-smi

# See what it's doing
tail -f /tmp/wispr-flow.log  # If running in background

# Check performance
./test_parakeet.sh
```

### Configuration

**File**: `config.yaml`

**Quick tweaks:**
```yaml
# Change hotkey
hotkey:
  modifiers: ["ctrl", "shift"]  # Use Ctrl+Shift instead

# Adjust sensitivity
app:
  min_audio_length: 0.5  # Ignore very short recordings
```

### Troubleshooting

**Problem**: Not transcribing  
**Solution**: Check if running: `pgrep -f "src.main"`

**Problem**: Wrong text  
**Solution**: Already using best model! Speak more clearly.

**Problem**: Too slow  
**Solution**: Already on GPU! First one is slower (warmup).

**Problem**: Hotkey not working  
**Solution**: Make sure no other app uses Ctrl+Alt

### Files You'll Use

```
./run.sh              → Simple start
./start-wispr.sh      → Nice launcher with status
./manage-wispr.sh     → Full management (start/stop/status)
./test_parakeet.sh    → Verify GPU setup
./setup-launcher.sh   → Create desktop icons
config.yaml           → Settings
```

### Startup Options

**Desktop Icon**: Run `./setup-launcher.sh`  
**Keyboard Shortcut**: Settings → Keyboard → Custom Shortcuts  
**Auto-start**: See `AUTOSTART_GUIDE.md`  

## One-Line Commands

```bash
# Most common
./run.sh                                    # Start
pkill -f "python -m src.main"              # Stop
./manage-wispr.sh status                   # Check status

# Useful
./test_parakeet.sh                         # Verify setup
nvidia-smi                                  # GPU status
./setup-launcher.sh                        # Create desktop icon
```

## Remember

- **Ctrl+Alt** = Your magic keys! 🎤
- **Hold to record** = Capture your voice
- **Release to transcribe** = Get instant text
- **Works everywhere** = Any text field

---

**You're all set! Press Ctrl+Alt and start speaking!** 🚀
