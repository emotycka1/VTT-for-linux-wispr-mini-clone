"""Global hotkey listener using pynput."""

import logging
from typing import Callable, Optional
from pynput import keyboard


logger = logging.getLogger(__name__)


class HotkeyListener:
    """Listens for global hotkey combinations."""
    
    def __init__(
        self,
        modifiers: list[str],
        key: str = "",
        on_press: Optional[Callable] = None,
        on_release: Optional[Callable] = None
    ):
        """Initialize hotkey listener.
        
        Args:
            modifiers: List of modifier keys (e.g., ['ctrl', 'alt'])
            key: Optional main key (empty for modifier-only hotkey)
            on_press: Callback when hotkey is pressed
            on_release: Callback when hotkey is released
        """
        self.modifiers = set(self._normalize_modifier(m) for m in modifiers)
        self.key = key.lower() if key else None
        self.on_press_callback = on_press
        self.on_release_callback = on_release
        
        self.current_keys = set()
        self.hotkey_active = False
        self.listener: Optional[keyboard.Listener] = None
        
        logger.info(f"HotkeyListener initialized: modifiers={modifiers}, key={key}")
    
    def _normalize_modifier(self, modifier: str) -> keyboard.Key:
        """Convert modifier string to pynput Key.
        
        Args:
            modifier: Modifier name (ctrl, alt, shift, etc.)
            
        Returns:
            pynput Key object
        """
        modifier_map = {
            'ctrl': keyboard.Key.ctrl,
            'control': keyboard.Key.ctrl,
            'alt': keyboard.Key.alt,
            'shift': keyboard.Key.shift,
            'cmd': keyboard.Key.cmd,
            'super': keyboard.Key.cmd,
        }
        
        normalized = modifier.lower()
        if normalized not in modifier_map:
            raise ValueError(f"Unknown modifier: {modifier}")
        
        return modifier_map[normalized]
    
    def _check_hotkey(self) -> bool:
        """Check if current key combination matches hotkey.
        
        Returns:
            True if hotkey is active
        """
        # Check if all modifiers are pressed
        modifiers_pressed = all(mod in self.current_keys for mod in self.modifiers)
        
        # If no main key specified, just check modifiers
        if self.key is None:
            return modifiers_pressed
        
        # Check if main key is also pressed
        return modifiers_pressed and self.key in self.current_keys
    
    def _on_press(self, key) -> None:
        """Handle key press event.
        
        Args:
            key: Key that was pressed
        """
        try:
            # Add key to current set
            if hasattr(key, 'char') and key.char:
                self.current_keys.add(key.char.lower())
            else:
                self.current_keys.add(key)
            
            # Check if hotkey is now active
            if not self.hotkey_active and self._check_hotkey():
                self.hotkey_active = True
                logger.debug("Hotkey pressed")
                if self.on_press_callback:
                    self.on_press_callback()
        
        except Exception as e:
            logger.error(f"Error in key press handler: {e}")
    
    def _on_release(self, key) -> None:
        """Handle key release event.
        
        Args:
            key: Key that was released
        """
        try:
            # Remove key from current set
            if hasattr(key, 'char') and key.char:
                self.current_keys.discard(key.char.lower())
            else:
                self.current_keys.discard(key)
            
            # Check if hotkey was released
            if self.hotkey_active and not self._check_hotkey():
                self.hotkey_active = False
                logger.debug("Hotkey released")
                if self.on_release_callback:
                    self.on_release_callback()
        
        except Exception as e:
            logger.error(f"Error in key release handler: {e}")
    
    def start(self) -> None:
        """Start listening for hotkeys."""
        if self.listener is not None:
            logger.warning("Listener already running")
            return
        
        self.listener = keyboard.Listener(
            on_press=self._on_press,
            on_release=self._on_release
        )
        self.listener.start()
        logger.info("Hotkey listener started")
    
    def stop(self) -> None:
        """Stop listening for hotkeys."""
        if self.listener is None:
            return
        
        self.listener.stop()
        self.listener = None
        self.current_keys.clear()
        self.hotkey_active = False
        logger.info("Hotkey listener stopped")
    
    def is_running(self) -> bool:
        """Check if listener is running.
        
        Returns:
            True if running
        """
        return self.listener is not None and self.listener.is_alive()
