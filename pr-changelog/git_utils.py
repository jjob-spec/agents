"""Git utilities for extracting PR and merge information."""
from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional


@dataclass
class MergedPR:
    """Information about a merged PR."""
    number: int
    title: str
    author: str
    branch: str
    merge_date: str
    commits: list[str]
    files_changed: int


def run_git(args: list[str], cwd: Path = None) -> str:
    """Run a git command and return output."""
    result = subprocess.run(
        ["git"] + args,
        capture_output=True,
        text=True,
        cwd=cwd
    )
    return result.stdout.strip()


def get_repo_name(cwd: Path = None) -> str:
    """Get the repository name from git remote or directory."""
    remote = run_git(["remote", "get-url", "origin"], cwd)
    if remote:
        # Extract repo name from URL
        # git@github.com:user/repo.git or https://github.com/user/repo.git
        match = re.search(r'/([^/]+?)(?:\.git)?$', remote)
        if match:
            return match.group(1)
    # Fallback to directory name
    return (cwd or Path.cwd()).name


def get_default_branch(cwd: Path = None) -> str:
    """Get the default branch name (main or master)."""
    # Try to get from remote HEAD
    result = run_git(["symbolic-ref", "refs/remotes/origin/HEAD"], cwd)
    if result:
        return result.split("/")[-1]
    # Fallback: check if main exists, otherwise master
    branches = run_git(["branch", "-l"], cwd)
    if "main" in branches:
        return "main"
    return "master"


def get_recent_merges(since: str = "1 day ago", cwd: Path = None) -> list[str]:
    """Get merge commit hashes since a given time."""
    output = run_git([
        "log",
        "--merges",
        "--pretty=format:%H",
        f"--since={since}"
    ], cwd)
    if not output:
        return []
    return output.split("\n")


def get_merge_info(commit_hash: str, cwd: Path = None) -> MergedPR | None:
    """Extract PR information from a merge commit."""
    # Get commit message
    message = run_git(["log", "-1", "--pretty=format:%s%n%b", commit_hash], cwd)

    # Try to extract PR number from merge commit message
    # Common formats:
    # - "Merge pull request #123 from branch"
    # - "Merge branch 'feature' (PR #123)"
    # - "feat: something (#123)"
    pr_match = re.search(r'#(\d+)', message)
    if not pr_match:
        return None

    pr_number = int(pr_match.group(1))

    # Get the first line as title (clean it up)
    title = message.split("\n")[0]
    # Remove "Merge pull request #N from ..." prefix
    title = re.sub(r'^Merge pull request #\d+ from \S+\s*', '', title)
    # Remove trailing PR reference if it's just "(#N)"
    title = re.sub(r'\s*\(#\d+\)$', '', title)
    if not title:
        title = f"PR #{pr_number}"

    # Get author
    author = run_git(["log", "-1", "--pretty=format:%an", commit_hash], cwd)

    # Get merge date
    date = run_git(["log", "-1", "--pretty=format:%ci", commit_hash], cwd)
    merge_date = date.split(" ")[0] if date else datetime.now().strftime("%Y-%m-%d")

    # Get branch name from merge commit
    branch_match = re.search(r'from (\S+)', message)
    branch = branch_match.group(1) if branch_match else "unknown"

    # Get commits in this merge (excluding the merge commit itself)
    commits_output = run_git([
        "log",
        "--pretty=format:%s",
        f"{commit_hash}^..{commit_hash}^2"
    ], cwd)
    commits = [c for c in commits_output.split("\n") if c] if commits_output else []

    # Get files changed count
    files_output = run_git(["diff", "--stat", f"{commit_hash}^..{commit_hash}"], cwd)
    files_match = re.search(r'(\d+) files? changed', files_output)
    files_changed = int(files_match.group(1)) if files_match else 0

    return MergedPR(
        number=pr_number,
        title=title,
        author=author,
        branch=branch,
        merge_date=merge_date,
        commits=commits,
        files_changed=files_changed
    )


def get_pr_info_from_gh(pr_number: int, cwd: Path = None) -> dict | None:
    """Get PR info using GitHub CLI (more reliable)."""
    try:
        result = subprocess.run(
            ["gh", "pr", "view", str(pr_number), "--json",
             "title,author,mergedAt,commits,changedFiles,headRefName"],
            capture_output=True,
            text=True,
            cwd=cwd,
            timeout=10
        )
        if result.returncode == 0:
            import json
            return json.loads(result.stdout)
    except Exception:
        pass
    return None


def detect_change_type(title: str) -> str:
    """Detect the type of change from PR title."""
    title_lower = title.lower()

    if any(kw in title_lower for kw in ["feat:", "feature:", "add ", "added ", "new "]):
        return "feat"
    elif any(kw in title_lower for kw in ["fix:", "bug:", "fixed ", "bugfix"]):
        return "fix"
    elif any(kw in title_lower for kw in ["refactor:", "refactored ", "cleanup"]):
        return "refactor"
    elif any(kw in title_lower for kw in ["docs:", "documentation", "readme"]):
        return "docs"
    elif any(kw in title_lower for kw in ["test:", "tests:", "testing"]):
        return "test"
    elif any(kw in title_lower for kw in ["chore:", "deps:", "dependency", "bump"]):
        return "chore"
    else:
        return "update"
