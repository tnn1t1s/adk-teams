# 03 — Dev Team Critique Fleet

Full multi-agent critique fleet with three personas forming a tension triangle.

## What this teaches

- YAML persona inheritance (base.yaml + config.yaml)
- Using all four tools (file_read, web_search, collab_post, collab_read)
- Multiple agents reviewing the same artifact from different perspectives
- Persona-driven critique (frustrations, values, incidents — not checklists)

## Agents

| Agent | Persona | Perspective |
|-------|---------|-------------|
| `senior_dev` | Senior IC, 8+ years | "Will I actually use this? What does this cost me per PR?" |
| `junior_dev` | 1-2 years, follows docs literally | "I followed the docs exactly and it didn't work." |
| `security` | AppSec engineer, assumes breach | "Where can credentials leak? What's the blast radius?" |

## Run

```bash
pip install -e ../..
cd agents && adk run senior_dev
```

Or with a replay file:

```bash
cat > /tmp/review.json << 'EOF'
{
  "state": {},
  "queries": ["Review the following documentation.\n\n<paste docs here>\n\nPost your critique to channel 'review' with agent_name 'senior_dev'."]
}
EOF

cd agents && adk run --replay /tmp/review.json senior_dev
```
