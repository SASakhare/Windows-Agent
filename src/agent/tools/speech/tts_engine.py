# tools/speech/tts_engine.py
from typing import List, Dict, Any
import pyttsx3


class TTSEngine:
    """Pure text-to-speech wrapper. No AI/semantic logic — just audio.

    Note: pyttsx3 has a known issue where reusing one engine instance
    across multiple say()+runAndWait() calls can hang after the first
    call (especially with the Windows sapi5 driver). Re-initializing
    the engine per speak() call avoids this reliably.
    """

    def __init__(self) -> None:
        self._rate: int = 200
        self._volume: float = 1.0
        self._voice_id: str = None # type: ignore

    def _new_engine(self):
        engine = pyttsx3.init()
        engine.setProperty("rate", self._rate)
        engine.setProperty("volume", self._volume)
        if self._voice_id:
            engine.setProperty("voice", self._voice_id)
        return engine

    def speak(self, text: str, block: bool = True) -> str:
        engine = self._new_engine()
        engine.say(text)
        if block:
            engine.runAndWait()
            engine.stop()
        return "Spoken."

    def stop(self) -> str:
        # Nothing persistent to stop since engines are per-call now.
        return "Stopped."

    def save_audio(self, text: str, path: str) -> str:
        engine = self._new_engine()
        engine.save_to_file(text, path)
        engine.runAndWait()
        engine.stop()
        return path

    def set_rate(self, rate: int) -> str:
        self._rate = rate
        return f"Rate set to {rate}."

    def set_volume(self, volume: float) -> str:
        self._volume = volume
        return f"Volume set to {volume}."

    def set_voice(self, voice_id: str) -> str:
        self._voice_id = voice_id
        return f"Voice set to {voice_id}."

    def voices(self) -> List[Dict[str, Any]]:
        engine = self._new_engine()
        result = [{"id": v.id, "name": v.name} for v in engine.getProperty("voices")] # type: ignore
        engine.stop()
        return result

    def is_speaking(self) -> bool:
        # Can't meaningfully track this across per-call engines;
        # left as False since each speak() call is blocking/synchronous.
        return False