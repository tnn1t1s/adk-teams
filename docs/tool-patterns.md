# Tool Patterns

Design principles for ADK agent tools.

## Two categories of failure

### Config errors → crash at import

Missing env vars, bad config files — these crash the process immediately. The agent should never start if its configuration is broken.

```python
SERPER_API_KEY = os.environ["SERPER_API_KEY"]  # KeyError if missing → good
```

### Runtime errors → return error dicts

File not found, HTTP errors, bad input — these return error dicts so the agent can adapt.

```python
if not target.exists():
    return {"status": "error", "error": f"File not found: {file_path}"}
```

ADK propagates tool exceptions as process kills. If `file_read` raises `AssertionError`, the entire agent crashes — no critique posted, no partial output saved.

## Return format

All tools return dicts with a `status` field:

```python
# Success
{"status": "success", "channel": "review", "messages": [...]}

# Error
{"status": "error", "error": "Channel not found: review"}
```

## Tool inventory

| Tool | Purpose | Env vars |
|------|---------|----------|
| `file_read` | Read artifacts from the repository | None |
| `web_search` | Search via Serper for evidence | `SERPER_API_KEY` |
| `collab_post` | Post to a collaboration channel | `COLLABORATION_PLATFORM` |
| `collab_read` | Read from a collaboration channel | `COLLABORATION_PLATFORM` |

## Collaboration platform

The collab tools delegate to a `CollaborationPlatform` backend selected by the `COLLABORATION_PLATFORM` env var:

| Value | Backend | Use case |
|-------|---------|----------|
| `file` | Append-only JSONL files | Development, testing |
| `discord` | Discord API | Production collaboration |
| `irc` | Stub (not yet implemented) | Future A2A communication |

The factory pattern (GoF) in `collaboration/factory.py` reads the env var and returns the appropriate backend. Tools use lazy initialization — the platform is created on first use.

## Adding a new tool

1. Create `agents/tools/<tool_name>.py` with a single function
2. Read env vars at module level via `os.environ["KEY"]` (fail fast)
3. Return dicts from the function (never raise on runtime errors)
4. Add to `agents/tools/__init__.py` exports
5. Add to each agent's `tools=[...]` list
6. Write an integration test in `tests/test_<tool_name>.py`

## Adding a new collaboration platform

1. Create `agents/tools/collaboration/<name>_platform.py`
2. Implement the `CollaborationPlatform` ABC
3. Add a branch in `factory.py` for the new platform type
4. Test with `COLLABORATION_PLATFORM=<name>`
