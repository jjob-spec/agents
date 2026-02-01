"""Document parser - detects type and extracts readable content."""
from __future__ import annotations

import re
from pathlib import Path
from dataclasses import dataclass


@dataclass
class ParsedDocument:
    """Parsed document content."""
    title: str
    content: str
    doc_type: str  # youtube_summary, markdown, text, pdf
    full_content: str  # Original full content


def detect_document_type(file_path: Path, content: str) -> str:
    """Detect document type based on content patterns."""
    # Check for YouTube summary markers
    if "| **Channel** |" in content and "| **Duration** |" in content:
        return "youtube_summary"

    # Check file extension
    suffix = file_path.suffix.lower()
    if suffix == ".pdf":
        return "pdf"
    elif suffix in [".md", ".markdown"]:
        return "markdown"
    else:
        return "text"


def extract_title(content: str) -> str:
    """Extract title from document."""
    # Look for markdown H1
    match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if match:
        return match.group(1).strip()

    # First non-empty line
    for line in content.split('\n'):
        line = line.strip()
        if line:
            return line[:100]

    return "Untitled Document"


def parse_youtube_summary(content: str, include_transcript: bool = False) -> str:
    """
    Parse YouTube summary, extracting readable content.

    By default, skips the transcript section.
    """
    lines = content.split('\n')
    result_lines = []
    in_transcript = False
    in_details = False

    for line in lines:
        # Detect transcript section
        if '<details>' in line.lower():
            in_details = True
            if not include_transcript:
                continue

        if '</details>' in line.lower():
            in_details = False
            if not include_transcript:
                continue

        if in_details and not include_transcript:
            continue

        # Skip the "Full Transcript" header
        if '## Full Transcript' in line and not include_transcript:
            continue

        # Skip table formatting (but keep content)
        if line.strip().startswith('|') and '---' in line:
            continue

        # Convert table rows to readable text
        if line.strip().startswith('|') and '**' in line:
            # Extract key-value from table
            parts = line.split('|')
            if len(parts) >= 3:
                key = parts[1].replace('**', '').strip()
                value = parts[2].replace('**', '').strip()
                if key and value:
                    result_lines.append(f"{key}: {value}")
            continue

        # Skip HTML-like tags
        if line.strip().startswith('<') and line.strip().endswith('>'):
            continue

        # Skip summary click instruction
        if 'Click to expand' in line:
            continue

        result_lines.append(line)

    return '\n'.join(result_lines)


def parse_markdown(content: str) -> str:
    """Parse markdown, converting to readable plain text."""
    # Remove code blocks
    content = re.sub(r'```[\s\S]*?```', '[code block]', content)
    content = re.sub(r'`[^`]+`', '', content)

    # Convert headers to emphasized text
    content = re.sub(r'^#{1,6}\s+(.+)$', r'\1.', content, flags=re.MULTILINE)

    # Remove markdown links, keep text
    content = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', content)

    # Remove emphasis markers
    content = re.sub(r'\*\*([^*]+)\*\*', r'\1', content)
    content = re.sub(r'\*([^*]+)\*', r'\1', content)
    content = re.sub(r'__([^_]+)__', r'\1', content)
    content = re.sub(r'_([^_]+)_', r'\1', content)

    # Convert bullet points
    content = re.sub(r'^\s*[-*+]\s+', '• ', content, flags=re.MULTILINE)

    # Remove horizontal rules
    content = re.sub(r'^-{3,}$', '', content, flags=re.MULTILINE)

    # Clean up extra whitespace
    content = re.sub(r'\n{3,}', '\n\n', content)

    return content.strip()


def parse_document(
    file_path: Path,
    include_transcript: bool = False
) -> ParsedDocument:
    """
    Parse a document and extract readable content.

    Args:
        file_path: Path to the document
        include_transcript: For YouTube summaries, include the transcript

    Returns:
        ParsedDocument with extracted content
    """
    # Read file
    if file_path.suffix.lower() == ".pdf":
        # For PDFs, try to extract text
        try:
            import pypdf
            reader = pypdf.PdfReader(str(file_path))
            full_content = "\n".join(page.extract_text() for page in reader.pages)
        except ImportError:
            raise RuntimeError("PDF support requires pypdf: pip install pypdf")
    else:
        full_content = file_path.read_text(encoding='utf-8')

    # Detect type
    doc_type = detect_document_type(file_path, full_content)

    # Extract title
    title = extract_title(full_content)

    # Parse based on type
    if doc_type == "youtube_summary":
        content = parse_youtube_summary(full_content, include_transcript)
        content = parse_markdown(content)  # Also clean up markdown
    elif doc_type == "markdown":
        content = parse_markdown(full_content)
    else:
        content = full_content

    return ParsedDocument(
        title=title,
        content=content,
        doc_type=doc_type,
        full_content=full_content
    )
