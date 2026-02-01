"""Write changelog entries to project and Obsidian vault."""
from datetime import datetime
from pathlib import Path

from config import PROJECTS_FOLDER
from git_utils import MergedPR, detect_change_type


def format_changelog_entry(pr: MergedPR) -> str:
    """Format a PR as a changelog line."""
    change_type = detect_change_type(pr.title)
    return f"- {change_type}: {pr.title} (PR #{pr.number})"


def update_project_changelog(project_dir: Path, entries: list[str], date: str) -> Path:
    """Update or create CHANGELOG.md in the project."""
    changelog_path = project_dir / "CHANGELOG.md"

    # Read existing content
    if changelog_path.exists():
        content = changelog_path.read_text()
    else:
        content = "# Changelog\n\nAll notable changes to this project.\n\n"

    # Check if today's section exists
    date_header = f"## {date}"

    if date_header in content:
        # Append to existing date section
        lines = content.split("\n")
        new_lines = []
        inserted = False

        for i, line in enumerate(lines):
            new_lines.append(line)
            if line.strip() == date_header and not inserted:
                # Insert entries after the header
                # Find where to insert (skip empty lines after header)
                j = i + 1
                while j < len(lines) and lines[j].strip() == "":
                    new_lines.append(lines[j])
                    j += 1
                # Add new entries
                for entry in entries:
                    if entry not in content:  # Avoid duplicates
                        new_lines.append(entry)
                inserted = True

        content = "\n".join(new_lines)
    else:
        # Insert new date section after the header
        header_end = content.find("\n\n", content.find("# Changelog"))
        if header_end == -1:
            header_end = len(content)
        else:
            header_end += 2

        new_section = f"{date_header}\n\n"
        for entry in entries:
            new_section += f"{entry}\n"
        new_section += "\n"

        content = content[:header_end] + new_section + content[header_end:]

    changelog_path.write_text(content)
    return changelog_path


def update_obsidian_changelog(repo_name: str, entries: list[str], date: str, prs: list[MergedPR]) -> Path:
    """Update changelog in Obsidian vault."""
    project_dir = PROJECTS_FOLDER / repo_name
    project_dir.mkdir(parents=True, exist_ok=True)

    changelog_path = project_dir / "changelog.md"

    # Read existing content
    if changelog_path.exists():
        content = changelog_path.read_text()
    else:
        content = f"# Changelog - {repo_name}\n\n> Merged PRs and releases.\n\n---\n\n"

    # Check if today's section exists
    date_header = f"## {date}"

    if date_header in content:
        # Append to existing date section
        lines = content.split("\n")
        new_lines = []
        inserted = False

        for i, line in enumerate(lines):
            new_lines.append(line)
            if line.strip() == date_header and not inserted:
                j = i + 1
                while j < len(lines) and lines[j].strip() == "":
                    new_lines.append(lines[j])
                    j += 1
                for entry in entries:
                    if entry not in content:
                        new_lines.append(entry)
                inserted = True

        content = "\n".join(new_lines)
    else:
        # Insert new date section after the header
        insert_pos = content.find("---\n")
        if insert_pos != -1:
            insert_pos += 4
        else:
            insert_pos = len(content)

        new_section = f"\n{date_header}\n\n"
        for entry in entries:
            new_section += f"{entry}\n"

        # Add PR details
        for pr in prs:
            if pr.commits:
                new_section += f"\n**PR #{pr.number}** ({pr.author}):\n"
                for commit in pr.commits[:5]:  # Limit to 5 commits
                    new_section += f"  - {commit}\n"

        content = content[:insert_pos] + new_section + content[insert_pos:]

    changelog_path.write_text(content)
    return changelog_path
