# Getting Started

## Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) or pip for package management
- OpenRouter account (API key for model routing)
- Serper account (API key for web search)

## Setup

```bash
git clone https://github.com/tnn1t1s/adk-teams.git
cd adk-teams

# Install dependencies
pip install -e .

# Configure environment
cp .env.example .env
# Edit .env with your API keys
```

## Run an agent

```bash
cd agents && adk run example_fleet/senior_dev
```

Or with a replay file for batch review:

```bash
cat > /tmp/review.json << 'EOF'
{
  "state": {},
  "queries": ["Review the following documentation.\n\n<paste your docs here>\n\nPost your critique to channel 'senior-dev-review' with agent_name 'senior_dev'."]
}
EOF

cd agents && adk run --replay /tmp/review.json example_fleet/senior_dev
```

## Run tests

```bash
# All tests (requires SERPER_API_KEY in .env)
pytest

# Just the collaboration and file tests (no API key needed)
pytest tests/test_file_read.py tests/test_collab_post.py tests/test_collab_read.py
```

## Start with 3 personas

The minimum viable tension triangle: `senior_dev`, `junior_dev`, `security`.

- **senior_dev** — values simplicity, hates ceremony, remembers the last migration that went wrong
- **junior_dev** — follows docs literally, surfaces ambiguity and missing steps
- **security** — assumes breach, reads every auth flow, asks about blast radius

These three disagree on nearly everything. That's the point.

## Read the output

```bash
cat .collaboration/<channel>.jsonl
```

Each line is a JSON object with `timestamp`, `agent`, and `message`.

## Tune the personas

If output feels generic, the persona isn't specific enough. Add more frustrations and incidents to the config.yaml. The specificity of the persona drives the specificity of the critique.

## Add more personas

After the initial three produce useful output, consider adding:
- **architect** — thinks in systems, 3-year maintainability horizon
- **devops** — owns the pipeline and the 2am pages
- **pm** — owns roadmap and headcount, asks about adoption cost
- **qa** — thinks in edge cases and failure modes

Each addition should surface new types of critique. If an agent's output overlaps significantly with an existing agent, the persona isn't differentiated enough.
