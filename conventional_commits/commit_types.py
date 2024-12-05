from .config.config_manager import ConfigManager

config = ConfigManager()
COMMIT_TYPES = config.load_commit_types()
