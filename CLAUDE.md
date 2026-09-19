# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project purpose

A learning project for building a LangChain-based agent over an IT support ticket dataset. The agent is being wired up manually and incrementally (raw `ChatOpenAI` + `bind_tools` + a hand-rolled message loop) rather than via a prebuilt framework agent, so each mechanic (tool schema generation, tool-call parsing, `ToolMessage` round-tripping) is understood before adding abstraction.

## Setup and commands

- Virtualenv lives at `.venv/`. Activate with `source .venv/bin/activate`.
- Dependencies are managed via `requirements.in` (top-level deps) compiled to `requirements.txt` (pinned, via `pip-compile`). After editing `requirements.in`, regenerate with:
  ```
  pip-compile --no-index
  ```
  then `pip install -r requirements.txt`.
- Run any script directly, e.g. `python agent.py`, `python main.py`.
- `.env` holds `OPEN_ROUTER_API_KEY` (see `.env.example` for the shape). It is gitignored — never commit real keys.
- There is no test suite, linter, or build step configured yet.

## Architecture

**Config loading (`config.py`)**: calls `dotenv.load_dotenv()` at import time, then builds a module-level `settings = Config()` singleton. Every other file imports the same instance via `from config import settings` and reads `settings.open_router_api_key`. Because Python caches modules, the env loading and key lookup happen exactly once regardless of how many files import `settings`.

**LLM provider**: OpenRouter (OpenAI-compatible API), accessed through `langchain_openai.ChatOpenAI` with `base_url="https://openrouter.ai/api/v1"` and `api_key=settings.open_router_api_key`. The model slug (e.g. `deepseek/deepseek-v4-flash-0731`) is currently hardcoded per-script and swapped manually while experimenting with free/cheap OpenRouter models — there's no central model config yet.

**Data layer (`data_utils.py`)**: `load_tickets(path)` is the single entry point for reading the ticket CSV — it sets categorical dtypes on a fixed list of columns (`customer_segment`, `channel`, `product_area`, `issue_type`, `priority`, `status`, `sla_plan`, `customer_sentiment`, `platform`, `region`) and parses `created_at` as datetime. Any new code that reads ticket data should go through this function rather than calling `pd.read_csv` directly, to keep dtypes consistent.

- `data/raw/` holds the untouched dataset (populated by `get_kaggle_dataset.py`, which pulls `ahsanneural/synthetic-it-support-tickets` from Kaggle via `kagglehub`).
- `data/processed/sample_5000.csv` is the working sample most scripts (`tools.py`, `main.py`) currently point at.
- The whole `data/` directory is gitignored — datasets are not committed.

**Tools (`tools.py`)**: LangChain tools are plain functions decorated with `@tool` from `langchain.tools`. The function's docstring is sent to the LLM verbatim as the tool's description and is load-bearing — it's how the model learns valid argument values (e.g. the fixed `priority` values are spelled out in the docstring, not just in code). Tools that filter the ticket DataFrame do exact-match filtering; they do not validate or normalize arguments themselves, so correctness currently depends on the model passing values that match the docstring's stated options.

**Agent loop (`agent.py`)**: the manual tool-calling pattern used throughout this project:
1. Send `[HumanMessage(...)]` to `llm.bind_tools(tools)`.
2. Check `ai_msg.tool_calls` — if populated, look up each tool by name in a `tools_by_name` dict, invoke it with the model-provided args, and append a `ToolMessage(content=result, tool_call_id=...)` for each.
3. Re-invoke the model with the full message history to get the final natural-language answer.

When extending this file or adding new agent scripts, follow this same explicit loop shape (rather than switching to `create_react_agent` or another prebuilt abstraction) unless asked to graduate to one — the project's stated goal is understanding the underlying mechanics first.
