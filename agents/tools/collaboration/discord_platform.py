import os
import json
from urllib.request import Request, urlopen

from .platform import CollaborationPlatform

DISCORD_API = "https://discord.com/api/v10"


class DiscordCollaborationPlatform(CollaborationPlatform):

    def __init__(self):
        self.token = os.environ["DISCORD_BOT_TOKEN"]

    def _request(self, method: str, path: str, body: dict | None = None) -> dict:
        url = f"{DISCORD_API}{path}"
        data = json.dumps(body).encode() if body else None
        req = Request(
            url,
            data=data,
            headers={
                "Authorization": f"Bot {self.token}",
                "Content-Type": "application/json",
            },
            method=method,
        )
        with urlopen(req, timeout=10) as resp:
            return json.loads(resp.read())

    # --- chat ---

    def post_message(self, channel: str, agent_name: str, message: str) -> dict:
        formatted = f"**[{agent_name}]** {message}"
        data = self._request("POST", f"/channels/{channel}/messages", {"content": formatted})
        return {"status": "success", "channel": channel, "message_id": data["id"]}

    def read_messages(self, channel: str, limit: int = 20) -> dict:
        data = self._request("GET", f"/channels/{channel}/messages?limit={limit}")
        messages = [
            {
                "timestamp": msg["timestamp"],
                "agent": msg["author"]["username"],
                "message": msg["content"],
            }
            for msg in data
        ]
        return {"status": "success", "channel": channel, "messages": messages}

    # --- roles ---

    def assign_role(self, channel: str, agent_name: str, role: str) -> dict:
        raise NotImplementedError("Discord role assignment requires guild-level bot permissions")

    def get_roles(self, channel: str) -> dict:
        raise NotImplementedError("Discord role listing requires guild-level bot permissions")

    # --- permissions ---

    def check_permission(self, channel: str, agent_name: str, action: str) -> bool:
        return True

    # --- integrations ---

    def list_channels(self) -> dict:
        raise NotImplementedError("Discord channel listing requires guild ID configuration")
