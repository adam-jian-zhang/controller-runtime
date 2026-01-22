.PHONY: help process build serve clean docker-build docker-run generate-svgs all

PYTHON := python3
HUGO := hugo
DOCKER := docker
PORT := 9005

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

generate-svgs: ## Generate SVG files from Mermaid diagrams (REQUIRED)
	@echo "Generating SVG files from Mermaid diagrams..."
	@node scripts/convert-mermaid-node.js || true

process: generate-svgs ## Process markdown files and embed SVGs
	@echo "Processing documentation..."
	@$(PYTHON) scripts/process.py

build: process ## Build the Hugo site
	@echo "Building Hugo site..."
	@$(HUGO) -d public

serve: process ## Serve the site locally with Hugo
	@echo "Starting Hugo server on port $(PORT)..."
	@$(HUGO) server -p $(PORT) --bind 0.0.0.0

clean: ## Clean generated files
	@echo "Cleaning..."
	@rm -rf public content/docs content/_index.md static/images/diagrams

docker-build: build ## Build Docker image
	@echo "Building Docker image..."
	@$(DOCKER) build -t controller-runtime-docs:latest -f Dockerfile .

docker-run: ## Run Docker container
	@echo "Running Docker container on port $(PORT)..."
	@$(DOCKER) run -d -p $(PORT):$(PORT) --name controller-runtime-docs controller-runtime-docs:latest

docker-stop: ## Stop Docker container
	@$(DOCKER) stop controller-runtime-docs || true
	@$(DOCKER) rm controller-runtime-docs || true

all: clean build ## Clean and build everything

.DEFAULT_GOAL := help
