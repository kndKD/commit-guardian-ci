"""Rule-based Conventional Commits scoring, 0-100. No API key needed."""

import re

from guardian.suggest import suggest
from guardian.types import (
    COMPLIANT_MIN_SCORE,
    MAX_SUBJECT_LENGTH,
    MIN_SUBJECT_LENGTH,
    CheckResult,
)

# Re-exported so `from guardian.scoring import suggest` keeps working.
__all__ = ["check", "suggest"]

PATTERN = re.compile(
    r"^(?P<type>feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)"
    r"(?P<scope>\([a-z0-9\-/]+\))?(?P<breaking>!)?: (?P<subject>.+)$"
)


def check(message: str) -> CheckResult:
    message = message.strip().splitlines()[0] if message.strip() else ""
    result: CheckResult = {
        "message": message,
        "score": 0,
        "compliant": False,
        "issues": [],
        "suggestion": suggest(message),
    }
    if not message:
        result["issues"].append("Commit message is empty.")
        return result
    match = PATTERN.match(message)
    if not match:
        result["issues"].append(
            "Not Conventional Commits: expected '<type>: <subject>', "
            "e.g. 'feat: add login endpoint'."
        )
        result["score"] = 20 if len(message) > 10 else 0
        return result
    score = 70
    subject = match.group("subject")
    if len(subject) < MIN_SUBJECT_LENGTH:
        result["issues"].append("Subject is very short — say what changed.")
    else:
        score += 10
    if len(subject) > MAX_SUBJECT_LENGTH:
        result["issues"].append(
            f"Subject is long ({len(subject)} chars) — "
            f"keep it under {MAX_SUBJECT_LENGTH}."
        )
        score -= 10
    if subject[0].isupper():
        score += 5
    if not subject.endswith("."):
        score += 5
    else:
        result["issues"].append("Subject should not end with a period.")
    if match.group("scope"):
        score += 10
    result["score"] = max(0, min(score, 100))
    result["compliant"] = (
        result["score"] >= COMPLIANT_MIN_SCORE and not result["issues"]
    )
    if result["compliant"]:
        result["suggestion"] = message
    return result
