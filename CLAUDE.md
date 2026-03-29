# CLAUDE.md — adk-teams

## Project Context

adk-teams is a standalone, reusable framework for building multi-agent critique fleets using Google ADK. Agents embody professional personas, review artifacts, and post structured disagreements to a shared collaboration channel. A human synthesizes the output.

## Repository Layout

```
adk-teams/
  adk_teams/                        # core package — primitives, ABCs, factories
    persona.py                      # build_persona_prompt(): YAML → system prompt
    tools/                          # shared tools
      collaboration/                # GoF Factory for platform backends
  examples/
    01_hello/                       # simplest agent — no tools, no inheritance
    02_a2a_greeting/                # two agents coordinating via collab channel
    03_dev_team/                    # full critique fleet (senior_dev, junior_dev, security)
  tests/
    test_tools/                     # core tool tests
    test_e2e/                       # E2E tests per example
  docs/                             # guides
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

- **Never use `sys.path.insert`** — `pyproject.toml` sets `pythonpath = ["."]`.
- **Never call `load_dotenv` in test code** — `pytest-dotenv` handles it.
- Agent code uses `from adk_teams.tools import file_read, web_search, collab_read, collab_post`.
- Agent code uses `from adk_teams import build_persona_prompt`.

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

# Single agent (example: 03_dev_team)
cd examples/03_dev_team/agents && adk run senior_dev

# Simplest agent
cd examples/01_hello/agents && adk run greeter
```
