import json
from datetime import datetime, timezone
from pathlib import Path

from .platform import CollaborationPlatform


class FileCollaborationPlatform(CollaborationPlatform):

    def __init__(self, base_dir: str):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def _channel_path(self, channel: str) -> Path:
        return self.base_dir / f"{channel}.jsonl"

    def _roles_path(self, channel: str) -> Path:
        return self.base_dir / f"{channel}.roles.json"

    # --- chat ---

    def post_message(self, channel: str, agent_name: str, message: str) -> dict:
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "agent": agent_name,
            "message": message,
        }
        path = self._channel_path(channel)
        with open(path, "a") as f:
            f.write(json.dumps(entry) + "\n")
        return {"status": "success", "channel": channel}

    def read_messages(self, channel: str, limit: int = 20) -> dict:
        path = self._channel_path(channel)
        if not path.exists():
            return {"status": "error", "error": f"Channel not found: {channel}"}
        lines = path.read_text().strip().splitlines()
        messages = [json.loads(line) for line in lines[-limit:]]
        return {"status": "success", "channel": channel, "messages": messages}

    # --- roles ---

    def assign_role(self, channel: str, agent_name: str, role: str) -> dict:
        path = self._roles_path(channel)
        roles = json.loads(path.read_text()) if path.exists() else {}
        roles[agent_name] = role
        path.write_text(json.dumps(roles, indent=2))
        return {"status": "success", "channel": channel, "agent": agent_name, "role": role}

    def get_roles(self, channel: str) -> dict:
        path = self._roles_path(channel)
        if not path.exists():
            return {"status": "error", "error": f"No roles for channel: {channel}"}
        roles = json.loads(path.read_text())
        return {"status": "success", "channel": channel, "roles": roles}

    # --- permissions ---

    def check_permission(self, channel: str, agent_name: str, action: str) -> bool:
        return True

    # --- integrations ---

    def list_channels(self) -> dict:
        channels = [p.stem for p in self.base_dir.glob("*.jsonl")]
        return {"status": "success", "channels": channels}
