# tools/speech/speech_tool.py
from typing import Any, Dict, List, Optional
from src.agent.tools.base_tool import BaseTool
from .tts_engine import TTSEngine
from .conversation import ConversationManager


class SpeechTool(BaseTool):
    """Speak, notify, and communicate with the user by voice.

    The agent should describe *what kind* of communication it wants
    (status, success, warning, ask) rather than deciding how it
    sounds — that's handled internally.
    """

    def __init__(self) -> None:
        self._tts = TTSEngine()
        self._conversation = ConversationManager(self._tts)

    @property
    def name(self) -> str:
        return "speech"

    @property
    def description(self) -> str:
        return "Speak to the user: status updates, questions, success/warning/error notifications."

    def execute(self, action: str, **kwargs: Any) -> Any:
        actions = {
            "speak": self.speak,
            "ask": self.ask,
            "status": self.status,
            "progress": self.progress,
            "success": self.success,
            "warning": self.warning,
            "error": self.error,
            "think": self.think,
            "stop": self.stop,
            "mute": self.mute,
            "unmute": self.unmute,
            "voices": self.voices,
            "set_rate": self.set_rate,
            "set_volume": self.set_volume,
        }
        if action not in actions:
            raise ValueError(f"Unknown action: {action}")
        return actions[action](**kwargs)

    # ==========================================================
    # Semantic communication
    # ==========================================================

    def speak(self, text: str) -> str:
        """Speak arbitrary text out loud.

        Args:
            text: Text to speak.

        Returns:
            The spoken text.
        """
        return self._conversation.say(text)

    def think(self, text: str) -> str:
        """Vocalize a reasoning/thinking-aloud message, e.g. before
        taking an action.

        Args:
            text: What the agent is thinking about.

        Returns:
            The spoken text.
        """
        return self._conversation.think(text)

    def status(self, text: str) -> str:
        """Announce a current action, e.g. 'Opening Chrome.'

        Args:
            text: Status message.

        Returns:
            The spoken text.
        """
        return self._conversation.status(text)

    def progress(self, text: str, percent: Optional[float] = None) -> str:
        """Announce progress on a long-running task.

        Args:
            text: Description of the task in progress.
            percent: Optional completion percentage (0-100).

        Returns:
            The spoken text.
        """
        return self._conversation.progress(text, percent=percent)

    def success(self, text: str) -> str:
        """Announce successful completion of a task.

        Args:
            text: Success message.

        Returns:
            The spoken text.
        """
        return self._conversation.success(text)

    def warning(self, text: str) -> str:
        """Announce a non-fatal warning.

        Args:
            text: Warning message.

        Returns:
            The spoken text.
        """
        return self._conversation.warning(text)

    def error(self, text: str) -> str:
        """Announce a failure or error.

        Args:
            text: Error message.

        Returns:
            The spoken text.
        """
        return self._conversation.error(text)

    def ask(self, question: str, choices: Optional[List[str]] = None) -> str:
        """Ask the user a question, optionally with multiple choice options.

        Args:
            question: The question to ask.
            choices: Optional list of choices to present.

        Returns:
            The spoken text.
        """
        return self._conversation.ask(question, choices=choices)

    # ==========================================================
    # Playback control
    # ==========================================================

    def stop(self) -> str:
        """Stop any speech currently playing.

        Returns:
            Status message.
        """
        return self._tts.stop()

    def mute(self) -> str:
        """Suppress all future speech until unmute() is called.

        Returns:
            Status message.
        """
        return self._conversation.mute()

    def unmute(self) -> str:
        """Resume speech output.

        Returns:
            Status message.
        """
        return self._conversation.unmute()

    # ==========================================================
    # Voice configuration
    # ==========================================================

    def voices(self) -> List[Dict[str, Any]]:
        """List available TTS voices on this system.

        Returns:
            List of dictionaries with voice id and name.
        """
        return self._tts.voices()

    def set_rate(self, rate: int = 200) -> str:
        """Set speech rate (words per minute, roughly).

        Args:
            rate: Speaking rate. Default ~200.

        Returns:
            Status message.
        """
        return self._tts.set_rate(rate)

    def set_volume(self, volume: float = 1.0) -> str:
        """Set speech volume.

        Args:
            volume: 0.0 (silent) to 1.0 (max).

        Returns:
            Status message.
        """
        return self._tts.set_volume(volume)


if __name__ == "__main__":
    tool = SpeechTool()
    tool.set_rate(150)
    tool.set_volume(0.8)
    tool.execute("status", text="Opening Chrome")
    tool.execute("progress", text="Downloading file", percent=45)
    tool.execute("success", text="Download complete")
    tool.execute("ask", question="Which browser should I use?", choices=["Chrome", "Firefox", "Edge"])
    print(tool.execute("voices"))