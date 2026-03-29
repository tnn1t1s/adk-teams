# adk-teams

A reusable framework for building multi-agent critique fleets using [Google ADK](https://pypi.org/project/google-adk/).

## The Pattern

A fleet of independent agents, each embodying a distinct professional persona, reviews the same artifact and posts structured disagreements to a shared channel. A human synthesizes the disagreements into decisions.

The value is not in any single agent's output. It is in the collision of perspectives and the human judgment applied to them.

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

Each agent produces `(challenge, evidence, recommendation)` tuples. The persona drives what challenges surface.

## Quick Start

```bash
# 1. Install
pip install -e .

# 2. Configure
cp .env.example .env
# Add your OPENROUTER_API_KEY and SERPER_API_KEY

# 3. Run an agent
cd agents && adk run example_fleet/senior_dev
```

## Example Fleet

Three agents forming a minimum viable tension triangle:

| Agent | Persona | Perspective |
|-------|---------|-------------|
| `senior_dev` | Senior IC, 8+ years | "Will I actually use this? What does this cost me per PR?" |
| `junior_dev` | 1-2 years, follows docs literally | "I followed the docs exactly and it didn't work." |
| `security` | AppSec engineer, assumes breach | "Where can credentials leak? What's the blast radius?" |

## A2A Agent Cards

Every agent directory includes an `agent-card.json` following the [A2A protocol](https://github.com/google/A2A) spec. These cards declare the agent's name, capabilities, and skills for future orchestrator discovery:

```json
{
  "name": "senior_dev",
  "description": "Senior software engineer reviewing artifacts...",
  "version": "1.0.0",
  "capabilities": {"streaming": false},
  "skills": [
    {
      "id": "critique",
      "name": "Document Critique",
      "description": "Reviews documentation and produces (challenge, evidence, recommendation) tuples"
    }
  ]
}
```

Agent cards enable an orchestrator to discover fleet members, understand their capabilities, and route review tasks to appropriate agents.

## Collaboration Platforms

The collaboration tools delegate to a backend selected by the `COLLABORATION_PLATFORM` env var:

| Platform | Backend | Use case |
|----------|---------|----------|
| `file` | Append-only JSONL | Development and testing |
| `discord` | Discord API | Production collaboration |
| `irc` | Stub | Planned — future A2A agent communication |

Set `COLLABORATION_PLATFORM=file` and read output with `cat .collaboration/<channel>.jsonl`.

## Building Your Own Fleet

1. Create a `base.yaml` with shared team context
2. Write persona `config.yaml` files — frustrations, values, incidents (no checklists)
3. Copy the `agent.py` pattern — load YAML, build system prompt, export `root_agent`
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
pytest tests/test_file_read.py tests/test_collab_post.py tests/test_collab_read.py
```
