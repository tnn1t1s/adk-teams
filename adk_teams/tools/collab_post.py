from .collaboration import CollaborationPlatformFactory

_platform = None


def _get_platform():
    global _platform
    if _platform is None:
        _platform = CollaborationPlatformFactory.create()
    return _platform


def collab_post(channel: str, message: str, agent_name: str = "unknown") -> dict:
    """Posts a message to a collaboration channel.

    Args:
        channel: The channel name or ID to post to.
        message: The message content to post.
        agent_name: The name of the agent posting.

    Returns:
        dict: status and channel confirmation.
    """
    return _get_platform().post_message(channel, agent_name, message)
