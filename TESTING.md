# Testing Guide

This guide explains how to test the Wispr-Flow Clone application without actually running the full hotkey listener (which requires X11 and a graphical environment).

## Component Testing

You can test individual components separately:

### 1. Configuration Loading

Test if configuration loads correctly:

```bash
.venv/bin/python -c "
from src.config import Config
config = Config()
print(f'Model: {config.model.type} ({config.model.size})')
print(f'Device: {config.model.device}')
print(f'Hotkey: {\" + \".join(config.hotkey.modifiers)}')
print(f'Sample rate: {config.audio.sample_rate}Hz')
"
```

### 2. Text Injector (X11 Required)

Test text injection (requires X11 and xdotool):

```bash
.venv/bin/python -c "
from src.text_injector import TextInjector
injector = TextInjector()
print('Text injector initialized successfully')
print(f'Active window: {injector.get_active_window()}')
# Note: Actually injecting text requires a focused text field
"
```

### 3. Audio Recorder

Test audio device listing (doesn't require microphone):

```bash
.venv/bin/python -c "
from src.audio_recorder import AudioRecorder
recorder = AudioRecorder()
devices = recorder.list_devices()
print(f'Found {len(devices)} audio input devices:')
for dev in devices:
    print(f\"  Device {dev['index']}: {dev['name']}\")
recorder.close()
"
```

### 4. Whisper Model Loading

Test if Whisper model loads (will download on first run):

```bash
.venv/bin/python -c "
from src.models.whisper_model import WhisperTranscriber
print('Loading Whisper model...')
model = WhisperTranscriber(model_size='tiny', device='cpu', language='en')
print('Model loaded successfully!')
print(f'Ready: {model.is_ready()}')
"
```

### 5. Full Transcription Test

Test transcription with a sample audio file (create one first):

```bash
# First, create a test recording (requires microphone)
.venv/bin/python << 'EOF'
from src.audio_recorder import AudioRecorder
import numpy as np
import time

recorder = AudioRecorder(sample_rate=16000)
print("Recording for 3 seconds... Speak now!")
recorder.start_recording()
time.sleep(3)
audio_data = recorder.stop_recording()
recorder.close()

if audio_data is not None:
    np.save('test_audio.npy', audio_data)
    print(f"Saved {len(audio_data)} samples")
else:
    print("No audio recorded")
EOF

# Then transcribe it
.venv/bin/python << 'EOF'
import numpy as np
from src.models.whisper_model import WhisperTranscriber

audio_data = np.load('test_audio.npy')
print("Transcribing audio...")
model = WhisperTranscriber(model_size='tiny', device='cpu', language='en')
text = model.transcribe(audio_data, sample_rate=16000)
print(f"Transcription: {text}")
EOF
```

## Integration Testing

### Test Without Hotkey Listener

You can test the full flow without the hotkey listener by creating a simple test script:

```bash
cat > test_transcription.py << 'EOF'
#!/usr/bin/env python3
"""Test transcription without hotkey listener."""

import time
import numpy as np
from src.config import Config
from src.audio_recorder import AudioRecorder
from src.transcriber import Transcriber
from src.text_injector import TextInjector

print("Loading configuration...")
config = Config()

print("Initializing components...")
recorder = AudioRecorder(
    sample_rate=config.audio.sample_rate,
    channels=config.audio.channels
)
transcriber = Transcriber(config)
injector = TextInjector()

print("\nRecording for 5 seconds... Speak now!")
recorder.start_recording()
time.sleep(5)
audio_data = recorder.stop_recording()

if audio_data is None:
    print("No audio recorded!")
    exit(1)

duration = recorder.get_audio_duration(audio_data)
print(f"Recorded {duration:.2f} seconds of audio")

print("Transcribing...")
text = transcriber.transcribe(audio_data, config.audio.sample_rate)
print(f"\nTranscription: {text}")

print("\nInjecting text in 3 seconds... Click in a text field!")
time.sleep(3)
success = injector.inject_text(text)

if success:
    print("Text injected successfully!")
else:
    print("Failed to inject text")

recorder.close()
EOF

chmod +x test_transcription.py
.venv/bin/python -m src.main  # Or use the test script
```

## Unit Testing Framework

For proper unit tests, create a `tests/` directory:

```bash
mkdir -p tests
```

### Example: Test Configuration

```bash
cat > tests/test_config.py << 'EOF'
"""Unit tests for configuration."""

import unittest
from pathlib import Path
from src.config import Config

class TestConfig(unittest.TestCase):
    def test_load_config(self):
        """Test loading configuration."""
        config = Config()
        self.assertIsNotNone(config.model)
        self.assertIsNotNone(config.hotkey)
        self.assertIsNotNone(config.audio)
    
    def test_default_values(self):
        """Test default configuration values."""
        config = Config()
        self.assertEqual(config.model.type, 'whisper')
        self.assertEqual(config.audio.sample_rate, 16000)
        self.assertIsInstance(config.hotkey.modifiers, list)

if __name__ == '__main__':
    unittest.main()
EOF

.venv/bin/python -m pytest tests/test_config.py -v
# Or use unittest
.venv/bin/python tests/test_config.py
```

## Performance Testing

### Model Loading Time

```bash
.venv/bin/python -c "
import time
from src.models.whisper_model import WhisperTranscriber

start = time.time()
model = WhisperTranscriber(model_size='base', device='cpu', language='en')
load_time = time.time() - start

print(f'Model loading time: {load_time:.2f} seconds')
"
```

### Transcription Speed

```bash
.venv/bin/python -c "
import time
import numpy as np
from src.models.whisper_model import WhisperTranscriber

# Generate 10 seconds of dummy audio
sample_rate = 16000
audio_data = np.random.randint(-32768, 32767, sample_rate * 10, dtype=np.int16)

model = WhisperTranscriber(model_size='tiny', device='cpu', language='en')

start = time.time()
text = model.transcribe(audio_data, sample_rate)
transcribe_time = time.time() - start

print(f'Transcription time: {transcribe_time:.2f} seconds')
print(f'Real-time factor: {10.0 / transcribe_time:.2f}x')
"
```

## Debugging Tips

### Enable Debug Logging

Edit `config.yaml`:

```yaml
app:
  debug: true
```

Then run:

```bash
./run.sh 2>&1 | tee debug.log
```

### Check Python Path

```bash
.venv/bin/python -c "import sys; print('\n'.join(sys.path))"
```

### Verify Imports

```bash
.venv/bin/python -c "
import src.config
import src.audio_recorder
import src.hotkey_listener
import src.transcriber
import src.text_injector
import src.models.whisper_model
print('All imports successful!')
"
```

## Continuous Integration

For automated testing in CI/CD, you can run:

```bash
# Lint
.venv/bin/python -m pylint src/

# Type checking
.venv/bin/python -m mypy src/

# Unit tests
.venv/bin/python -m pytest tests/
```

## Known Issues

1. **ALSA Warnings**: Normal in headless environments, can be ignored
2. **X11 Required**: Text injection and hotkey detection require X11
3. **First Run Slow**: Model download happens on first run
4. **Audio Permissions**: May need to add user to audio group

## Clean Up Test Files

```bash
rm -f test_audio.npy test_transcription.py debug.log
```
