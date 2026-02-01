#!/usr/bin/env python3
"""
Document Reader - TTS for any document

Reads documents aloud using text-to-speech.
For YouTube summaries, reads the summary but skips the transcript (unless --full).

Usage:
    read-doc document.md
    read-doc --voice guy --speed 1.2 document.md
    read-doc --save ~/podcasts/ document.md
    read-doc --full youtube-summary.md  # Include transcript
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Add script directory to path
sys.path.insert(0, str(Path(__file__).parent))

from config import (
    DEFAULT_TTS_BACKEND, DEFAULT_VOICE, DEFAULT_SPEED,
    DEFAULT_MACOS_VOICE, EDGE_VOICES, AUDIO_OUTPUT_DIR
)
from parsers.document import parse_document


def get_tts_backend(backend: str):
    """Get TTS backend module."""
    if backend == "edge":
        from tts import edge_tts
        return edge_tts
    elif backend == "macos":
        from tts import macos_tts
        return macos_tts
    else:
        raise ValueError(f"Unknown TTS backend: {backend}")


def resolve_voice(voice: str, backend: str) -> str:
    """Resolve voice shorthand to full voice name."""
    if backend == "edge":
        # Check if it's a shorthand
        if voice.lower() in EDGE_VOICES:
            return EDGE_VOICES[voice.lower()]
        return voice
    else:
        return voice


def read_document(
    file_path: Path,
    backend: str = DEFAULT_TTS_BACKEND,
    voice: str | None = None,
    speed: float = DEFAULT_SPEED,
    save_dir: Path | None = None,
    include_full: bool = False,
    quiet: bool = False
) -> Path | None:
    """
    Read a document aloud.

    Args:
        file_path: Path to document
        backend: TTS backend (edge, macos)
        voice: Voice to use
        speed: Playback speed
        save_dir: Directory to save audio (None = don't save)
        include_full: Include transcript for YouTube summaries
        quiet: Don't print progress

    Returns:
        Path to saved audio if save_dir provided
    """
    # Set default voice based on backend
    if voice is None:
        voice = DEFAULT_VOICE if backend == "edge" else DEFAULT_MACOS_VOICE

    # Resolve voice shorthand
    voice = resolve_voice(voice, backend)

    # Parse document
    if not quiet:
        print(f"Parsing: {file_path.name}")

    doc = parse_document(file_path, include_transcript=include_full)

    if not quiet:
        print(f"  Type: {doc.doc_type}")
        print(f"  Title: {doc.title}")
        print(f"  Content: {len(doc.content):,} characters")
        if doc.doc_type == "youtube_summary" and not include_full:
            print(f"  (Transcript skipped - use --full to include)")

    # Prepare save path if needed
    save_path = None
    if save_dir:
        save_dir = Path(save_dir)
        save_dir.mkdir(parents=True, exist_ok=True)
        # Create filename from document title
        safe_title = "".join(c if c.isalnum() or c in " -_" else "" for c in doc.title)
        safe_title = safe_title[:50].strip().replace(" ", "-").lower()
        save_path = save_dir / f"{safe_title}.mp3"

    # Get TTS backend
    tts = get_tts_backend(backend)

    # Speak
    if not quiet:
        if save_path:
            print(f"\nGenerating audio: {save_path}")
        else:
            print(f"\nReading aloud (voice: {voice}, speed: {speed}x)...")
            print("Press Ctrl+C to stop\n")

    try:
        result = tts.speak(
            doc.content,
            voice=voice,
            speed=speed,
            save_path=save_path
        )

        if result and not quiet:
            print(f"\n✓ Saved to: {result}")

        return result

    except KeyboardInterrupt:
        print("\n\nStopped.")
        return None


def main():
    parser = argparse.ArgumentParser(
        description="Read documents aloud using text-to-speech"
    )
    parser.add_argument(
        "files",
        nargs="+",
        type=Path,
        help="Document(s) to read"
    )
    parser.add_argument(
        "--backend", "-b",
        choices=["edge", "macos"],
        default=DEFAULT_TTS_BACKEND,
        help=f"TTS backend (default: {DEFAULT_TTS_BACKEND})"
    )
    parser.add_argument(
        "--voice", "-v",
        help="Voice to use (e.g., 'aria', 'guy', 'jenny' for Edge; 'Samantha', 'Alex' for macOS)"
    )
    parser.add_argument(
        "--speed", "-s",
        type=float,
        default=DEFAULT_SPEED,
        help=f"Playback speed (default: {DEFAULT_SPEED})"
    )
    parser.add_argument(
        "--save",
        type=Path,
        metavar="DIR",
        help="Save audio to directory instead of playing"
    )
    parser.add_argument(
        "--full", "-f",
        action="store_true",
        help="Include transcript for YouTube summaries"
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Minimal output"
    )
    parser.add_argument(
        "--list-voices",
        action="store_true",
        help="List available voices for the backend"
    )

    args = parser.parse_args()

    # List voices if requested
    if args.list_voices:
        if args.backend == "edge":
            print("Edge TTS voices (shortcuts):")
            for name, voice in EDGE_VOICES.items():
                print(f"  {name}: {voice}")
            print("\nFor full list: edge-tts --list-voices")
        else:
            from tts import macos_tts
            print("macOS voices:")
            for voice in macos_tts.list_voices()[:20]:
                print(f"  {voice}")
        return

    # Read each file
    for file_path in args.files:
        if not file_path.exists():
            print(f"Error: File not found: {file_path}", file=sys.stderr)
            continue

        read_document(
            file_path,
            backend=args.backend,
            voice=args.voice,
            speed=args.speed,
            save_dir=args.save,
            include_full=args.full,
            quiet=args.quiet
        )

        # Add spacing between multiple files
        if len(args.files) > 1:
            print()


if __name__ == "__main__":
    main()
