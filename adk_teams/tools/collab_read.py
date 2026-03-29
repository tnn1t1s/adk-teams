from .collaboration import CollaborationPlatformFactory

_platform = None


def _get_platform():
    global _platform
    if _platform is None:
        _platform = CollaborationPlatformFactory.create()
    return _platform


def collab_read(channel: str, limit: int = 20) -> dict:
    """Reads recent messages from a collaboration channel.

    Args:
        channel: The channel name or ID to read from.
        limit: Number of recent messages to retrieve (default 20, max 50).

    Returns:
        dict: status and list of messages with timestamp, agent, and message.
    """
    return _get_platform().read_messages(channel, limit=limit)
