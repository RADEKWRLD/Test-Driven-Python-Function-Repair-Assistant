PYTHON ?= python3.12
VENV ?= .venv
IMAGE ?= function-repair/sandbox-python:dev
TASKS_DIR ?= benchmarks/tasks
MAX_ATTEMPTS ?= 5
REPETITIONS ?= 10
SEED ?= 20261016
MODEL ?= deepseek-chat
DATA_DIR ?= var

.PHONY: bootstrap format lint typecheck test check sandbox-build sandbox-test experiment

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

experiment: check sandbox-test
	$(VENV)/bin/repair-agent doctor
	$(VENV)/bin/repair-agent benchmark $(TASKS_DIR) \
		--max-attempts $(MAX_ATTEMPTS) \
		--repetitions $(REPETITIONS) \
		--seed $(SEED) \
		--model $(MODEL) \
		--image $(IMAGE) \
		--data-dir $(DATA_DIR)
