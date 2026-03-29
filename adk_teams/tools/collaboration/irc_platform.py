from .platform import CollaborationPlatform


class IRCCollaborationPlatform(CollaborationPlatform):
    """Stub for future A2A agent-to-agent communication over IRC."""

    def post_message(self, channel: str, agent_name: str, message: str) -> dict:
        raise NotImplementedError("IRC platform planned for future A2A agent communication")

    def read_messages(self, channel: str, limit: int = 20) -> dict:
        raise NotImplementedError("IRC platform planned for future A2A agent communication")

    def assign_role(self, channel: str, agent_name: str, role: str) -> dict:
        raise NotImplementedError("IRC platform planned for future A2A agent communication")

    def get_roles(self, channel: str) -> dict:
        raise NotImplementedError("IRC platform planned for future A2A agent communication")

    def check_permission(self, channel: str, agent_name: str, action: str) -> bool:
        raise NotImplementedError("IRC platform planned for future A2A agent communication")

    def list_channels(self) -> dict:
        raise NotImplementedError("IRC platform planned for future A2A agent communication")
