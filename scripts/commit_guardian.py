"""AI Commit Guardian — rule-based checker (no API key needed).

Checks commit messages against Conventional Commits and scores them
0-100. An LLM layer (OpenAI/Gemini/Ollama) can be added later: it
receives the same JSON this script emits and returns a suggested fix.
The CI job posts the result as a PR comment; it never blocks on the
LLM being unavailable — the rule-based score is the fallback.

Usage:
    python scripts/commit_guardian.py "feat: add login endpoint"
    python scripts/commit_guardian.py --from-git HEAD~3..HEAD
    echo "bad message" | python scripts/commit_guardian.py --stdin
"""
import json
import re
import subprocess
import sys

TYPES = {
    "feat", "fix", "docs", "style", "refactor", "perf", "test",
    "build", "ci", "chore", "revert",
}
PATTERN = re.compile(
    r"^(?P<type>feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)"
    r"(?P<scope>\([a-z0-9\-/]+\))?(?P<breaking>!)?: (?P<subject>.+)$"
)


def suggest(message: str) -> str:
    words = message.strip().lower().split()
    verb = words[0] if words else "update"
    rest = " ".join(words[1:]) if len(words) > 1 else "app"
    return f"feat: {verb} {rest}" if verb not in TYPES else f"feat: {rest}"


def check(message: str) -> dict:
    message = message.strip().splitlines()[0] if message.strip() else ""
    result = {"message": message, "score": 0, "compliant": False,
              "issues": [], "suggestion": suggest(message)}
    if not message:
        result["issues"].append("Commit message is empty.")
        return result
    match = PATTERN.match(message)
    if not match:
        result["issues"].append(
            "Not Conventional Commits: expected '<type>: <subject>', "
            "e.g. 'feat: add login endpoint'.")
        result["score"] = 20 if len(message) > 10 else 0
        return result
    score = 70
    subject = match.group("subject")
    if len(subject) < 10:
        result["issues"].append("Subject is very short — say what changed.")
    else:
        score += 10
    if subject[0].isupper():
        score += 5
    if not subject.endswith("."):
        score += 5
    else:
        result["issues"].append("Subject should not end with a period.")
    if match.group("scope"):
        score += 10
    result["score"] = min(score, 100)
    result["compliant"] = result["score"] >= 70 and not result["issues"]
    if result["compliant"]:
        result["suggestion"] = message
    return result


def messages_from_git(range_spec: str) -> list[str]:
    out = subprocess.check_output(
        ["git", "log", "--format=%s", range_spec], text=True)
    return [line for line in out.splitlines() if line.strip()]


def main(argv: list[str]) -> int:
    if "--stdin" in argv:
        messages = [line for line in sys.stdin.read().splitlines() if line.strip()]
    elif "--from-git" in argv:
        idx = argv.index("--from-git")
        messages = messages_from_git(argv[idx + 1])
    elif len(argv) > 1:
        messages = [" ".join(argv[1:])]
    else:
        print(__doc__)
        return 2
    results = [check(m) for m in messages]
    print(json.dumps(results, indent=2))
    return 0 if all(r["compliant"] for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
