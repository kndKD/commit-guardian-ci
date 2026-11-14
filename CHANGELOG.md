# Changelog
All notable changes, generated from Conventional Commits.
## Features
- add Makefile with test, lint, coverage and run targets
- add ruff configuration in pyproject.toml
- build Docker image in two stages (builder + slim runtime)
- split commit guardian into guardian package with scoring, suggestions, CLI and optional LLM layer
- add changelog generator from Conventional Commits
- add AI Commit Guardian rule-based Conventional Commits checker
- add Dockerfile with non-root user, gunicorn and healthcheck
- add Flask app with index, health and hello endpoints
- initialise Flask app package

## Documentation
- update CHANGELOG.md [skip ci]
- update CHANGELOG.md [skip ci]
- update CHANGELOG.md [skip ci]
- update CHANGELOG.md [skip ci]
- update CHANGELOG.md [skip ci]
- update CHANGELOG.md [skip ci]
- update CHANGELOG.md [skip ci]
- document guardian flags, exit codes and LLM layer in README
- update CHANGELOG.md [skip ci]
- update CHANGELOG.md [skip ci]
- update CHANGELOG.md [skip ci]
- update CHANGELOG.md [skip ci]
- update CHANGELOG.md [skip ci]
- update CHANGELOG.md [skip ci]
- add initial changelog
- update CHANGELOG.md [skip ci]
- add README with purpose, tools, run steps and guardian guide
- update CHANGELOG.md [skip ci]
- add architecture diagram and component notes
- update CHANGELOG.md [skip ci]

## Refactoring
- rewrite commit-guardian CLI as thin wrapper

## Tests
- add guardian scoring, suggestion, long-subject and CLI tests
- add tests for index, health and hello endpoints

## CI
- PR comment posts per-commit score table
- add build-and-test, commit review and changelog jobs

## Build
- add pytest for development and CI
- add Flask and gunicorn dependencies

## Chores
- add ruff and pytest-cov to dev requirements
- exclude coverage, ruff cache and logs from Docker context
- add dockerignore to keep the image lean
- add MIT license
- add gitignore for Python, venv and caches

