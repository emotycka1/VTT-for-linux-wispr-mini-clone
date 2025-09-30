"""Parakeet model implementation using NeMo."""

import logging
import numpy as np
from typing import Optional


logger = logging.getLogger(__name__)


class ParakeetTranscriber:
    """Transcriber using NVIDIA Parakeet model via NeMo.
    
    Note: This requires nemo_toolkit to be installed.
    Install with: pip install nemo_toolkit[asr]
    """
    
    def __init__(
        self,
        model_name: str = "nvidia/parakeet-tdt-0.6b-v3",
        device: str = "cpu",
        language: str = "en"
    ):
        """Initialize Parakeet transcriber.
        
        Args:
            model_name: Hugging Face model name
            device: Device to use (cpu, cuda)
            language: Language code (currently supports en, es, fr, de, etc.)
        """
        self.model_name = model_name
        self.device = device
        self.language = language
        self.model: Optional[any] = None
        
        logger.info(
            f"Initializing Parakeet model: {model_name}, "
            f"device={device}, language={language}"
        )
        self._load_model()
    
    def _load_model(self) -> None:
        """Load the Parakeet model."""
        try:
            # Import NeMo (lazy import)
            try:
                import nemo.collections.asr as nemo_asr
            except ImportError:
                raise ImportError(
                    "nemo_toolkit not installed. "
                    "Install with: pip install nemo_toolkit[asr]"
                )
            
            # Load model from Hugging Face
            self.model = nemo_asr.models.EncDecRNNTBPEModel.from_pretrained(
                model_name=self.model_name
            )
            
            # Move to device
            if self.device == "cuda":
                self.model = self.model.cuda()
            else:
                self.model = self.model.cpu()
            
            self.model.eval()
            logger.info("Parakeet model loaded successfully")
        
        except Exception as e:
            logger.error(f"Failed to load Parakeet model: {e}")
            logger.warning(
                "Parakeet support is optional. "
                "Consider using Whisper instead or install: pip install nemo_toolkit[asr]"
            )
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
            
            # NeMo expects a list of file paths or audio arrays
            # We'll use the transcribe method with numpy array
            import tempfile
            import soundfile as sf
            
            # Save to temporary file (NeMo typically works with files)
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=True) as tmp:
                sf.write(tmp.name, audio_float, sample_rate)
                
                # Transcribe
                transcription = self.model.transcribe([tmp.name])
            
            if transcription and len(transcription) > 0:
                text = transcription[0].strip()
                logger.info(f"Transcription complete: {len(text)} characters")
                return text
            else:
                logger.warning("No transcription returned")
                return ""
        
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
        # Parakeet TDT 0.6B v3 supports multiple languages
        return [
            "en", "es", "fr", "de", "it", "pt", "pl", "ru",
            "zh", "ja", "ko", "ar", "hi", "tr"
        ]
