#!/bin/bash
# Install doc-reader dependencies

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/.venv"

echo "Document Reader - Installation"
echo "=============================="
echo ""

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"
pip install --quiet --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install --quiet edge-tts pypdf

echo "  ✓ edge-tts installed"
echo "  ✓ pypdf installed (for PDF support)"

deactivate

# Create shell alias
echo ""
echo "Setting up shell alias..."

ALIAS_LINE='alias read-doc="~/agents/doc-reader/.venv/bin/python ~/agents/doc-reader/reader.py"'

if [[ -f "$HOME/.zshrc" ]]; then
    if ! grep -q "read-doc" "$HOME/.zshrc"; then
        echo "" >> "$HOME/.zshrc"
        echo "# Document Reader" >> "$HOME/.zshrc"
        echo "$ALIAS_LINE" >> "$HOME/.zshrc"
        echo "  ✓ Added alias to ~/.zshrc"
    else
        echo "  - Alias already exists in ~/.zshrc"
    fi
fi

if [[ -f "$HOME/.bashrc" ]]; then
    if ! grep -q "read-doc" "$HOME/.bashrc"; then
        echo "" >> "$HOME/.bashrc"
        echo "# Document Reader" >> "$HOME/.bashrc"
        echo "$ALIAS_LINE" >> "$HOME/.bashrc"
        echo "  ✓ Added alias to ~/.bashrc"
    else
        echo "  - Alias already exists in ~/.bashrc"
    fi
fi

# Create output directory
mkdir -p "$HOME/podcasts"
echo "  ✓ Created ~/podcasts/"

# Make script executable
chmod +x "$SCRIPT_DIR/reader.py"

echo ""
echo "=============================="
echo "Installation complete!"
echo ""
echo "Usage:"
echo "  read-doc document.md              # Read aloud"
echo "  read-doc --voice guy document.md  # Different voice"
echo "  read-doc --speed 1.2 document.md  # Faster"
echo "  read-doc --save ~/podcasts/ doc.md # Save as MP3"
echo "  read-doc --full youtube-summary.md # Include transcript"
echo ""
echo "Voices (Edge TTS shortcuts):"
echo "  aria, guy, jenny, davis, nova"
echo ""
echo "Reload shell or run: source ~/.zshrc"
