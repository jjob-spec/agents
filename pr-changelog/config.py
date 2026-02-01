"""Configuration for PR Changelog Agent."""
import os
from pathlib import Path

# Obsidian vault path
VAULT_PATH = Path(os.path.expanduser(
    "~/Library/Mobile Documents/iCloud~md~obsidian/Documents/MyVault"
))

# Projects folder within vault
PROJECTS_FOLDER = VAULT_PATH / "Projects"
