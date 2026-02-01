"""Edge TTS backend - free, high-quality neural voices."""
from __future__ import annotations

import asyncio
import subprocess
import tempfile
from pathlib import Path


async def _synthesize_async(text: str, voice: str, output_path: Path, rate: str = "+0%"):
    """Async synthesis using edge-tts library."""
    import edge_tts

    communicate = edge_tts.Communicate(text, voice, rate=rate)
    await communicate.save(str(output_path))


def synthesize(
    text: str,
    voice: str = "en-US-AriaNeural",
    speed: float = 1.0,
    output_path: Path | None = None
) -> Path:
    """
    Synthesize text to speech using Edge TTS.

    Args:
        text: Text to synthesize
        voice: Edge TTS voice name
        speed: Playback speed (1.0 = normal)
        output_path: Where to save the audio (None = temp file)

    Returns:
        Path to the generated audio file
    """
    if output_path is None:
        output_path = Path(tempfile.mktemp(suffix=".mp3"))

    # Convert speed to rate string (e.g., 1.2 -> "+20%")
    rate_percent = int((speed - 1.0) * 100)
    rate = f"{rate_percent:+d}%"

    # Run async synthesis
    asyncio.run(_synthesize_async(text, voice, output_path, rate))

    return output_path


def play(audio_path: Path):
    """Play audio file using system player."""
    import platform

    if platform.system() == "Darwin":
        subprocess.run(["afplay", str(audio_path)], check=True)
    elif platform.system() == "Linux":
        # Try common players
        for player in ["mpv", "ffplay", "aplay"]:
            try:
                subprocess.run([player, str(audio_path)], check=True)
                return
            except FileNotFoundError:
                continue
        raise RuntimeError("No audio player found. Install mpv or ffmpeg.")
    else:
        raise RuntimeError(f"Unsupported platform: {platform.system()}")


def speak(
    text: str,
    voice: str = "en-US-AriaNeural",
    speed: float = 1.0,
    save_path: Path | None = None
) -> Path | None:
    """
    Synthesize and play text.

    Args:
        text: Text to speak
        voice: Edge TTS voice name
        speed: Playback speed
        save_path: If provided, save audio to this path

    Returns:
        Path to saved audio if save_path provided, else None
    """
    output_path = save_path or Path(tempfile.mktemp(suffix=".mp3"))

    synthesize(text, voice, speed, output_path)
    play(output_path)

    if save_path is None:
        output_path.unlink()  # Clean up temp file
        return None

    return output_path
