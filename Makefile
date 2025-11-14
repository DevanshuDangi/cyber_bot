.PHONY: help setup install start stop clean test

help: ## Show this help message
	@echo "1930 Cyber Crime Helpline WhatsApp Chatbot - Makefile Commands"
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-15s %s\n", $$1, $$2}'

setup: ## Run automated setup (creates venv, installs dependencies)
	@echo "Running automated setup..."
	@chmod +x setup.sh
	@./setup.sh

install: setup ## Alias for setup

start: ## Start both backend and frontend servers
	@echo "Starting servers..."
	@chmod +x start.sh
	@./start.sh

stop: ## Stop all running servers
	@echo "Stopping servers..."
	@pkill -f "uvicorn backend.main:app" || true
	@pkill -f "vite" || true
	@echo "Servers stopped"

clean: ## Clean up generated files and caches
	@echo "Cleaning up..."
	@rm -rf venv
	@rm -rf admin-ui/node_modules
	@rm -rf admin-ui/dist
	@rm -rf __pycache__
	@rm -rf backend/__pycache__
	@rm -f *.log
	@rm -f chatbot.db
	@echo "Cleanup complete"

test: ## Run tests (if available)
	@echo "Running tests..."
	@echo "Tests not yet implemented"

dev: ## Start development servers with auto-reload
	@echo "Starting development servers..."
	@make start

backend: ## Start only backend server
	@echo "Starting backend server..."
	@source venv/bin/activate && uvicorn backend.main:app --reload --port 8000

frontend: ## Start only frontend server
	@echo "Starting frontend server..."
	@cd admin-ui && npm run dev

