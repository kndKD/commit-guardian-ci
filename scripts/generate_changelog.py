"""Generate CHANGELOG.md from Conventional Commits in git history.

Fallback for git-cliff: if `git-cliff` is installed, CI prefers it.
This script needs no extra tooling and groups feat/fix/docs/etc.
Usage: python scripts/generate_changelog.py [--from-git v0.1.0..HEAD]
"""
import re
import subprocess
import sys
from collections import defaultdict

SECTIONS = [
    ("feat", "Features"), ("fix", "Bug Fixes"), ("perf", "Performance"),
    ("docs", "Documentation"), ("refactor", "Refactoring"),
    ("test", "Tests"), ("ci", "CI"), ("build", "Build"), ("chore", "Chores"),
]
PATTERN = re.compile(r"^(feat|fix|perf|docs|refactor|test|ci|build|chore)(?:\(.+\))?: (.+)$")


def commits(range_spec: str = "HEAD") -> list[str]:
    out = subprocess.check_output(
        ["git", "log", "--format=%s", range_spec], text=True)
    return [line for line in out.splitlines() if line.strip()]


def main() -> int:
    range_spec = sys.argv[2] if len(sys.argv) > 2 and sys.argv[1] == "--from-git" else "HEAD"
    grouped: dict[str, list[str]] = defaultdict(list)
    for message in commits(range_spec):
        match = PATTERN.match(message)
        if match:
            grouped[match.group(1)].append(match.group(2))
    lines = ["# Changelog\n", "All notable changes, generated from Conventional Commits.\n"]
    for type_, title in SECTIONS:
        if grouped.get(type_):
            lines.append(f"## {title}\n")
            lines.extend(f"- {item}\n" for item in grouped[type_])
            lines.append("\n")
    with open("CHANGELOG.md", "w", encoding="utf-8") as f:
        f.writelines(lines)
    print("Wrote CHANGELOG.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
