#!/usr/bin/env python3
"""Verification script to check if all dependencies are properly installed."""

import sys
import subprocess
from pathlib import Path

# Add project root to Python path for imports
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def check_system_dependency(command, package_name):
    """Check if a system command is available."""
    try:
        result = subprocess.run(
            ['which', command],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
        print(f"✓ {command} is installed: {result.stdout.decode().strip()}")
        return True
    except subprocess.CalledProcessError:
        print(f"✗ {command} is NOT installed. Install with: sudo apt install {package_name}")
        return False


def check_python_module(module_name):
    """Check if a Python module can be imported."""
    try:
        __import__(module_name)
        print(f"✓ Python module '{module_name}' is installed")
        return True
    except ImportError as e:
        print(f"✗ Python module '{module_name}' is NOT installed: {e}")
        return False


def main():
    """Run all verification checks."""
    print("=" * 60)
    print("Wispr-Flow Clone - Setup Verification")
    print("=" * 60)
    
    all_ok = True
    
    print("\n1. Checking system dependencies...")
    print("-" * 60)
    all_ok &= check_system_dependency('xdotool', 'xdotool')
    
    print("\n2. Checking Python modules...")
    print("-" * 60)
    modules = [
        'pynput',
        'pyaudio',
        'faster_whisper',
        'yaml',
        'numpy'
    ]
    
    for module in modules:
        all_ok &= check_python_module(module)
    
    print("\n3. Checking audio devices...")
    print("-" * 60)
    try:
        import pyaudio
        p = pyaudio.PyAudio()
        device_count = p.get_device_count()
        input_devices = 0
        
        for i in range(device_count):
            info = p.get_device_info_by_index(i)
            if info['maxInputChannels'] > 0:
                input_devices += 1
                print(f"  Device {i}: {info['name']} ({info['maxInputChannels']} channels)")
        
        p.terminate()
        
        if input_devices > 0:
            print(f"✓ Found {input_devices} audio input device(s)")
        else:
            print("✗ No audio input devices found")
            all_ok = False
    except Exception as e:
        print(f"✗ Error checking audio devices: {e}")
        all_ok = False
    
    print("\n" + "=" * 60)
    if all_ok:
        print("✓ All checks passed! Ready to run Wispr-Flow Clone.")
        print("\nStart the application with:")
        print("  ./run.sh")
        print("  or")
        print("  .venv/bin/python src/main.py")
    else:
        print("✗ Some checks failed. Please install missing dependencies.")
        print("\nRefer to README.md for installation instructions.")
    print("=" * 60)
    
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
