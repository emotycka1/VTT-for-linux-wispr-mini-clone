#!/bin/bash
# Convenient launcher for Wispr-Flow Clone
# Double-click this file or run from terminal

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Function to check if already running
check_if_running() {
    if pgrep -f "python -m src.main" > /dev/null; then
        echo "⚠️  Wispr-Flow is already running!"
        echo ""
        read -p "Do you want to restart it? (y/N) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo "Stopping existing instance..."
            pkill -f "python -m src.main"
            sleep 2
        else
            echo "Keeping existing instance. Exiting..."
            sleep 2
            exit 0
        fi
    fi
}

# Welcome message
clear
echo "╔════════════════════════════════════════════╗"
echo "║     Wispr-Flow Clone - Voice-to-Text      ║"
echo "║         GPU Accelerated Edition 🚀         ║"
echo "╚════════════════════════════════════════════╝"
echo ""
echo "Starting application..."
echo ""

# Check if already running
check_if_running

# Check virtual environment
if [ ! -d ".venv" ]; then
    echo "❌ Error: Virtual environment not found!"
    echo "   Please run setup first."
    read -p "Press Enter to exit..."
    exit 1
fi

# Quick GPU check
echo "🔍 GPU Status:"
if nvidia-smi --query-gpu=name,temperature.gpu,memory.used,memory.total --format=csv,noheader 2>/dev/null; then
    echo ""
else
    echo "   ⚠️  Warning: Could not detect NVIDIA GPU"
    echo ""
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📝 Instructions:"
echo "   • Press Ctrl+Alt and HOLD to record"
echo "   • Speak while holding the keys"
echo "   • Release to transcribe"
echo "   • Press Ctrl+C in this window to stop"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Small delay to read messages
sleep 2

# Run the application
./run.sh

# If it exits, wait before closing
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Application stopped."
read -p "Press Enter to close..."
