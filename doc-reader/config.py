"""Configuration for doc-reader."""
from pathlib import Path

# Output directory for saved audio
AUDIO_OUTPUT_DIR = Path.home() / "podcasts"

# Default TTS settings
DEFAULT_TTS_BACKEND = "edge"  # edge, macos, piper
DEFAULT_VOICE = "en-US-AriaNeural"  # Edge TTS voice
DEFAULT_SPEED = 1.0
DEFAULT_MACOS_VOICE = "Samantha"

# Edge TTS voices (good options)
EDGE_VOICES = {
    "aria": "en-US-AriaNeural",      # Female, conversational
    "guy": "en-US-GuyNeural",        # Male, conversational
    "jenny": "en-US-JennyNeural",    # Female, warm
    "davis": "en-US-DavisNeural",    # Male, friendly
    "nova": "en-US-NovaNeural",      # Female, formal
}

# macOS voices
MACOS_VOICES = ["Samantha", "Alex", "Daniel", "Karen", "Moira", "Tessa"]
