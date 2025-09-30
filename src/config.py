"""Configuration management for Wispr-Flow Clone."""

import os
import yaml
from pathlib import Path
from typing import Any, Dict, Optional
from dataclasses import dataclass, field


@dataclass
class ModelConfig:
    """Model configuration."""
    type: str = "whisper"
    size: str = "base"
    device: str = "cpu"
    language: str = "en"


@dataclass
class HotkeyConfig:
    """Hotkey configuration."""
    modifiers: list[str] = field(default_factory=lambda: ["ctrl", "alt"])
    key: str = ""


@dataclass
class AudioConfig:
    """Audio recording configuration."""
    sample_rate: int = 16000
    channels: int = 1
    chunk_size: int = 1024
    format: str = "int16"
    device_index: Optional[int] = None


@dataclass
class AppConfig:
    """Application configuration."""
    debug: bool = False
    min_audio_length: float = 0.3
    show_notifications: bool = False


class Config:
    """Main configuration class."""
    
    def __init__(self, config_path: Optional[Path] = None):
        """Initialize configuration.
        
        Args:
            config_path: Path to config file. Defaults to config.yaml in project root.
        """
        if config_path is None:
            # Get project root (parent of src directory)
            src_dir = Path(__file__).parent
            project_root = src_dir.parent
            config_path = project_root / "config.yaml"
        
        self.config_path = Path(config_path)
        self._config_data: Dict[str, Any] = {}
        self._load_config()
        
        # Initialize sub-configs
        self.model = self._init_model_config()
        self.hotkey = self._init_hotkey_config()
        self.audio = self._init_audio_config()
        self.app = self._init_app_config()
    
    def _load_config(self) -> None:
        """Load configuration from YAML file."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        
        with open(self.config_path, 'r') as f:
            self._config_data = yaml.safe_load(f) or {}
    
    def _init_model_config(self) -> ModelConfig:
        """Initialize model configuration."""
        model_data = self._config_data.get('model', {})
        return ModelConfig(
            type=model_data.get('type', 'whisper'),
            size=model_data.get('size', 'base'),
            device=model_data.get('device', 'cpu'),
            language=model_data.get('language', 'en')
        )
    
    def _init_hotkey_config(self) -> HotkeyConfig:
        """Initialize hotkey configuration."""
        hotkey_data = self._config_data.get('hotkey', {})
        return HotkeyConfig(
            modifiers=hotkey_data.get('modifiers', ['ctrl', 'alt']),
            key=hotkey_data.get('key', '')
        )
    
    def _init_audio_config(self) -> AudioConfig:
        """Initialize audio configuration."""
        audio_data = self._config_data.get('audio', {})
        return AudioConfig(
            sample_rate=audio_data.get('sample_rate', 16000),
            channels=audio_data.get('channels', 1),
            chunk_size=audio_data.get('chunk_size', 1024),
            format=audio_data.get('format', 'int16'),
            device_index=audio_data.get('device_index')
        )
    
    def _init_app_config(self) -> AppConfig:
        """Initialize application configuration."""
        app_data = self._config_data.get('app', {})
        return AppConfig(
            debug=app_data.get('debug', False),
            min_audio_length=app_data.get('min_audio_length', 0.3),
            show_notifications=app_data.get('show_notifications', False)
        )
