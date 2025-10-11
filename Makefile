.PHONY: install run lint format test test-unit test-integration ci

install:
	uv sync

run:
	uv run python -m src.main

lint:
	uv run ruff check src/ tests/
	uv run mypy src/

format:
	uv run ruff format src/ tests/

test:
	uv run pytest -v --cov=src --cov-report=term-missing --cov-report=html

test-unit:
	uv run pytest -m "not integration" -v --cov=src --cov-report=term-missing

test-integration:
	uv run pytest -m integration -v

ci: lint test-unit

