from abc import ABC, abstractmethod


class CollaborationPlatform(ABC):

    # --- chat ---

    @abstractmethod
    def post_message(self, channel: str, agent_name: str, message: str) -> dict:
        """Post a message to a channel."""

    @abstractmethod
    def read_messages(self, channel: str, limit: int = 20) -> dict:
        """Read recent messages from a channel."""

    # --- roles ---

    @abstractmethod
    def assign_role(self, channel: str, agent_name: str, role: str) -> dict:
        """Assign a role to an agent in a channel."""

    @abstractmethod
    def get_roles(self, channel: str) -> dict:
        """Get all role assignments for a channel."""

    # --- permissions ---

    @abstractmethod
    def check_permission(self, channel: str, agent_name: str, action: str) -> bool:
        """Check whether an agent can perform an action in a channel."""

    # --- integrations ---

    @abstractmethod
    def list_channels(self) -> dict:
        """List all available channels."""
