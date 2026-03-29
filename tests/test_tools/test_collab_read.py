from adk_teams.tools import collab_post, collab_read


def test_collab_read_after_post():
    collab_post("read-test-channel", "First message", agent_name="agent_a")
    collab_post("read-test-channel", "Second message", agent_name="agent_b")

    result = collab_read("read-test-channel")
    assert result["status"] == "success"
    assert len(result["messages"]) == 2
    assert result["messages"][0]["agent"] == "agent_a"
    assert result["messages"][1]["agent"] == "agent_b"


def test_collab_read_nonexistent_channel():
    result = collab_read("nonexistent-channel")
    assert result["status"] == "error"
    assert "not found" in result["error"].lower()


def test_collab_read_with_limit():
    for i in range(5):
        collab_post("limit-test-channel", f"Message {i}", agent_name="agent")

    result = collab_read("limit-test-channel", limit=2)
    assert result["status"] == "success"
    assert len(result["messages"]) == 2
