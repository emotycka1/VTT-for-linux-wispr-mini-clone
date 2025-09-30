"""Whisper model implementation using faster-whisper."""

import logging
import numpy as np
from typing import Optional
from faster_whisper import WhisperModel


logger = logging.getLogger(__name__)


class WhisperTranscriber:
    """Transcriber using faster-whisper."""
    
    def __init__(
        self,
        model_size: str = "base",
        device: str = "cpu",
        language: str = "en"
    ):
        """Initialize Whisper transcriber.
        
        Args:
            model_size: Model size (tiny, base, small, medium, large-v2, large-v3)
            device: Device to use (cpu, cuda)
            language: Language code (en, es, fr, etc.) or 'auto' for detection
        """
        self.model_size = model_size
        self.device = device
        self.language = None if language == "auto" else language
        self.model: Optional[WhisperModel] = None
        
        logger.info(
            f"Initializing Whisper model: size={model_size}, "
            f"device={device}, language={language}"
        )
        self._load_model()
    
    def _load_model(self) -> None:
        """Load the Whisper model."""
        try:
            # Determine compute type based on device
            if self.device == "cuda":
                compute_type = "float16"
            else:
                compute_type = "int8"
            
            self.model = WhisperModel(
                self.model_size,
                device=self.device,
                compute_type=compute_type,
                download_root=None  # Use default cache
            )
            logger.info("Whisper model loaded successfully")
        
        except Exception as e:
            logger.error(f"Failed to load Whisper model: {e}")
            raise
    
    def transcribe(
        self,
        audio_data: np.ndarray,
        sample_rate: int = 16000
    ) -> str:
        """Transcribe audio data.
        
        Args:
            audio_data: Audio data as numpy array (int16)
            sample_rate: Sample rate of audio data
            
        Returns:
            Transcribed text
        """
        if self.model is None:
            raise RuntimeError("Model not loaded")
        
        if audio_data is None or len(audio_data) == 0:
            logger.warning("Empty audio data provided")
            return ""
        
        try:
            # Convert int16 to float32 normalized to [-1, 1]
            audio_float = audio_data.astype(np.float32) / 32768.0
            
            # Transcribe
            segments, info = self.model.transcribe(
                audio_float,
                language=self.language,
                beam_size=5,
                vad_filter=True,  # Voice activity detection
                vad_parameters=dict(
                    min_silence_duration_ms=500
                )
            )
            
            # Collect all segments
            text_parts = []
            for segment in segments:
                text_parts.append(segment.text)
            
            full_text = " ".join(text_parts).strip()
            
            # Log detected language if auto-detection
            if self.language is None:
                logger.info(f"Detected language: {info.language}")
            
            logger.info(f"Transcription complete: {len(full_text)} characters")
            return full_text
        
        except Exception as e:
            logger.error(f"Transcription failed: {e}")
            raise
    
    def is_ready(self) -> bool:
        """Check if model is ready.
        
        Returns:
            True if model is loaded
        """
        return self.model is not None
    
    def get_supported_languages(self) -> list[str]:
        """Get list of supported language codes.
        
        Returns:
            List of language codes
        """
        # Common languages supported by Whisper
        return [
            "en", "es", "fr", "de", "it", "pt", "nl", "pl", "ru",
            "zh", "ja", "ko", "ar", "hi", "tr", "vi", "id", "th"
        ]
