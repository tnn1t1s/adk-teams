from pathlib import Path

from adk_teams import build_persona_prompt


EXAMPLES_DIR = Path(__file__).parent.parent.parent / "examples" / "02_a2a_greeting" / "agents"


def test_planner_persona_loads():
    prompt = build_persona_prompt(config_path=EXAMPLES_DIR / "planner" / "config.yaml")
    assert "Greeting Planner" in prompt
    assert "greeting style" in prompt.lower()


def test_greeter_persona_loads():
    prompt = build_persona_prompt(config_path=EXAMPLES_DIR / "greeter" / "config.yaml")
    assert "Friendly Greeter" in prompt
    assert "greeting-plan" in prompt
