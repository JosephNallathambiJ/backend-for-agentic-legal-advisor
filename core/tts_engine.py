"""
core/tts_engine.py - Local Text-to-Speech (TTS)
Local speech synthesis adapter with lazy loading to preserve memory.
"""

import os
from typing import Optional
from core.logging_config import logger

class TTSEngine:
    def __init__(self, voice: str = "en_default"):
        self.voice = voice

    def synthesize(self, text: str, output_path: str = "/tmp/speech.wav") -> Optional[str]:
        """Synthesizes text to speech offline without external API."""
        logger.info(f"Offline TTS: generating audio for text: {text[:50]}...")
        # Offline synthesizers like pyttsx3 or Piper
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.save_to_file(text, output_path)
            engine.runAndWait()
            return output_path
        except Exception:
            logger.info("Local TTS engine not loaded; offline voice summary available as text.")
            return None
