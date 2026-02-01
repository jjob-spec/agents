#!/usr/bin/env python3
"""
PR Changelog Agent

Detects merged PRs and updates:
1. Project CHANGELOG.md
2. Obsidian vault changelog

Usage:
    python update_changelog.py                    # Check last day
    python update_changelog.py --since "3 days"  # Check last 3 days
    python update_changelog.py --pr 123          # Specific PR
    python update_changelog.py --dry-run         # Preview only
"""
from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

# Add script directory to path
sys.path.insert(0, str(Path(__file__).parent))

from git_utils import (
    get_repo_name,
    get_recent_merges,
    get_merge_info,
    get_pr_info_from_gh,
    MergedPR,
    detect_change_type
)
from changelog_writer import (
    format_changelog_entry,
    update_project_changelog,
    update_obsidian_changelog
)


def get_pr_from_gh(pr_number: int, cwd: Path) -> MergedPR | None:
    """Get PR info from GitHub CLI."""
    info = get_pr_info_from_gh(pr_number, cwd)
    if not info:
        return None

    merge_date = info.get("mergedAt", "")
    if merge_date:
        # Parse ISO format: 2024-01-31T12:00:00Z
        merge_date = merge_date.split("T")[0]
    else:
        merge_date = datetime.now().strftime("%Y-%m-%d")

    commits = []
    for c in info.get("commits", [])[:10]:
        msg = c.get("messageHeadline", "") or c.get("commit", {}).get("message", "").split("\n")[0]
        if msg:
            commits.append(msg)

    author = info.get("author", {})
    author_name = author.get("name") or author.get("login", "unknown")

    return MergedPR(
        number=pr_number,
        title=info.get("title", f"PR #{pr_number}"),
        author=author_name,
        branch=info.get("headRefName", "unknown"),
        merge_date=merge_date,
        commits=commits,
        files_changed=info.get("changedFiles", 0)
    )


def main():
    parser = argparse.ArgumentParser(description="Update changelog from merged PRs")
    parser.add_argument("--since", default="1 day ago", help="Time range to check")
    parser.add_argument("--pr", type=int, help="Specific PR number to add")
    parser.add_argument("--dry-run", "-n", action="store_true", help="Preview only")
    parser.add_argument("--project", "-p", help="Project directory")

    args = parser.parse_args()

    project_dir = Path(args.project) if args.project else Path.cwd()
    repo_name = get_repo_name(project_dir)

    print(f"Repository: {repo_name}")
    print(f"Project dir: {project_dir}")

    merged_prs: list[MergedPR] = []

    if args.pr:
        # Get specific PR
        print(f"Fetching PR #{args.pr}...")
        pr = get_pr_from_gh(args.pr, project_dir)
        if pr:
            merged_prs.append(pr)
        else:
            print(f"Could not find PR #{args.pr}")
            sys.exit(1)
    else:
        # Find recent merges
        print(f"Checking merges since: {args.since}")
        merge_commits = get_recent_merges(args.since, project_dir)
        print(f"Found {len(merge_commits)} merge commits")

        for commit in merge_commits:
            pr = get_merge_info(commit, project_dir)
            if pr:
                merged_prs.append(pr)
                print(f"  - PR #{pr.number}: {pr.title}")

    if not merged_prs:
        print("No merged PRs found.")
        return

    # Enhance PR info using GitHub CLI for better titles
    print("\nFetching PR details from GitHub...")
    for i, pr in enumerate(merged_prs):
        if pr.title == f"PR #{pr.number}":  # Title not extracted from git
            gh_pr = get_pr_from_gh(pr.number, project_dir)
            if gh_pr:
                merged_prs[i] = gh_pr
                print(f"  - PR #{pr.number}: {gh_pr.title}")

    # Group by date
    by_date: dict[str, list[MergedPR]] = {}
    for pr in merged_prs:
        date = pr.merge_date
        if date not in by_date:
            by_date[date] = []
        by_date[date].append(pr)

    # Generate entries
    all_entries = []
    for date in sorted(by_date.keys(), reverse=True):
        prs = by_date[date]
        entries = [format_changelog_entry(pr) for pr in prs]
        all_entries.extend(entries)

        print(f"\n## {date}")
        for entry in entries:
            print(f"  {entry}")

    if args.dry_run:
        print("\n[DRY RUN] No files updated.")
        return

    # Update project changelog
    for date, prs in by_date.items():
        entries = [format_changelog_entry(pr) for pr in prs]

        project_changelog = update_project_changelog(project_dir, entries, date)
        print(f"\nUpdated: {project_changelog}")

        obsidian_changelog = update_obsidian_changelog(repo_name, entries, date, prs)
        print(f"Updated: {obsidian_changelog}")


if __name__ == "__main__":
    main()
