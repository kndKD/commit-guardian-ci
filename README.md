#Dockerize + GitHub Actions CI

[![CI](https://github.com/kndKD/commit-guardian-ci/actions/workflows/ci.yml/badge.svg)](https://github.com/kndKD/commit-guardian-ci/actions/workflows/ci.yml) [![License: MIT](https://img.shields.io/github/license/kndKD/commit-guardian-ci)](https://github.com/kndKD/commit-guardian-ci/blob/main/LICENSE)

**Innovation: AI Commit Guardian + Auto-Changelog**

This CI pipeline doesn't just build — it teaches. Every PR gets AI-powered
commit message feedback, and every merge auto-generates a changelog. This
turns CI into a learning loop.

## Purpose

Package a small Flask app in Docker, build and test it with GitHub Actions,
and carry the same app forward through Projects 2–12.

## Architecture

See [docs/architecture.md](docs/architecture.md) — Mermaid diagram of
developer → GitHub → CI (build/test) → Commit Guardian (PR comment) →
changelog on merge to `main`.

## Tools used

Python 3.12, Flask, gunicorn, Docker, GitHub Actions, pytest, git-cliff
(CI prefers it; `scripts/generate_changelog.py` is the no-dependency fallback).

## Run locally

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
python -m pytest -q
python app/main.py
# Docker (verified in CI — Docker is not installed on the author's local VM):
# docker build -t system-core:ci . && docker run -p 5000:5000 system-core:ci
```

## AI Commit Guardian

```bash
python scripts/commit_guardian.py "feat: add login endpoint"
python scripts/commit_guardian.py "added stuff"   # non-compliant, with a suggested fix
python scripts/commit_guardian.py --json "added stuff"  # machine-readable JSON (used by CI)
python scripts/commit_guardian.py --quiet --from-git HEAD~3..HEAD  # only non-compliant lines
python scripts/commit_guardian.py --llm "added stuff"  # optional LLM-improved suggestion
```

Exit codes: `0` every message compliant, `1` at least one non-compliant,
`2` usage error (no message, `--from-git` range, or `--stdin` given).

The checker is rule-based and needs no API key (score 0–100, Conventional
Commits). An optional LLM layer lives in `guardian/llm.py` and is disabled
by default: set `GUARDIAN_LLM=ollama` for local Ollama (free), or
`openai` / `gemini` with the key in a GitHub Secret (`OPENAI_API_KEY` /
`GEMINI_API_KEY`) — never hard-code a key. If the LLM is unconfigured or
fails, the rule-based suggestion is used instead. On every PR, CI posts a
per-commit score table as a PR comment.

## Measurable impact

- Commit message quality score (0–100) shown in CI output and in the PR comment.
- PR review time: to be measured before vs after once the guardian is live
  on real PRs — no invented baseline is claimed here.

## What I learned

- _To be filled in as the project runs — Docker layering, CI job design,
  and Conventional Commits in practice._

## Challenges

- _To be filled in as the project runs — e.g. Docker not available locally,
  so image builds are verified in GitHub Actions._

## Docker (multi-stage)

```sh
./scripts/docker-build.sh            # builds commit-guardian-ci:latest
docker run -p 5000:5000 commit-guardian-ci:latest
```

The image is built in two stages: a `builder` stage installs dependencies
into `/install`, and the `runtime` stage copies only those packages plus
`app/` into a slim image running as the non-root `appuser`. Build size is
not measured locally — Docker is not installed on this VM; the build is
verified in GitHub Actions CI.

## Lint and coverage

```sh
make test        # pytest
make lint        # ruff check . (rules E, F; line-length 88, see pyproject.toml)
make coverage    # pytest --cov=app --cov=guardian
make run         # ./scripts/run.sh — Flask on :5000
```

Coverage is reported, not gated: total is 77% (14 Nov 2026), with
`guardian/llm.py` at 26% because the LLM providers are disabled by default
and need no key — its paths need mocked tests before any coverage gate.
