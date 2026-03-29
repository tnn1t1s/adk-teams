# adk-teams

A reusable framework for building multi-agent critique fleets using [Google ADK](https://pypi.org/project/google-adk/).

## The Pattern

A fleet of independent agents, each embodying a distinct professional persona, reviews the same artifact and posts structured disagreements to a shared channel. A human synthesizes the disagreements into decisions.

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  senior_dev  │     │  junior_dev  │     │  security    │
│  config.yaml │     │  config.yaml │     │  config.yaml │
│  agent.py    │     │  agent.py    │     │  agent.py    │
└──────┬───────┘     └──────┬───────┘     └──────┬───────┘
       │                    │                    │
       ▼                    ▼                    ▼
   ┌────────┐          ┌────────┐          ┌────────┐
   │ Tools  │          │ Tools  │          │ Tools  │
   └────┬───┘          └────┬───┘          └────┬───┘
        │                   │                   │
        └───────────┬───────┴───────────────────┘
                    ▼
          ┌─────────────────┐
          │  Collaboration   │
          │  Channel (JSONL) │
          └────────┬─────────┘
                   ▼
          ┌─────────────────┐
          │  Human           │
          │  Synthesizer     │
          └─────────────────┘
```

## Quick Start

```bash
# 1. Install
pip install -e .

# 2. Configure
cp .env.example .env
# Add your OPENROUTER_API_KEY and SERPER_API_KEY

# 3. Run the simplest example
cd examples/01_hello/agents && adk run greeter
```

## Examples

| # | Example | What it teaches |
|---|---------|-----------------|
| [01](examples/01_hello/) | Hello | Simplest agent — one persona, no tools, no inheritance |
| [02](examples/02_a2a_greeting/) | A2A Greeting | Two agents coordinating via collaboration channel |
| [03](examples/03_dev_team/) | Dev Team | Full critique fleet with YAML inheritance and all tools |

### 03 — Dev Team Critique Fleet

Three agents forming a minimum viable tension triangle:

| Agent | Persona | Perspective |
|-------|---------|-------------|
| `senior_dev` | Senior IC, 8+ years | "Will I actually use this? What does this cost me per PR?" |
| `junior_dev` | 1-2 years, follows docs literally | "I followed the docs exactly and it didn't work." |
| `security` | AppSec engineer, assumes breach | "Where can credentials leak? What's the blast radius?" |

```bash
cd examples/03_dev_team/agents && adk run senior_dev
```

## Core Package: `adk_teams`

```python
from adk_teams import build_persona_prompt
from adk_teams.tools import file_read, web_search, collab_post, collab_read
```

- **`build_persona_prompt(config_path, base_path=None)`** — loads YAML persona config, merges with optional base, returns system prompt string
- **Tools** — `file_read`, `web_search`, `collab_post`, `collab_read`
- **Collaboration platforms** — file (JSONL), Discord, IRC (stub)

## Building Your Own Fleet

1. Create a `config.yaml` with persona sections: identity, work, frustrations, values, context
2. Optionally create a `base.yaml` for shared team context
3. Write a minimal `agent.py`:

```python
from pathlib import Path
from adk_teams import build_persona_prompt
from adk_teams.tools import file_read, web_search, collab_post, collab_read
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

prompt = build_persona_prompt(
    base_path=Path(__file__).parent.parent / "team" / "base.yaml",
    config_path=Path(__file__).parent / "config.yaml",
)

root_agent = Agent(
    name="my_agent",
    model=LiteLlm(model="openrouter/anthropic/claude-sonnet-4"),
    instruction=prompt,
    tools=[file_read, web_search, collab_post, collab_read],
)
```

4. Add an `agent-card.json` for A2A discovery
5. Run with `adk run` and tune personas until output is specific

See [docs/persona-design.md](docs/persona-design.md) for detailed guidance.

## Documentation

- [Persona Design](docs/persona-design.md) — how to write personas that produce useful critique
- [Tool Patterns](docs/tool-patterns.md) — tool design, error handling, adding new tools
- [Getting Started](docs/getting-started.md) — setup, running agents, tuning output

## Testing

```bash
# All tests (requires SERPER_API_KEY)
pytest

# File and collaboration tests only (no API key needed)
pytest tests/test_tools/test_file_read.py tests/test_tools/test_collab_post.py tests/test_tools/test_collab_read.py
```
