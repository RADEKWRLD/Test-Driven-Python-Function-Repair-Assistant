PYTHON ?= python3.12
VENV ?= .venv
IMAGE ?= function-repair/sandbox-python:dev
TASKS_DIR ?= benchmarks/feedbackeval-humaneval-full
MAX_ATTEMPTS ?= 3
REPETITIONS ?= 1
SEED ?= 20261016
# Leave empty to let repair-agent read REPAIR_ASSISTANT_MODEL from .env.
# Callers can still override it explicitly with `make experiment MODEL=...`.
MODEL ?=
DATA_DIR ?= results
PRICING_FILE ?=
RESUME ?=
DOCKER_PROXY ?=

.PHONY: bootstrap format lint typecheck test check sandbox-build sandbox-test experiment

bootstrap:
	$(PYTHON) -m venv $(VENV)
	$(VENV)/bin/pip install -e '.[dev]'

format:
	$(VENV)/bin/ruff format src tests tools
	$(VENV)/bin/ruff check --fix src tests tools

lint:
	$(VENV)/bin/ruff format --check src tests tools
	$(VENV)/bin/ruff check src tests tools

typecheck:
	$(VENV)/bin/mypy src tests

test:
	$(VENV)/bin/pytest -m 'not sandbox'

check: lint typecheck test

sandbox-build:
	docker build $(if $(strip $(DOCKER_PROXY)),--build-arg HTTP_PROXY=$(DOCKER_PROXY) --build-arg HTTPS_PROXY=$(DOCKER_PROXY)) -f docker/sandbox-python.Dockerfile -t $(IMAGE) .

sandbox-test:
	$(VENV)/bin/pytest -m sandbox

experiment: check sandbox-test
	$(VENV)/bin/repair-agent doctor
	$(VENV)/bin/repair-agent benchmark $(TASKS_DIR) \
		--max-attempts $(MAX_ATTEMPTS) \
		--repetitions $(REPETITIONS) \
		--seed $(SEED) $(if $(strip $(MODEL)),--model $(MODEL)) \
		--image $(IMAGE) \
		--data-dir $(DATA_DIR) \
		$(if $(strip $(PRICING_FILE)),--pricing-file "$(PRICING_FILE)") \
		$(if $(strip $(RESUME)),--resume "$(RESUME)")
