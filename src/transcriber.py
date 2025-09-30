"""Transcription interface that delegates to specific model implementations."""

import logging
import numpy as np
from typing import Optional
from .config import Config


logger = logging.getLogger(__name__)


class Transcriber:
    """Main transcription interface."""
    
    def __init__(self, config: Config):
        """Initialize transcriber with configuration.
        
        Args:
            config: Application configuration
        """
        self.config = config
        self.model: Optional[any] = None
        self._initialize_model()
    
    def _initialize_model(self) -> None:
        """Initialize the appropriate model based on configuration."""
        model_type = self.config.model.type.lower()
        
        logger.info(f"Initializing transcription model: {model_type}")
        
        if model_type == "whisper":
            from .models.whisper_model import WhisperTranscriber
            
            self.model = WhisperTranscriber(
                model_size=self.config.model.size,
                device=self.config.model.device,
                language=self.config.model.language
            )
        
        elif model_type == "parakeet":
            from .models.parakeet_model import ParakeetTranscriber
            
            # Map size to model name if needed
            model_name = self._get_parakeet_model_name(self.config.model.size)
            
            self.model = ParakeetTranscriber(
                model_name=model_name,
                device=self.config.model.device,
                language=self.config.model.language
            )
        
        else:
            raise ValueError(
                f"Unknown model type: {model_type}. "
                "Supported types: whisper, parakeet"
            )
        
        if not self.model.is_ready():
            raise RuntimeError("Failed to initialize transcription model")
        
        logger.info("Transcription model initialized successfully")
    
    def _get_parakeet_model_name(self, size: str) -> str:
        """Get Parakeet model name from size specification.
        
        Args:
            size: Model size or full name
            
        Returns:
            Full Hugging Face model name
        """
        # Map common names to full model names
        size_map = {
            "parakeet": "nvidia/parakeet-tdt-0.6b-v3",
            "parakeet-0.6b": "nvidia/parakeet-tdt-0.6b-v3",
            "parakeet-1.1b": "nvidia/parakeet-rnnt-1.1b"
        }
        
        return size_map.get(size.lower(), "nvidia/parakeet-tdt-0.6b-v3")
    
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
            raise RuntimeError("Transcription model not initialized")
        
        try:
            text = self.model.transcribe(audio_data, sample_rate)
            return text
        except Exception as e:
            logger.error(f"Transcription error: {e}")
            raise
    
    def is_ready(self) -> bool:
        """Check if transcriber is ready.
        
        Returns:
            True if ready to transcribe
        """
        return self.model is not None and self.model.is_ready()
