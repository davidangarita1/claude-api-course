# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
uv sync                          # install dependencies
uv run marimo edit notebooks/    # open all notebooks in the interactive editor
uv run marimo edit notebooks/<file>.py   # open a single notebook
uv run marimo run notebooks/<file>.py    # run a notebook headlessly
```

Environment variables required: copy `.env.example` to `.env` and fill in `ANTHROPIC_API_KEY` and `VOYAGE_API_KEY`.

## Architecture

Each file in `notebooks/` is a self-contained **marimo** notebook that demonstrates one Claude API feature. Marimo notebooks are plain Python files; cells are decorated with `@app.cell`. Dependencies between cells are declared via function parameters and return tuples — marimo builds a reactive DAG from these.

The standard pattern used across almost every notebook:

```python
@app.cell
def _(client, model):
    def add_user_message(messages, text): ...
    def add_assistant_message(messages, text): ...
    def chat(messages, system=None, tools=None, ...): ...
    return add_user_message, add_assistant_message, chat
```

`chat()` wraps `client.messages.create()`. Any notebook that passes `system=` or `tools=` to `chat()` applies `cache_control: ephemeral` to the last tool and to the system prompt content block — this is already wired in `caching.py` and `thinking_complete.py`.

### Notebook groups

| Group | Files |
|---|---|
| Core messaging | `multi_turn`, `system_prompts`, `streaming`, `temperature`, `structured_data` |
| Tool use | `tools`, `tools_007–009`, `tool_streaming_completed`, `text_editor_tool` |
| Vision / docs | `images`, `citations_complete`, `code_execution` |
| RAG | `chunking`, `embeddings`, `bm25`, `vectordb`, `hybrid` |
| Web search | `web_search_complete` |
| Thinking / caching | `thinking_complete`, `caching` |
| Prompt evaluation | `prompt_evals`, `prompt_evals_fns`, `prompt_evals_grader`, `prompting_completed` |

### RAG stack (`bm25`, `vectordb`, `hybrid`)

`BM25Index` — bag-of-words BM25 scorer. `add_document({"content": str})` → `search(query, k)`.

`VectorIndex` — cosine/euclidean nearest-neighbour over VoyageAI embeddings (`voyage-3-large`). `add_documents([{"content": str}])` → `search(query, k)`.

`Retriever` (in `hybrid.py`) — fuses both indexes with Reciprocal Rank Fusion (RRF).

### Prompt evaluation pattern (`prompt_evals_grader`, `prompting_completed`)

`generate_dataset()` → list of task dicts → `run_prompt(task)` → `grade_by_model(task, output)` → score + reasoning. `prompting_completed.py` extends this with `ThreadPoolExecutor` for parallel grading and HTML report generation.

### `@app.function` vs `@app.cell`

`@app.function` (used only on `chunk_by_char` in `chunking.py`) makes a function importable as a regular Python callable:

```python
from notebooks.chunking import chunk_by_char
```

All other definitions inside `@app.cell` are only accessible within the marimo reactive graph.

## Models in use

| Model | Used for |
|---|---|
| `claude-sonnet-4-6` | general notebooks (multi-turn, streaming, system prompts, …) |
| `claude-sonnet-4-5` | caching, thinking, citations, web search, code execution |
| `claude-haiku-4-5` | tool use notebooks, prompt evaluation |
