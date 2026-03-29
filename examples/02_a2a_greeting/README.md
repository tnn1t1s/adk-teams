# 02 — A2A Greeting

Two agents that coordinate via the collaboration platform before responding.

## What this teaches

- Agent-to-agent communication via `collab_post` and `collab_read`
- Sequential agent execution (planner before greeter)
- Reading another agent's output from a shared channel

## Agents

| Agent | Role | Tools |
|-------|------|-------|
| `planner` | Decides greeting style, posts plan to `greeting-plan` channel | `collab_post` |
| `greeter` | Reads planner's recommendation, greets in that style | `collab_read` |

## Run

```bash
pip install -e ../..
chmod +x run.sh
./run.sh
```

Or manually:

```bash
cd agents
adk run --replay ../planner-input.json planner
adk run --replay ../greeter-input.json greeter
```
