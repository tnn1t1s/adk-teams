from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.parent


def file_read(file_path: str) -> dict:
    """Reads a file from the repository.

    Args:
        file_path: Path relative to the repository root.

    Returns:
        dict: status and file contents, or error if file not found.
    """
    target = (REPO_ROOT / file_path).resolve()

    if not target.is_relative_to(REPO_ROOT):
        return {"status": "error", "error": f"Path escapes repository root: {file_path}"}

    if not target.exists():
        return {"status": "error", "error": f"File not found: {file_path}"}

    if not target.is_file():
        return {"status": "error", "error": f"Not a file: {file_path}"}

    return {"status": "success", "file_path": file_path, "content": target.read_text()}
