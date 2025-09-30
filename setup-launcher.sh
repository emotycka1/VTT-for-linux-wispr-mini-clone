#!/bin/bash
# Quick setup script for Wispr-Flow launchers

echo "╔════════════════════════════════════════════╗"
echo "║   Wispr-Flow Clone Launcher Setup         ║"
echo "╚════════════════════════════════════════════╝"
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "Setting up easy launchers for Wispr-Flow..."
echo ""

# 1. Desktop launcher
echo "1️⃣  Creating desktop launcher..."
if [ -d "$HOME/Desktop" ]; then
    cp wispr-flow.desktop "$HOME/Desktop/"
    chmod +x "$HOME/Desktop/wispr-flow.desktop"
    
    # Try to trust it (Ubuntu 22.04+)
    if command -v gio &> /dev/null; then
        gio set "$HOME/Desktop/wispr-flow.desktop" metadata::trusted true 2>/dev/null
    fi
    
    echo "   ✓ Desktop launcher created: ~/Desktop/wispr-flow.desktop"
    echo "   → Double-click to start!"
else
    echo "   ⚠️  Desktop folder not found, skipping..."
fi
echo ""

# 2. Applications menu
echo "2️⃣  Adding to Applications menu..."
mkdir -p "$HOME/.local/share/applications"
cp wispr-flow.desktop "$HOME/.local/share/applications/"

if command -v update-desktop-database &> /dev/null; then
    update-desktop-database "$HOME/.local/share/applications/" 2>/dev/null
    echo "   ✓ Added to Applications menu"
    echo "   → Search for 'Wispr-Flow' in app launcher!"
else
    echo "   ✓ Copied to Applications (may need logout to appear)"
fi
echo ""

# 3. Optional: Startup Applications
echo "3️⃣  Auto-start on login? (optional)"
echo "   This will start Wispr-Flow automatically when you log in."
read -p "   Add to startup? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    mkdir -p "$HOME/.config/autostart"
    cp wispr-flow.desktop "$HOME/.config/autostart/"
    echo "   ✓ Added to startup applications"
    echo "   → Will start automatically on next login"
else
    echo "   ⊘ Skipped (you can start it manually when needed)"
fi
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Setup complete!"
echo ""
echo "How to start Wispr-Flow:"
echo ""
echo "  1. Double-click icon on Desktop"
echo "  2. Search 'Wispr-Flow' in app launcher"
echo "  3. Run: ./start-wispr.sh"
echo "  4. Run: ./run.sh"
echo ""
echo "How to set up keyboard shortcut (optional):"
echo "  1. Open Settings → Keyboard → Keyboard Shortcuts"
echo "  2. Add custom shortcut"
echo "  3. Command: $SCRIPT_DIR/start-wispr.sh"
echo "  4. Assign key (e.g., Super+W)"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
