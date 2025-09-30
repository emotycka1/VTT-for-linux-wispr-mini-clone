"""Main application orchestrator for Wispr-Flow Clone."""

import logging
import sys
import signal
from pathlib import Path

from .config import Config
from .hotkey_listener import HotkeyListener
from .audio_recorder import AudioRecorder
from .transcriber import Transcriber
from .text_injector import TextInjector


class WisprFlowApp:
    """Main application class."""
    
    def __init__(self, config_path: Path = None):
        """Initialize application.
        
        Args:
            config_path: Path to configuration file
        """
        # Load configuration
        self.config = Config(config_path)
        
        # Setup logging
        self._setup_logging()
        
        self.logger = logging.getLogger(__name__)
        self.logger.info("Starting Wispr-Flow Clone")
        
        # Initialize components
        self.audio_recorder = AudioRecorder(
            sample_rate=self.config.audio.sample_rate,
            channels=self.config.audio.channels,
            chunk_size=self.config.audio.chunk_size,
            device_index=self.config.audio.device_index
        )
        
        self.text_injector = TextInjector()
        
        # Initialize transcriber (may take time to load model)
        self.logger.info("Loading transcription model...")
        self.transcriber = Transcriber(self.config)
        self.logger.info("Transcription model loaded")
        
        # Initialize hotkey listener
        self.hotkey_listener = HotkeyListener(
            modifiers=self.config.hotkey.modifiers,
            key=self.config.hotkey.key,
            on_press=self._on_hotkey_press,
            on_release=self._on_hotkey_release
        )
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        self.is_running = False
    
    def _setup_logging(self) -> None:
        """Setup logging configuration."""
        level = logging.DEBUG if self.config.app.debug else logging.INFO
        
        logging.basicConfig(
            level=level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(sys.stdout)
            ]
        )
    
    def _on_hotkey_press(self) -> None:
        """Handle hotkey press event."""
        self.logger.info("Hotkey pressed - Starting recording")
        try:
            self.audio_recorder.start_recording()
        except Exception as e:
            self.logger.error(f"Failed to start recording: {e}")
    
    def _on_hotkey_release(self) -> None:
        """Handle hotkey release event."""
        self.logger.info("Hotkey released - Stopping recording")
        
        try:
            # Stop recording and get audio data
            audio_data = self.audio_recorder.stop_recording()
            
            if audio_data is None:
                self.logger.warning("No audio data to transcribe")
                return
            
            # Check minimum duration
            duration = self.audio_recorder.get_audio_duration(audio_data)
            self.logger.info(f"Recorded audio duration: {duration:.2f}s")
            
            if duration < self.config.app.min_audio_length:
                self.logger.info(
                    f"Audio too short ({duration:.2f}s < "
                    f"{self.config.app.min_audio_length}s), ignoring"
                )
                return
            
            # Transcribe (pass actual recorded sample rate for proper resampling)
            self.logger.info("Transcribing audio...")
            text = self.transcriber.transcribe(
                audio_data,
                self.audio_recorder.actual_sample_rate
            )
            
            if not text:
                self.logger.warning("Transcription returned empty text")
                return
            
            self.logger.info(f"Transcription: {text}")
            
            # Inject text
            self.logger.info("Injecting text...")
            success = self.text_injector.inject_text(text)
            
            if success:
                self.logger.info("Text injected successfully")
            else:
                self.logger.error("Failed to inject text")
        
        except Exception as e:
            self.logger.error(f"Error processing recording: {e}", exc_info=True)
    
    def _signal_handler(self, signum, frame) -> None:
        """Handle shutdown signals.
        
        Args:
            signum: Signal number
            frame: Current stack frame
        """
        self.logger.info(f"Received signal {signum}, shutting down...")
        self.stop()
        sys.exit(0)
    
    def start(self) -> None:
        """Start the application."""
        self.logger.info("Application starting...")
        self.logger.info(
            f"Press {'+'.join(self.config.hotkey.modifiers)} "
            "and hold to record, release to transcribe"
        )
        
        self.is_running = True
        self.hotkey_listener.start()
        
        # Keep main thread alive
        try:
            while self.is_running:
                import time
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.logger.info("Interrupted by user")
            self.stop()
    
    def stop(self) -> None:
        """Stop the application."""
        self.logger.info("Stopping application...")
        self.is_running = False
        
        # Stop components
        self.hotkey_listener.stop()
        self.audio_recorder.close()
        
        self.logger.info("Application stopped")


def main():
    """Main entry point."""
    try:
        app = WisprFlowApp()
        app.start()
    except Exception as e:
        logging.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
