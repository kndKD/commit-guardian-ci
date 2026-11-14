"""Command-line interface for the Commit Guardian.

Exit codes (documented here and in the README):
    0 — every checked message is compliant
    1 — at least one message is non-compliant
    2 — usage error (no message, no --from-git, no --stdin)

Output modes:
    default  — one human-readable line per message
    --json   — machine-readable JSON array (what CI consumes)
    --quiet  — only non-compliant messages, one line each; silent when clean

Usage:
    python scripts/commit_guardian.py "feat: add login endpoint"
    python scripts/commit_guardian.py --json "added stuff"
    python scripts/commit_guardian.py --quiet --from-git HEAD~3..HEAD
    echo "bad message" | python scripts/commit_guardian.py --stdin
    python scripts/commit_guardian.py --llm "added stuff"
"""
import argparse
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from guardian.llm import suggest_via_llm  # noqa: E402
from guardian.scoring import check  # noqa: E402


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="commit_guardian",
        description="Score commit messages against Conventional Commits.")
    parser.add_argument("message", nargs="*", help="Commit message to check.")
    parser.add_argument("--from-git", metavar="RANGE",
                        help="Check commit subjects in a git range, e.g. HEAD~3..HEAD.")
    parser.add_argument("--stdin", action="store_true",
                        help="Read one message per line from stdin.")
    parser.add_argument("--llm", action="store_true",
                        help="Let the optional LLM layer improve suggestions "
                             "(guardian/llm.py; disabled unless configured).")
    parser.add_argument("--json", action="store_true",
                        help="Print results as a JSON array instead of "
                             "human-readable lines.")
    parser.add_argument("--quiet", action="store_true",
                        help="Only print non-compliant messages; silent when all pass.")
    return parser


def messages_from_git(range_spec: str) -> list[str]:
    out = subprocess.check_output(
        ["git", "log", "--format=%s", range_spec], text=True)
    return [line for line in out.splitlines() if line.strip()]


def format_human(result: dict) -> str:
    mark = "✓" if result["compliant"] else "✗"
    line = f"{mark} {result['score']:3d}  {result['message']}"
    if not result["compliant"]:
        line += f"  →  {result['suggestion']} ({'; '.join(result['issues'])})"
    return line


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.stdin:
        messages = [line for line in sys.stdin.read().splitlines() if line.strip()]
    elif args.from_git:
        messages = messages_from_git(args.from_git)
    elif args.message:
        messages = [" ".join(args.message)]
    else:
        build_parser().print_usage(sys.stderr)
        print("commit_guardian: error: no message given "
              "(pass a message, --from-git RANGE, or --stdin)",
              file=sys.stderr)
        return 2
    results = [check(m) for m in messages]
    if args.llm:
        for result in results:
            if not result["compliant"]:
                improved = suggest_via_llm(result["message"])
                if improved:
                    result["suggestion"] = improved
                    result["llm_suggestion"] = True
    if args.json:
        print(json.dumps(results, indent=2))
    elif args.quiet:
        for result in results:
            if not result["compliant"]:
                print(format_human(result))
    else:
        for result in results:
            print(format_human(result))
    return 0 if all(r["compliant"] for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
