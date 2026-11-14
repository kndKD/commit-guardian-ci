.PHONY: test lint coverage run docker-build clean

VENV ?= .venv
PYTHON ?= $(VENV)/bin/python

test:
	$(PYTHON) -m pytest -q

lint:
	$(PYTHON) -m ruff check .

coverage:
	$(PYTHON) -m pytest -q --cov=app --cov=guardian --cov-report=term-missing

run:
	./scripts/run.sh

docker-build:
	./scripts/docker-build.sh

clean:
	rm -rf .pytest_cache .coverage htmlcov .ruff_cache
	find . -name __pycache__ -type d -exec rm -rf {} + 2>/dev/null || true
