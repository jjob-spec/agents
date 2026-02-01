# PR Changelog Agent

Automatically updates changelog when PRs are merged.

## What It Does

When you `git pull` and a PR merge comes in, this agent:

1. Detects the merged PR(s)
2. Extracts PR info (title, number, commits, author)
3. Updates `CHANGELOG.md` in the project
4. Logs to Obsidian vault

## Changelog Format

```markdown
## 2026-01-31

- feat: Add user authentication (PR #42)
- fix: Login redirect bug (PR #38)
- refactor: Clean up API handlers (PR #35)
```

## Installation

### 1. Install the post-merge hook in your project

```bash
~/agents/pr-changelog/install-hook.sh /path/to/your/project
```

Or for current directory:

```bash
~/agents/pr-changelog/install-hook.sh .
```

### 2. (Optional) Add shell alias

Add to `~/.zshrc`:

```bash
alias pr-changelog="python3 ~/agents/pr-changelog/update_changelog.py"
```

## Usage

### Automatic (Post-Merge Hook)

After installing the hook, changelog updates automatically on:
- `git pull` (when it includes a merge)
- `git merge` (direct merges)

Only runs on main/master branch.

### Manual

```bash
# Check last day (default)
pr-changelog

# Check last 3 days
pr-changelog --since "3 days ago"

# Add specific PR
pr-changelog --pr 123

# Preview only (no file changes)
pr-changelog --dry-run

# For a specific project
pr-changelog --project /path/to/project
```

## Requirements

- Python 3.10+
- Git
- GitHub CLI (`gh`) for fetching PR details

## Files

| File | Purpose |
|------|---------|
| `config.py` | Path configuration |
| `git_utils.py` | Git and GitHub utilities |
| `changelog_writer.py` | Writes to CHANGELOG.md and Obsidian |
| `update_changelog.py` | Main entry point |
| `install-hook.sh` | Installs git hook in a project |

## Output Locations

| Location | Format |
|----------|--------|
| `{project}/CHANGELOG.md` | Simple date-based entries |
| `MyVault/Projects/{repo}/changelog.md` | Same + PR commit details |

## Change Type Detection

The agent auto-detects change type from PR title:

| Prefix/Keyword | Type |
|----------------|------|
| `feat:`, `add`, `new` | feat |
| `fix:`, `bug` | fix |
| `refactor:` | refactor |
| `docs:` | docs |
| `test:` | test |
| `chore:`, `deps:` | chore |
| (other) | update |
