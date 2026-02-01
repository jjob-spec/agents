"""macOS TTS backend - uses built-in 'say' command."""
from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path


def speak(
    text: str,
    voice: str = "Samantha",
    speed: float = 1.0,
    save_path: Path | None = None
) -> Path | None:
    """
    Speak text using macOS say command.

    Args:
        text: Text to speak
        voice: macOS voice name (e.g., Samantha, Alex, Daniel)
        speed: Words per minute multiplier (1.0 = ~175 wpm)
        save_path: If provided, save audio to this path

    Returns:
        Path to saved audio if save_path provided, else None
    """
    # Convert speed multiplier to words per minute
    base_wpm = 175
    wpm = int(base_wpm * speed)

    cmd = ["say", "-v", voice, "-r", str(wpm)]

    if save_path:
        # Save to file
        cmd.extend(["-o", str(save_path)])
        if save_path.suffix == ".mp3":
            # say outputs AIFF by default, convert to mp3
            aiff_path = save_path.with_suffix(".aiff")
            cmd.extend(["-o", str(aiff_path)])
            cmd.append(text)
            subprocess.run(cmd, check=True)
            # Convert to mp3
            subprocess.run([
                "ffmpeg", "-y", "-i", str(aiff_path),
                "-acodec", "libmp3lame", "-q:a", "2",
                str(save_path)
            ], capture_output=True, check=True)
            aiff_path.unlink()
        else:
            cmd.append(text)
            subprocess.run(cmd, check=True)
        return save_path
    else:
        # Speak directly
        cmd.append(text)
        subprocess.run(cmd, check=True)
        return None


def list_voices() -> list[str]:
    """List available macOS voices."""
    result = subprocess.run(
        ["say", "-v", "?"],
        capture_output=True,
        text=True,
        check=True
    )
    voices = []
    for line in result.stdout.strip().split("\n"):
        if line:
            voice_name = line.split()[0]
            voices.append(voice_name)
    return voices
