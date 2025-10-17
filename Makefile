.PHONY: install run lint format test test-unit test-integration ci migrate db-up db-down api-dev api-test api-docs

install:
	uv sync

run:
	uv run python -m src.main

api-dev:
	uv run python -m src.api_main

api-test:
	@echo "Testing API endpoint..."
	@curl -s http://localhost:8000/api/stats/dashboard | python -m json.tool || echo "Error: API not responding. Run 'make api-dev' first."

api-docs:
	@echo "Opening Swagger UI at http://localhost:8000/docs"
	@python -m webbrowser http://localhost:8000/docs 2>/dev/null || echo "Please open http://localhost:8000/docs in your browser"

migrate:
	uv run python -m src.migrations

db-up:
	docker compose up -d postgres

db-down:
	docker compose down

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

