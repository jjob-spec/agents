# Document Reader

Text-to-speech for any document. Reads aloud using high-quality neural voices.

## Features

- **Any document**: Markdown, text, PDF, YouTube summaries
- **Smart parsing**: For YouTube summaries, reads summary but skips transcript
- **High-quality voices**: Edge TTS neural voices (free)
- **Save to MP3**: Create audio files for offline listening
- **Speed control**: Adjust playback speed

## Installation

```bash
~/agents/doc-reader/install.sh
```

## Usage

```bash
# Read a document aloud
read-doc document.md

# Different voice
read-doc --voice guy document.md

# Faster playback
read-doc --speed 1.2 document.md

# Save as MP3
read-doc --save ~/podcasts/ document.md

# YouTube summary - include transcript
read-doc --full youtube-summary.md

# Multiple files
read-doc *.md

# List available voices
read-doc --list-voices
```

## Voices

Edge TTS voice shortcuts:

| Shortcut | Voice | Description |
|----------|-------|-------------|
| `aria` | en-US-AriaNeural | Female, conversational (default) |
| `guy` | en-US-GuyNeural | Male, conversational |
| `jenny` | en-US-JennyNeural | Female, warm |
| `davis` | en-US-DavisNeural | Male, friendly |
| `nova` | en-US-NovaNeural | Female, formal |

Or use full voice names: `en-US-AriaNeural`, `en-GB-SoniaNeural`, etc.

## Document Types

| Type | Detection | Behavior |
|------|-----------|----------|
| YouTube summary | Has Channel/Duration table | Reads summary, skips transcript |
| Markdown | .md extension | Converts to readable text |
| PDF | .pdf extension | Extracts text |
| Text | Default | Reads as-is |

## Options

| Option | Description |
|--------|-------------|
| `--backend`, `-b` | TTS backend: `edge` (default), `macos` |
| `--voice`, `-v` | Voice name or shortcut |
| `--speed`, `-s` | Playback speed (default: 1.0) |
| `--save DIR` | Save audio to directory |
| `--full`, `-f` | Include transcript for YouTube summaries |
| `--quiet`, `-q` | Minimal output |
| `--list-voices` | Show available voices |

## Examples

```bash
# Read YouTube summary (skips transcript)
read-doc ~/summaries/2026-02-01-agentic-rag.md

# Create podcast version
read-doc --save ~/podcasts/ --voice davis ~/summaries/*.md

# Quick listen at 1.3x speed
read-doc -s 1.3 notes.md

# Use macOS built-in TTS (no internet needed)
read-doc --backend macos --voice Samantha document.md
```

## Podcast Mode

Convert your summaries to MP3s for listening on the go:

```bash
# Convert all summaries to podcasts
read-doc --save ~/podcasts/ ~/summaries/*.md

# Then sync ~/podcasts/ to your phone or music player
```
