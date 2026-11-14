"""Suggest a Conventional Commits fix for a non-compliant message.

Rule-based only — no API key, no network. The suggestion is a starting
point for the author, not a rewrite: it keeps the author's words and
only repairs the shape.
"""

from guardian.types import TYPES


def suggest(message: str) -> str:
    """Return a `'<type>: <subject>'` suggestion for `message`."""
    stripped = message.strip()
    # A bare type with no subject ("feat:" / "feat") — ask for one.
    bare = stripped.rstrip(":").lower()
    if bare in TYPES:
        return f"{bare}: describe the change"
    words = stripped.lower().split()
    verb = words[0] if words else "update"
    rest = " ".join(words[1:]) if len(words) > 1 else "app"
    return f"feat: {verb} {rest}" if verb not in TYPES else f"feat: {rest}"
