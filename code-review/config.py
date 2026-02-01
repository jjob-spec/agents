"""Configuration for Code Review Agent."""

# Review categories and their severity
CATEGORIES = {
    "security": "critical",      # Security vulnerabilities
    "bug": "critical",           # Likely bugs
    "error-handling": "warning", # Missing error handling
    "code-smell": "warning",     # Code quality issues
    "style": "info",             # Style suggestions
    "todo": "info",              # TODOs and FIXMEs
}

# Patterns to check (from your PROVE phase)
CRITICAL_PATTERNS = [
    "ENUM_VALUE: Use string VALUES not Python names (e.g., 'CO-OWNER' not CO_OWNER)",
    "COMPONENT_API: Verify props match PropTypes before using components",
    "TODO/STUB: Check for incomplete implementations",
]
