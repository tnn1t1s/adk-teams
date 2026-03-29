# Persona Design

How to write agent personas that produce useful critique.

## Persona-driven, not checklist-driven

The most important lesson from the reference implementation: describe WHO the person is, not WHAT they should check.

### Don't do this

```yaml
evaluation_criteria:
  - "What is the measured latency overhead?"
  - "Are access controls enforced?"
  - "Can decisions be audited?"
```

Checklist agents find exactly what you tell them to find. The output is predictable and useless — you're reading your own assumptions back to yourself.

### Do this

```yaml
frustrations:
  - "New tools always claim zero overhead but the build is 30 seconds slower"
  - "Architecture docs describe the ideal state, not what we actually have"

values:
  optimizes_for:
    - Simplicity — if a junior can't understand it, it's too complex
    - Small blast radius — changes should be reversible
```

Persona agents react to what matters to THEM. The critique emerges from the collision of persona and document.

## Config structure

Every persona config has these sections:

- **identity** — title, seniority, who they are professionally
- **work** — what they do daily, a typical project description
- **frustrations** — specific complaints from lived experience (quoted strings)
- **values** — what they optimize for, tolerate, and reject
- **context** — incidents they remember, regulatory awareness

The base.yaml provides shared context (company type, team, tools, environment). Each agent's config.yaml provides persona-specific overrides.

## Seniority splits

The same role at different seniority levels produces completely different output. Use YAML inheritance:

```
developer/
  base.yaml          # shared: company, team, tools, tech stack
senior_dev/
  config.yaml        # overrides: 8+ years, simplicity-first, migration trauma
junior_dev/
  config.yaml        # overrides: 1-2 years, follows docs literally, hasn't been burned
```

The merge in agent.py is a shallow dict merge — specialization overrides base.

## Design for productive tension

Every persona should disagree with at least one other persona on something real. If two personas always agree, one is redundant.

| Tension | Agent A | Agent B |
|---------|---------|---------|
| Simplicity vs security controls | senior_dev | security |
| Speed vs documentation quality | senior_dev | junior_dev |
| Move fast vs assume breach | junior_dev | security |

## Don't lead the prompt

The user message should be neutral: "Review the following documentation." All persona context lives in the system prompt. If you tell the agent what to complain about in the user message, you've defeated the purpose.

## Human in the loop is essential

Without human judgment, the fleet manufactures garbage. The fleet generates critique surface area. The human decides what's signal. Every fleet needs a designated synthesizer who reads all output and decides: accept, dismiss, or reframe.
