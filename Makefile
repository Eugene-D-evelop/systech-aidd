.PHONY: install run lint format

install:
	uv sync

run:
	uv run python src/main.py

lint:
	uv run ruff check src/

format:
	uv run ruff format src/

