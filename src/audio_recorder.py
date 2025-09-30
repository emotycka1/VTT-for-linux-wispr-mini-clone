"""Audio recording module using PyAudio."""

import pyaudio
import numpy as np
import logging
from typing import Optional
from threading import Lock


logger = logging.getLogger(__name__)


class AudioRecorder:
    """Records audio from microphone to memory buffer."""
    
    def __init__(
        self,
        sample_rate: int = 16000,
        channels: int = 1,
        chunk_size: int = 1024,
        device_index: Optional[int] = None
    ):
        """Initialize audio recorder.
        
        Args:
            sample_rate: Sample rate in Hz
            channels: Number of audio channels
            chunk_size: Size of audio chunks
            device_index: Microphone device index (None for default)
        """
        self.sample_rate = sample_rate
        self.channels = channels
        self.chunk_size = chunk_size
        self.device_index = device_index
        
        self.audio = pyaudio.PyAudio()
        self.stream: Optional[pyaudio.Stream] = None
        self.is_recording = False
        self.audio_buffer: list[np.ndarray] = []
        self._lock = Lock()
        
        logger.info(
            f"AudioRecorder initialized: {sample_rate}Hz, "
            f"{channels} channel(s), chunk={chunk_size}"
        )
    
    def start_recording(self) -> None:
        """Start recording audio."""
        with self._lock:
            if self.is_recording:
                logger.warning("Recording already in progress")
                return
            
            self.audio_buffer = []
            self.is_recording = True
            
            try:
                self.stream = self.audio.open(
                    format=pyaudio.paInt16,
                    channels=self.channels,
                    rate=self.sample_rate,
                    input=True,
                    input_device_index=self.device_index,
                    frames_per_buffer=self.chunk_size,
                    stream_callback=self._audio_callback
                )
                self.stream.start_stream()
                logger.info("Recording started")
            except Exception as e:
                self.is_recording = False
                logger.error(f"Failed to start recording: {e}")
                raise
    
    def stop_recording(self) -> Optional[np.ndarray]:
        """Stop recording and return audio data.
        
        Returns:
            Audio data as numpy array, or None if no data recorded
        """
        with self._lock:
            if not self.is_recording:
                logger.warning("Not currently recording")
                return None
            
            self.is_recording = False
            
            if self.stream:
                try:
                    self.stream.stop_stream()
                    self.stream.close()
                except Exception as e:
                    logger.error(f"Error stopping stream: {e}")
                finally:
                    self.stream = None
            
            if not self.audio_buffer:
                logger.warning("No audio data recorded")
                return None
            
            # Concatenate all chunks
            audio_data = np.concatenate(self.audio_buffer, axis=0)
            logger.info(f"Recording stopped: {len(audio_data)} samples")
            
            return audio_data
    
    def _audio_callback(self, in_data, frame_count, time_info, status):
        """Callback for audio stream."""
        if status:
            logger.warning(f"Audio callback status: {status}")
        
        if self.is_recording:
            # Convert bytes to numpy array
            audio_chunk = np.frombuffer(in_data, dtype=np.int16)
            self.audio_buffer.append(audio_chunk)
        
        return (in_data, pyaudio.paContinue)
    
    def get_audio_duration(self, audio_data: np.ndarray) -> float:
        """Get duration of audio data in seconds.
        
        Args:
            audio_data: Audio data array
            
        Returns:
            Duration in seconds
        """
        return len(audio_data) / self.sample_rate
    
    def list_devices(self) -> list[dict]:
        """List available audio input devices.
        
        Returns:
            List of device information dictionaries
        """
        devices = []
        for i in range(self.audio.get_device_count()):
            try:
                info = self.audio.get_device_info_by_index(i)
                if info['maxInputChannels'] > 0:
                    devices.append({
                        'index': i,
                        'name': info['name'],
                        'channels': info['maxInputChannels'],
                        'sample_rate': int(info['defaultSampleRate'])
                    })
            except Exception as e:
                logger.warning(f"Error getting device {i} info: {e}")
        
        return devices
    
    def close(self) -> None:
        """Clean up resources."""
        if self.is_recording:
            self.stop_recording()
        
        if self.audio:
            self.audio.terminate()
            logger.info("AudioRecorder closed")
