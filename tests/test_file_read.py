from tools import file_read


def test_file_read_success():
    result = file_read("pyproject.toml")
    assert result["status"] == "success"
    assert "adk-teams" in result["content"]


def test_file_read_not_found():
    result = file_read("nonexistent-file.md")
    assert result["status"] == "error"
    assert "not found" in result["error"].lower()


def test_file_read_path_escape():
    result = file_read("../../etc/passwd")
    assert result["status"] == "error"
    assert "escapes" in result["error"].lower()


def test_file_read_directory():
    result = file_read("agents")
    assert result["status"] == "error"
    assert "not a file" in result["error"].lower()
