.DEFAULT_GOAL := help

.PHONY: help sync ingest chatbot evaluator evaluate visualize lint format imports fix

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2}'

sync: ## Install/update dependencies from uv.lock
	uv sync

ingest: ## Chunk and embed knowledge-base/ into the vector DB
	uv run python -m tmay_chatbot.app.cli.ingestor

chatbot: ## Launch the chatbot Gradio app
	uv run python -m tmay_chatbot.app.gradio.chatbot

evaluator: ## Launch the evaluator Gradio dashboard
	uv run python -m tmay_chatbot.app.gradio.evaluator

evaluate: ## Run a single evaluation test row, e.g. make evaluate N=3
ifndef N
	$(error N is not set. Usage: make evaluate N=<test_row_number>)
endif
	uv run python -m tmay_chatbot.app.cli.evaluator $(N)

visualize: ## Visualize knowledge-base embeddings with Plotly
	uv run python -m tmay_chatbot.app.plotly.visualizer

lint: ## Check code with ruff (no changes)
	uv run ruff check .

format: ## Format code with ruff
	uv run ruff format .

imports: ## Sort imports and remove unused ones with ruff
	uv run ruff check --select I --fix .

fix: ## Auto-fix lint issues (incl. imports) and format code
	uv run ruff check --fix .
	uv run ruff format .
