# Daily Standup Agent

Aggregates work across all projects from your Obsidian vault for daily standups.

## What It Does

Reads from your Obsidian vault and generates:
- Yesterday's completed items (across all projects)
- Today's next steps
- Current blockers

## Usage

### Terminal

```bash
# Standard daily standup
daily-standup

# Last 3 days
daily-standup --since "3 days"

# Weekly summary
daily-standup --week

# Single project only
daily-standup --project mymoney-dev

# Copy to clipboard
daily-standup --copy
```

### Claude Code

```
/standup
```

## Output Example

```markdown
# Daily Standup - 2026-01-31

## Yesterday

### mymoney-dev
- [x] Fixed security audit logging (#656)
- [x] Added multi-firm documentation (#657)

### agents
- [x] Built pr-changelog agent
- [x] Globalized memory system

## Today's Focus

### mymoney-dev
- [ ] Close GitHub issue #658
- [ ] Add integration tests

### agents
- [ ] Build daily-standup agent

## Blockers
- (none)
```

## Data Sources

The agent reads from:

```
Obsidian Vault/Projects/
├── {project}/
│   ├── completed.md    → completed items by date
│   ├── next-steps.md   → open tasks
│   └── blockers.md     → current blockers
```

These files are populated by the `obsidian-agent` during your coding sessions.

## Requirements

- Python 3.10+
- Obsidian vault with project structure (created by obsidian-agent)

## Options

| Flag | Description |
|------|-------------|
| `--since "N days"` | Look back N days for completed items |
| `--week` | Weekly summary (last 7 days) |
| `--project NAME` | Single project only |
| `--copy`, `-c` | Copy output to clipboard |
