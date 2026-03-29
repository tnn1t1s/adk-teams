import json
import os
import subprocess
from pathlib import Path

import pytest

OPENROUTER_KEY = os.environ.get("OPENROUTER_API_KEY", "")

REPO_ROOT = Path(__file__).parent.parent.parent
AGENTS_DIR = REPO_ROOT / "examples" / "03_dev_team" / "agents"
ADK_BIN = REPO_ROOT / ".venv" / "bin" / "adk"


@pytest.mark.skipif(not OPENROUTER_KEY, reason="OPENROUTER_API_KEY not set — skipping paid E2E test")
def test_senior_dev_e2e(tmp_path):
    replay = tmp_path / "replay.json"
    replay.write_text(json.dumps({
        "state": {},
        "queries": [
            "Review the following document: "
            "Viper is a Python environment management tool that creates "
            "deterministic environments from frozen tags. "
            "Post your critique to channel e2e-test "
            "with agent_name senior_dev."
        ],
    }))

    collab_dir = tmp_path / "collaboration"

    env = {
        **os.environ,
        "COLLABORATION_PLATFORM": "file",
        "COLLABORATION_FILE_DIR": str(collab_dir),
        "PYTHONPATH": str(REPO_ROOT),
    }

    result = subprocess.run(
        [str(ADK_BIN), "run", "--replay", str(replay), "senior_dev"],
        cwd=str(AGENTS_DIR),
        env=env,
        capture_output=True,
        text=True,
        timeout=120,
    )

    assert result.returncode == 0, f"adk exited {result.returncode}\nstderr: {result.stderr}"

    channel_file = collab_dir / "e2e-test.jsonl"
    assert channel_file.exists(), (
        f"No collaboration file at {channel_file}\n"
        f"collab_dir contents: {list(collab_dir.iterdir()) if collab_dir.exists() else 'dir missing'}\n"
        f"stdout: {result.stdout[-500:]}"
    )

    lines = [l for l in channel_file.read_text().splitlines() if l.strip()]
    assert len(lines) >= 1, "Expected at least one message in channel file"

    entry = json.loads(lines[0])
    assert entry["agent"] == "senior_dev"
    assert entry["timestamp"]
    assert len(entry["message"]) > 0


def test_persona_merge():
    from adk_teams import build_persona_prompt

    prompt = build_persona_prompt(
        base_path=AGENTS_DIR / "developer" / "base.yaml",
        config_path=AGENTS_DIR / "senior_dev" / "config.yaml",
    )

    assert "Senior Software Engineer" in prompt
    assert "Mid-to-large SaaS" in prompt
    assert "8+ years" in prompt
    assert "Simplicity" in prompt
    assert "ORM migration" in prompt
    assert "SOC 2" in prompt
