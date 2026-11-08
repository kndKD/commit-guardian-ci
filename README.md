# Project 1 — Dockerize + GitHub Actions CI

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
```

The checker is rule-based and needs no API key (score 0–100, Conventional
Commits). An LLM layer can be added later via a GitHub Secret
(`OPENAI_API_KEY` / `GEMINI_API_KEY`) or local Ollama — it receives the
same JSON and returns a suggested fix.

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
