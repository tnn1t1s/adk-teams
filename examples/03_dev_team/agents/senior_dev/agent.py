from pathlib import Path

from dotenv import load_dotenv
load_dotenv(Path(__file__).parent / ".env")

from adk_teams import build_persona_prompt
from adk_teams.tools import file_read, web_search, collab_post, collab_read
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

prompt = build_persona_prompt(
    base_path=Path(__file__).parent.parent / "developer" / "base.yaml",
    config_path=Path(__file__).parent / "config.yaml",
)

root_agent = Agent(
    name="senior_dev",
    model=LiteLlm(model="openrouter/anthropic/claude-sonnet-4"),
    instruction=prompt,
    tools=[file_read, web_search, collab_post, collab_read],
)
