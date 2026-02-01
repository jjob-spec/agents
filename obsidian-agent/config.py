"""Configuration for the Obsidian Vault Agent."""
import os
from pathlib import Path

# Obsidian vault path
VAULT_PATH = Path(os.path.expanduser(
    "~/Library/Mobile Documents/iCloud~md~obsidian/Documents/MyVault"
))

# Claude Code projects directory
CLAUDE_PROJECTS_PATH = Path(os.path.expanduser("~/.claude/projects"))

# Projects folder within vault
PROJECTS_FOLDER = VAULT_PATH / "Projects"

# Templates folder
TEMPLATES_FOLDER = PROJECTS_FOLDER / ".templates"
