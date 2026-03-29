from pathlib import Path

from adk_teams import build_persona_prompt


def test_hello_persona_loads():
    config_path = Path(__file__).parent.parent.parent / "examples" / "01_hello" / "agents" / "greeter" / "config.yaml"
    prompt = build_persona_prompt(config_path=config_path)
    assert "Friendly Greeter" in prompt
    assert "Enthusiastic and warm" in prompt
    assert "Making people smile" in prompt
