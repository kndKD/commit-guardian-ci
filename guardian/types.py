"""Shared types and limits for the Commit Guardian.

Kept in one place so scoring, suggesting and the CLI agree on the result
shape and on what counts as a well-formed subject.
"""

from typing import TypedDict

# Conventional Commits types recognised by the guardian.
TYPES = {
    "feat",
    "fix",
    "docs",
    "style",
    "refactor",
    "perf",
    "test",
    "build",
    "ci",
    "chore",
    "revert",
}

# A subject shorter than this is flagged as too vague; longer than the max
# is flagged as too long (keep the first line readable in `git log`).
MIN_SUBJECT_LENGTH = 10
MAX_SUBJECT_LENGTH = 72

# Minimum score for a message to count as compliant (with no open issues).
COMPLIANT_MIN_SCORE = 70


class CheckResult(TypedDict, total=False):
    """One scored commit message, as returned by guardian.scoring.check."""

    message: str
    score: int  # 0-100
    compliant: bool
    issues: list[str]
    suggestion: str
    llm_suggestion: bool  # True only when an LLM improved the suggestion
