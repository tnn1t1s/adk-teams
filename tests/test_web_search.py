from tools import web_search


def test_web_search_returns_results():
    result = web_search("Python ADK agent framework", num_results=3)
    assert result["status"] == "success"
    assert len(result["results"]) > 0
    assert "title" in result["results"][0]
    assert "link" in result["results"][0]
