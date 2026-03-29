# CLAUDE.md — adk-teams

## Project Context

adk-teams is a standalone, reusable framework for building multi-agent critique fleets using Google ADK. Agents embody professional personas, review artifacts, and post structured disagreements to a shared collaboration channel. A human synthesizes the output.

## Repository Layout

```
adk-teams/
  agents/
    tools/                      # shared tools — all agents import from here
      collaboration/            # GoF Factory for platform backends
    example_fleet/              # 3 example agents (senior_dev, junior_dev, security)
      developer/base.yaml       # shared dev team identity
  tests/                        # integration tests
  docs/                         # guides
```

## Rules

### Persona configs

- **Persona-driven only** — describe who the person is (frustrations, values, incidents). Never use `evaluation_criteria` checklists.
- Config format: `identity`, `work`, `frustrations`, `values`, `context` sections.
- Seniority splits use YAML inheritance: base.yaml + config.yaml with shallow merge.

### Tools

- Tools return dicts, never raise exceptions on runtime errors.
- Config errors (missing env vars) crash at import time — that's fail-fast on configuration.
- Runtime errors (HTTP failures, file not found) return `{"status": "error", "error": "..."}`.

### Imports

- **Never use `sys.path.insert`** — `pyproject.toml` sets `pythonpath = [".", "agents"]`.
- **Never call `load_dotenv` in test code** — `pytest-dotenv` handles it.
- Agent code uses `from tools import file_read, web_search, collab_read, collab_post`.

### Environment

- Always use dotenv for env vars.
- Never expose API keys in conversation, code, or logs.
- `COLLABORATION_PLATFORM=file` for testing, `=discord` for production.

### Testing

- No mocks, no monkeypatch — integration tests hit real services.
- `conftest.py` sets `COLLABORATION_FILE_DIR` to a temp path.
- `web_search` tests require `SERPER_API_KEY`.

### Running

```bash
# Tests
pytest

# Single agent
cd agents && adk run example_fleet/senior_dev
```
