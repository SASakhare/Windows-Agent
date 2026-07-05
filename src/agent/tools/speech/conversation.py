# tools/speech/conversation.py
from typing import Optional
from .tts_engine import TTSEngine


class ConversationManager:
    """Translates semantic communication intents (status, success,
    warning, ask...) into actual TTS calls. This is the layer that
    would later fan out to GUI notifications/logs too, without the
    agent's other tools knowing anything changed."""

    def __init__(self, tts: TTSEngine) -> None:
        self._tts = tts
        self._muted = False

    def _emit(self, text: str) -> str:
        if self._muted:
            return f"(muted) {text}"
        self._tts.speak(text)
        return text

    def say(self, text: str) -> str:
        return self._emit(text)

    def think(self, text: str) -> str:
        return self._emit(text)

    def status(self, text: str) -> str:
        return self._emit(text)

    def progress(self, text: str, percent: Optional[float] = None) -> str:
        msg = f"{text} ({percent:.0f}%)" if percent is not None else text
        return self._emit(msg)

    def success(self, text: str) -> str:
        return self._emit(text)

    def warning(self, text: str) -> str:
        return self._emit(text)

    def error(self, text: str) -> str:
        return self._emit(text)

    def ask(self, question: str, choices: Optional[list] = None) -> str:
        text = question
        if choices:
            text += " Options: " + ", ".join(choices)
        return self._emit(text)

    def mute(self) -> str:
        self._muted = True
        return "Muted."

    def unmute(self) -> str:
        self._muted = False
        return "Unmuted."