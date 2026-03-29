import os
from .platform import CollaborationPlatform


class CollaborationPlatformFactory:

    @staticmethod
    def create() -> CollaborationPlatform:
        platform_type = os.environ.get("COLLABORATION_PLATFORM", "file")

        if platform_type == "discord":
            from .discord_platform import DiscordCollaborationPlatform
            return DiscordCollaborationPlatform()

        if platform_type == "irc":
            from .irc_platform import IRCCollaborationPlatform
            return IRCCollaborationPlatform()

        if platform_type == "file":
            base_dir = os.environ.get("COLLABORATION_FILE_DIR", ".collaboration")
            from .file_platform import FileCollaborationPlatform
            return FileCollaborationPlatform(base_dir)

        raise ValueError(f"Unknown collaboration platform: {platform_type}")
