from adk_teams.tools import collab_post


def test_collab_post_creates_message():
    result = collab_post("test-channel", "Hello from tests", agent_name="test_agent")
    assert result["status"] == "success"
    assert result["channel"] == "test-channel"


def test_collab_post_default_agent_name():
    result = collab_post("test-channel-default", "Hello with default agent")
    assert result["status"] == "success"
