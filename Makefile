PYTHON ?= python3.12
VENV ?= .venv
IMAGE ?= function-repair/sandbox-python:dev

.PHONY: bootstrap format lint typecheck test check sandbox-build sandbox-test

bootstrap:
	$(PYTHON) -m venv $(VENV)
	$(VENV)/bin/pip install -e '.[dev]'

format:
	$(VENV)/bin/ruff format src tests
	$(VENV)/bin/ruff check --fix src tests

lint:
	$(VENV)/bin/ruff format --check src tests
	$(VENV)/bin/ruff check src tests

typecheck:
	$(VENV)/bin/mypy src tests

test:
	$(VENV)/bin/pytest -m 'not sandbox'

check: lint typecheck test

sandbox-build:
	docker build -f docker/sandbox-python.Dockerfile -t $(IMAGE) .

sandbox-test:
	$(VENV)/bin/pytest -m sandbox
