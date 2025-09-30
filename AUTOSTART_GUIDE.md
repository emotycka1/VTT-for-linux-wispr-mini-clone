# Auto-Start Guide for Wispr-Flow Clone

## Option 1: Desktop Launcher (Recommended)

### Create a clickable launcher on your desktop:

```bash
# Copy the launcher to your desktop
cp ~/projects/wispr-flow-clone/wispr-flow.desktop ~/Desktop/

# Make it executable
chmod +x ~/Desktop/wispr-flow.desktop

# Trust the launcher (Ubuntu 22.04+)
gio set ~/Desktop/wispr-flow.desktop metadata::trusted true
```

Now you can **double-click the icon** on your desktop to start!

### Alternative: Add to Applications Menu

```bash
# Copy to applications directory
mkdir -p ~/.local/share/applications
cp ~/projects/wispr-flow-clone/wispr-flow.desktop ~/.local/share/applications/

# Update desktop database
update-desktop-database ~/.local/share/applications/
```

Now search for "Wispr-Flow" in your application launcher!

## Option 2: Convenient Start Script

We created `start-wispr.sh` which:
- Shows a nice welcome message
- Checks if already running
- Displays GPU status
- Shows instructions
- Launches the application

### Use it:

```bash
# From anywhere
~/projects/wispr-flow-clone/start-wispr.sh

# Or navigate and run
cd ~/projects/wispr-flow-clone
./start-wispr.sh
```

### Make it even easier:

Create a desktop shortcut for the start script:

```bash
cat > ~/Desktop/Start-Wispr-Flow.desktop << 'EOF'
[Desktop Entry]
Type=Application
Name=Start Wispr-Flow
Comment=Launch voice-to-text with status info
Exec=/path/to/wispr-flow-clone/start-wispr.sh
Path=/path/to/wispr-flow-clone
Icon=audio-input-microphone
Terminal=true
Categories=Utility;
EOF

chmod +x ~/Desktop/Start-Wispr-Flow.desktop
gio set ~/Desktop/Start-Wispr-Flow.desktop metadata::trusted true
```

## Option 3: Auto-Start on Login

### Method A: GNOME Startup Applications (GUI)

1. Open "Startup Applications"
   ```bash
   gnome-session-properties
   ```

2. Click "Add"

3. Fill in:
   - **Name**: Wispr-Flow Voice-to-Text
   - **Command**: `/path/to/wispr-flow-clone/start-wispr.sh`
   - **Comment**: Voice-to-text transcription

4. Click "Add" and close

### Method B: Systemd User Service (Advanced)

```bash
# Create service file
mkdir -p ~/.config/systemd/user
cat > ~/.config/systemd/user/wispr-flow.service << 'EOF'
[Unit]
Description=Wispr-Flow Voice-to-Text
After=graphical-session.target

[Service]
Type=simple
WorkingDirectory=/path/to/wispr-flow-clone
ExecStart=/path/to/wispr-flow-clone/.venv/bin/python -m src.main
Restart=on-failure
RestartSec=5

[Install]
WantedBy=default.target
EOF

# Enable and start
systemctl --user enable wispr-flow.service
systemctl --user start wispr-flow.service

# Check status
systemctl --user status wispr-flow.service
```

To stop:
```bash
systemctl --user stop wispr-flow.service
```

To disable auto-start:
```bash
systemctl --user disable wispr-flow.service
```

### Method C: Autostart Desktop Entry

```bash
# Create autostart directory
mkdir -p ~/.config/autostart

# Copy the launcher
cp ~/projects/wispr-flow-clone/wispr-flow.desktop ~/.config/autostart/

# Optionally hide the terminal window on startup
sed -i 's/Terminal=true/Terminal=false/' ~/.config/autostart/wispr-flow.desktop
```

## Option 4: Keyboard Shortcut

Create a custom keyboard shortcut to launch with one key combination:

1. **Open Settings** → **Keyboard** → **View and Customize Shortcuts** → **Custom Shortcuts**

2. **Click** **+ Add Shortcut** (or **+ Add**)

3. **Fill in the form:**
   - **Name:** `Start Wispr-Flow`
   - **Command:** `/path/to/wispr-flow-clone/start-wispr.sh`
   - *(Replace `/path/to/` with your actual installation path)*

4. **Click "Set Shortcut"** button

5. **When the dialog appears waiting for input:**
   - Press the **Super key** (Windows logo key ⊞) + **W** together
   - Or choose your own combo like **Ctrl+Alt+W**
   - The keys you press will be captured as your shortcut

6. **Click "Add"** to save

**Now press your chosen keys (Super+W) anytime to launch the app!**

*The Super key is the Windows logo key (⊞) on your keyboard, also called the Meta key*

## Checking if Running

```bash
# Check if running
pgrep -f "python -m src.main" && echo "✓ Running" || echo "✗ Not running"

# See full process
ps aux | grep "src.main" | grep -v grep

# Stop it
pkill -f "python -m src.main"
```

## Monitoring in Background

If running in background, monitor with:

```bash
# View logs (if using systemd)
journalctl --user -u wispr-flow.service -f

# Or check GPU usage
watch -n 1 nvidia-smi
```

## Recommendations

### For Daily Use:
**→ Use the Desktop Launcher** (Option 1)
- Easy to start when needed
- Clean and simple
- Shows in terminal so you can see status

### For Always-On:
**→ Use Startup Applications** (Option 3A)
- Starts automatically on login
- Runs in background
- Always ready

### For Quick Access:
**→ Use Keyboard Shortcut** (Option 4)
- Press Super+W to launch
- Fast and convenient
- No desktop clutter

## Troubleshooting

### "Already running" message
```bash
# Stop existing instance
pkill -f "python -m src.main"

# Then start again
./start-wispr.sh
```

### Launcher doesn't work
```bash
# Make sure it's executable
chmod +x ~/Desktop/wispr-flow.desktop

# Trust it
gio set ~/Desktop/wispr-flow.desktop metadata::trusted true

# Or right-click → "Allow Launching"
```

### Auto-start not working
```bash
# Check if service is enabled (if using systemd)
systemctl --user is-enabled wispr-flow.service

# Check logs
journalctl --user -u wispr-flow.service --since today
```

## What I Recommend

**Best setup for you:**

1. ✅ **Create desktop launcher** - double-click to start
2. ✅ **Add keyboard shortcut** (Super+W) - quick access
3. ⚠️ **Don't auto-start on boot** - saves resources when not needed

This way:
- Start it when you need it (double-click or Super+W)
- GPU isn't active all the time (saves power)
- No background resource usage
- Clean and simple

Want me to set up the desktop launcher and keyboard shortcut for you?
