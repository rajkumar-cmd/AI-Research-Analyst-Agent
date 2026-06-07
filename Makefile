.PHONY: help dev dev-web dev-api test lint format-check docker-up docker-down docker-config clean-cache

help:
	@echo "research-agent-os developer commands"
	@echo ""
	@echo "  make dev             Start the full local stack with Docker Compose"
	@echo "  make dev-web         Start the Next.js app once apps/web is initialized"
	@echo "  make dev-api         Start the FastAPI app once apps/api is initialized"
	@echo "  make test            Run backend and frontend tests once configured"
	@echo "  make lint            Run lint checks once configured"
	@echo "  make format-check    Check formatting once configured"
	@echo "  make docker-up       Start Docker Compose services"
	@echo "  make docker-down     Stop Docker Compose services"
	@echo "  make docker-config   Validate Docker Compose configuration"
	@echo "  make clean-cache     Remove common generated caches"

dev: docker-up

dev-web:
	@if [ -f apps/web/package.json ]; then cd apps/web && npm run dev; else echo "apps/web is scaffolded but not initialized yet. Day 2 adds the Next.js app."; fi

dev-api:
	@if [ -f apps/api/pyproject.toml ]; then cd apps/api && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000; else echo "apps/api is scaffolded but not initialized yet. Day 4 adds the FastAPI app."; fi

test:
	@echo "Tests will be added gradually starting with backend service tests."

lint:
	@echo "Lint tooling will be configured as app packages are initialized."

format-check:
	@echo "Format checks will be configured as app packages are initialized."

docker-up:
	docker compose up --build

docker-down:
	docker compose down

docker-config:
	docker compose config

clean-cache:
	@echo "Remove generated caches manually until app tooling is initialized."

