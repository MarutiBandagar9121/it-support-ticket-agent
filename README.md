# IT Support Ticket Agent

A learning project exploring LangChain tool-calling by building an agent over a synthetic IT support ticket dataset. The agent is wired up manually (`ChatOpenAI` + `bind_tools` + a hand-rolled message loop) rather than through a prebuilt agent framework, to understand the underlying mechanics before adding abstraction.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and add your [OpenRouter](https://openrouter.ai/) API key:

```bash
cp .env.example .env
# then edit .env and set OPEN_ROUTER_API_KEY
```

## Data

The dataset is [ahsanneural/synthetic-it-support-tickets](https://www.kaggle.com/datasets/ahsanneural/synthetic-it-support-tickets) on Kaggle. Download it with:

```bash
python get_kaggle_dataset.py
```

This populates `data/raw/tickets.csv`. A processed sample used by the scripts lives at `data/processed/sample_5000.csv`. The `data/` directory is gitignored, so you'll need to run the download yourself.

## Usage

```bash
python agent.py   # runs the LangChain tool-calling agent
python main.py     # loads and inspects the ticket data
```

## Project structure

- `config.py` — loads environment variables and exposes app settings
- `data_utils.py` — shared ticket-loading/dtype logic
- `tools.py` — LangChain tools available to the agent
- `agent.py` — the LLM + tool-calling wiring
- `get_kaggle_dataset.py` — downloads the raw dataset from Kaggle

See `CLAUDE.md` for a deeper architecture walkthrough.
