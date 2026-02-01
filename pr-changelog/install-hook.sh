#!/bin/bash
# Install post-merge git hook for a project
#
# Usage: ./install-hook.sh /path/to/project

PROJECT_DIR="${1:-.}"
HOOK_DIR="$PROJECT_DIR/.git/hooks"
HOOK_FILE="$HOOK_DIR/post-merge"

if [ ! -d "$PROJECT_DIR/.git" ]; then
    echo "Error: $PROJECT_DIR is not a git repository"
    exit 1
fi

mkdir -p "$HOOK_DIR"

cat > "$HOOK_FILE" << 'EOF'
#!/bin/bash
# Post-merge hook: Update changelog from merged PRs
#
# This hook runs after a successful git merge (including git pull).
# It detects merged PRs and updates CHANGELOG.md + Obsidian vault.

# Only run if we're on main/master branch
BRANCH=$(git branch --show-current)
if [[ "$BRANCH" != "main" && "$BRANCH" != "master" ]]; then
    exit 0
fi

# Run the changelog agent
python3 ~/agents/pr-changelog/update_changelog.py --since "1 hour ago" 2>&1 | tee -a /tmp/pr-changelog.log

exit 0
EOF

chmod +x "$HOOK_FILE"
echo "Installed post-merge hook: $HOOK_FILE"
