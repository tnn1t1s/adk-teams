from pathlib import Path

import yaml


def build_persona_prompt(config_path: Path, base_path: Path | None = None) -> str:
    """Load persona config (with optional base inheritance) and return system prompt."""
    spec = yaml.safe_load(config_path.read_text())

    if base_path:
        base = yaml.safe_load(base_path.read_text())
        persona = {**base["persona"], **spec["persona"]}
        persona["identity"] = {**base["persona"].get("identity", {}), **spec["persona"].get("identity", {})}
        if "environment" in base["persona"]:
            persona["environment"] = base["persona"]["environment"]
        if "context" in base["persona"] or "context" in spec["persona"]:
            persona["context"] = {**base["persona"].get("context", {}), **spec["persona"].get("context", {})}
    else:
        persona = spec["persona"]

    sections = []

    identity = persona.get("identity", {})
    title = identity.get("title", "Agent")
    company_type = identity.get("company_type")
    seniority = identity.get("seniority")
    reports_to = identity.get("reports_to")
    team = identity.get("team")

    header = f"You are a {title}"
    if company_type:
        header += f" at a {company_type}"
    header += "."
    sections.append(header)
    if seniority:
        sections.append(f"You are {seniority}")
    if reports_to and team:
        sections.append(f"You report to {reports_to} on the {team} team.")

    work = persona.get("work")
    if work:
        parts = [f"## Your Work\n{work['description']}"]
        if "daily_activities" in work:
            activities = "\n".join(f"- {a}" for a in work["daily_activities"])
            parts.append(f"### What You Do Every Day\n{activities}")
        if "typical_project" in work:
            parts.append(f"### A Typical Project\n{work['typical_project']}")
        sections.append("\n\n".join(parts))

    env = persona.get("environment")
    if env:
        lines = []
        for key in ("languages", "tools"):
            if key in env:
                lines.append(f"- {key.title()}: {', '.join(env[key])}")
        for key in ("infrastructure", "observability", "agents"):
            if key in env:
                lines.append(f"- {key.title()}: {env[key]}")
        if lines:
            sections.append("## Your Environment\n" + "\n".join(lines))

    frustrations = persona.get("frustrations")
    if frustrations:
        items = "\n".join(f"- {f}" for f in frustrations)
        sections.append(f"## What Frustrates You\n{items}")

    values = persona.get("values")
    if values:
        parts = []
        for label, key in [("You optimize for:", "optimizes_for"), ("You tolerate:", "tolerates"), ("You reject:", "rejects")]:
            if key in values:
                items = "\n".join(f"- {v}" for v in values[key])
                parts.append(f"{label}\n{items}")
        if parts:
            sections.append("## What You Value\n" + "\n\n".join(parts))

    context = persona.get("context")
    if context:
        if "regulatory_awareness" in context:
            sections.append(f"## Your Relationship With Compliance\n{context['regulatory_awareness']}")
        if "incidents_they_remember" in context:
            items = "\n".join(f"- {i}" for i in context["incidents_they_remember"])
            sections.append(f"## Things That Have Gone Wrong\n{items}")

    task = persona.get("task")
    if task:
        sections.append(f"## Your Task\n{task}")

    tool_usage = persona.get("tool_usage")
    if tool_usage:
        sections.append(f"## Tool Usage\n{tool_usage}")

    return "\n\n".join(sections)
