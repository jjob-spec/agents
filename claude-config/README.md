# Claude Code Configuration

Portable Claude Code configuration that can be installed on any machine. Provides slash commands, agent workflows, hooks, and global rules that work across all projects.

## Prerequisites

- [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code) installed
- Git

## Installation

```bash
# 1. Clone the repo
git clone https://github.com/jwj2002/agents.git ~/agents

# 2. Run the install script
~/agents/claude-config/install.sh
```

The install script creates symlinks from `~/.claude/` to this repo:

```
~/.claude/commands/       → ~/agents/claude-config/commands/
~/.claude/agents/         → ~/agents/claude-config/agents/
~/.claude/hooks/          → ~/agents/claude-config/hooks/
~/.claude/rules/          → ~/agents/claude-config/rules/
~/.claude/settings.local.json → ~/agents/claude-config/settings.local.json
```

Existing files are backed up to `~/.claude/config-backup-{timestamp}/` before symlinking.

After installation, all commands and rules are immediately available in every Claude Code session.

## What's Included

| Directory | Purpose |
|-----------|---------|
| `commands/` | Slash commands available in Claude Code |
| `agents/` | Agent instructions for the orchestrate workflow |
| `hooks/` | Lifecycle hooks (session start, pre-compact) |
| `rules/` | Global rules loaded across all projects |
| `settings.local.json` | Hooks configuration and permissions |

## Commands

### Workflow

| Command | Usage | Description |
|---------|-------|-------------|
| `/orchestrate` | `/orchestrate 184` | Full issue workflow: MAP-PLAN → PATCH → PROVE |
| `/review` | `/review` | Code review staged changes |
| `/changelog` | `/changelog` | Generate changelog from merged PRs |
| `/standup` | `/standup` | Generate daily standup report |
| `/obsidian` | `/obsidian` | Update Obsidian vault with session info |

### FastAPI Scaffolding

| Command | Usage | Description |
|---------|-------|-------------|
| `/scaffold-project` | `/scaffold-project myapp --with-auth` | Generate a complete FastAPI project from scratch |
| `/scaffold-module` | `/scaffold-module items --fields "name:str, amount:Decimal"` | Add a module to an existing project |

#### `/scaffold-project` — New Project

Generates a complete FastAPI project with layered architecture:

```bash
# Basic project (postgres, no auth)
/scaffold-project myapp

# With JWT authentication and user management
/scaffold-project myapp --with-auth

# With SQLite instead of PostgreSQL
/scaffold-project myapp --with-auth --db sqlite
```

**What gets generated** (24-33 files):

```
myapp/
├── backend/
│   ├── backend/              # Python package
│   │   ├── main.py           # App factory
│   │   ├── main_router.py    # Router aggregator
│   │   ├── database.py       # Engine, session, Base, TimestampMixin
│   │   ├── core/
│   │   │   ├── config.py     # Pydantic Settings v2
│   │   │   ├── repository.py # BaseRepository[T] with enhanced methods
│   │   │   ├── exceptions.py # Domain exception hierarchy
│   │   │   ├── error_handlers.py
│   │   │   ├── cors.py
│   │   │   └── hashing.py    # bcrypt
│   │   └── auth/             # (if --with-auth)
│   │       ├── models.py     # User model
│   │       ├── oauth2.py     # JWT tokens
│   │       ├── router.py     # Login, signup, refresh
│   │       └── ...           # Full layered module
│   ├── tests/conftest.py     # SQLite test fixtures
│   ├── alembic/              # Migration setup
│   ├── requirements.txt
│   └── .env.example
├── .gitignore
└── README.md
```

#### `/scaffold-module` — Add Module

Adds a domain module to an existing project:

```bash
# Account-scoped entity (default)
/scaffold-module items --fields "name:str, amount:Decimal, is_active:bool"

# Not tied to an account
/scaffold-module notifications --fields "title:str, body:text, read:bool" --no-account-scoped

# Custom target directory
/scaffold-module items --fields "name:str" --parent-dir backend/backend
```

**What gets generated** (7 files):

```
module_name/
├── __init__.py
├── models.py       # SQLAlchemy model (UUID PK, TimestampMixin)
├── schemas.py      # Pydantic Create/Update/Read
├── repository.py   # BaseRepository subclass
├── services.py     # Business logic, owns transactions
├── deps.py         # FastAPI dependency factories
└── router.py       # CRUD endpoints
```

## Rules

| File | Description |
|------|-------------|
| `fastapi-layered-pattern.md` | Definitive reference for the FastAPI layered architecture pattern |

Rules in `~/.claude/rules/` are loaded globally across all Claude Code sessions, so Claude always knows the architecture conventions regardless of which project is open.

## Agents (Orchestrate Workflow)

Used by the `/orchestrate` command. Each agent has a specific role:

| Agent | Role |
|-------|------|
| `_base.md` | Shared behaviors inherited by all agents |
| `map-plan.md` | Combined analysis + implementation planning |
| `map.md` | Codebase analysis (complex issues) |
| `plan.md` | Implementation planning (complex issues) |
| `patch.md` | Code implementation |
| `prove.md` | Verification (lint, test, build) |
| `contract.md` | Frontend-backend API contract (fullstack) |
| `test-planner.md` | Test plan generation with edge cases |
| `spec-reviewer.md` | Specification review and issue creation |

## Hooks

| Hook | Trigger | Purpose |
|------|---------|---------|
| `precompact_checkpoint.py` | Before context compaction | Saves conversation state to YAML checkpoint |
| `sessionstart_restore_state.py` | Session start | Restores context from most recent checkpoint |

## Updating

Since `~/.claude/` symlinks to this repo, editing files here updates Claude Code immediately:

```bash
cd ~/agents/claude-config
# Edit files...
git add . && git commit -m "Update config" && git push
```

On other machines:

```bash
cd ~/agents && git pull
```

## What's NOT Tracked

These stay local and are not included in this repo:

- `~/.claude/projects/` — Session logs (large, machine-specific)
- `~/.claude/history.jsonl` — Command history
- `~/.claude/cache/`, `debug/`, `todos/` — Temp/state data
- `~/.claude/.claude.json` — Auth tokens

## Related

- [fastapi-architect-agent](https://github.com/jwj2002/fastapi-architect-agent) — Standalone CLI + AI agent for the same FastAPI patterns (works without Claude Code)
