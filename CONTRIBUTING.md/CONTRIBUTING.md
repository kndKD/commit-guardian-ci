# Contributing

## Setup

```sh
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
python -m pytest -q
```

## Commit messages

All commit messages follow [Conventional Commits](https://www.conventionalcommits.org/)
(`feat:`, `fix:`, `docs:`, `test:`, `ci:`, `chore:`, `refactor:`,
`style:`, `build:`, `perf:`). The AI Commit Guardian checks every
commit on PRs and posts a score table (0–100) as a PR comment:

```sh
python scripts/commit_guardian.py "feat: add login endpoint"
python scripts/commit_guardian.py --json "added stuff"   # machine-readable
python scripts/commit_guardian.py --quiet --from-git HEAD~3..HEAD
```

Exit codes: `0` every message compliant, `1` at least one
non-compliant, `2` usage error. Non-compliant messages get a suggested
fix — use it, don't force-push past the guardian.

The optional LLM layer (`guardian/llm.py`) is disabled by default.
Enable it locally with `GUARDIAN_LLM=ollama`, or `openai` / `gemini`
with the key in a GitHub Secret — never hard-code a key in the repo.

## Pull requests

- One logical change per PR; keep commits atomic and dated honestly.
- `python -m pytest -q` and `ruff check .` must pass before review.
- `make coverage` reports coverage (77% total at v0.1.0); it is
  reported, not gated — but don't drop it without saying why.
- The changelog is auto-generated on merge to `main`; don't edit
  `CHANGELOG.md` by hand.

## Docker

```sh
./scripts/docker-build.sh            # builds commit-guardian-ci:latest
docker run -p 5000:5000 commit-guardian-ci:latest
```

Docker builds are verified in GitHub Actions CI (Docker is not
installed on the author's local VM).
