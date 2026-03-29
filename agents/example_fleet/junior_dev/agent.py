import json
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).parent / ".env")
from tools import file_read, web_search, collab_read, collab_post

import yaml
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

base_path = Path(__file__).parent.parent / "developer" / "base.yaml"
config_path = Path(__file__).parent / "config.yaml"
base = yaml.safe_load(base_path.read_text())
spec = yaml.safe_load(config_path.read_text())

persona = {**base["persona"], **spec["persona"]}
persona["identity"] = {**base["persona"]["identity"], **spec["persona"]["identity"]}
persona["environment"] = base["persona"]["environment"]
persona["context"] = {**base["persona"]["context"], **spec["persona"]["context"]}
model_cfg = base["model"]

frustrations = "\n".join(f"- {f}" for f in persona["frustrations"])
activities = "\n".join(f"- {a}" for a in persona["work"]["daily_activities"])
optimizes = "\n".join(f"- {v}" for v in persona["values"]["optimizes_for"])
tolerates = "\n".join(f"- {v}" for v in persona["values"]["tolerates"])
rejects = "\n".join(f"- {v}" for v in persona["values"]["rejects"])
incidents = "\n".join(f"- {i}" for i in persona["context"]["incidents_they_remember"])

system_prompt = f"""You are a {persona['identity']['title']} at a {persona['identity']['company_type']}.
You are {persona['identity']['seniority']}.
You report to {persona['identity']['reports_to']} on the {persona['identity']['team']} team.

## Your Work
{persona['work']['description']}

### What You Do Every Day
{activities}

### A Typical Project
{persona['work']['typical_project']}

## Your Environment
- Languages: {', '.join(persona['environment']['languages'])}
- Tools: {', '.join(persona['environment']['tools'])}
- Infrastructure: {persona['environment']['infrastructure']}
- Observability: {persona['environment']['observability']}
- Agents: {persona['environment']['agents']}

## What Frustrates You
{frustrations}

## What You Value
You optimize for:
{optimizes}

You tolerate:
{tolerates}

You reject:
{rejects}

## Your Relationship With Compliance
{persona['context']['regulatory_awareness']}

## Things That Have Gone Wrong
{incidents}

## Your Task
You are reviewing documentation for a tool or process that someone wants your team to adopt.
Read it as yourself — a newer engineer who takes docs at face value. If something is unclear,
confusing, or assumes context you don't have, say so. Your confusion is the signal.
Produce a list of (challenge, evidence, recommendation) tuples based on your real experience.

## Tool Usage
- **web_search**: Use short, specific queries (5-10 words). Never paste document content into a search query.
- **collab_post**: Post one consolidated critique per review, not multiple messages.
- **file_read**: Use relative paths from the repo root. Do NOT use file_read when documents are already provided in the message.

Do not adopt a reviewer persona. Do not be comprehensive. React to what confuses you.
"""

agent_card_path = Path(__file__).parent / "agent-card.json"
agent_card = json.loads(agent_card_path.read_text())

root_agent = Agent(
    name="junior_dev",
    model=LiteLlm(model=f"{model_cfg['provider']}/{model_cfg['name']}"),
    instruction=system_prompt,
    tools=[file_read, web_search, collab_read, collab_post],
)
