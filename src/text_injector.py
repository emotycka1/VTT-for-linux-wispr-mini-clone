"""Text injection module using xdotool."""

import subprocess
import logging
from typing import Optional


logger = logging.getLogger(__name__)


class TextInjector:
    """Injects text at cursor position using xdotool."""
    
    def __init__(self):
        """Initialize text injector."""
        self._check_xdotool()
        logger.info("TextInjector initialized")
    
    def _check_xdotool(self) -> None:
        """Check if xdotool is available."""
        try:
            subprocess.run(
                ['which', 'xdotool'],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
        except subprocess.CalledProcessError:
            raise RuntimeError(
                "xdotool not found. Install it with: sudo apt install xdotool"
            )
    
    def inject_text(self, text: str, delay: int = 12) -> bool:
        """Inject text at current cursor position.
        
        Args:
            text: Text to inject
            delay: Delay between keystrokes in milliseconds
            
        Returns:
            True if successful, False otherwise
        """
        if not text:
            logger.warning("Empty text provided, nothing to inject")
            return False
        
        try:
            # Use xdotool to type the text
            # --delay controls typing speed (12ms is reasonable)
            subprocess.run(
                ['xdotool', 'type', '--delay', str(delay), '--', text],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=10
            )
            logger.info(f"Successfully injected text: {len(text)} characters")
            return True
            
        except subprocess.TimeoutExpired:
            logger.error("Text injection timeout")
            return False
        except subprocess.CalledProcessError as e:
            logger.error(f"Text injection failed: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during text injection: {e}")
            return False
    
    def get_active_window(self) -> Optional[str]:
        """Get name of currently active window.
        
        Returns:
            Window name or None if error
        """
        try:
            result = subprocess.run(
                ['xdotool', 'getactivewindow', 'getwindowname'],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=2
            )
            return result.stdout.strip()
        except Exception as e:
            logger.error(f"Failed to get active window: {e}")
            return None
