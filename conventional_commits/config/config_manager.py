from pathlib import Path
from .config_loader import load_commit_types
from .config_writer import (
    add_commit_type,
    remove_commit_type,
    modify_commit_type,
    reset_to_defaults
)

class ConfigManager:
    def __init__(self):
        self.config_dir = Path(__file__).parent
        self.config_file = self.config_dir / 'commit_types.json'

    def load_commit_types(self) -> dict:
        return load_commit_types(self.config_file)

    def add_commit_type(self, type_name: str, emoji: str) -> None:
        add_commit_type(self.config_file, type_name, emoji)

    def remove_commit_type(self, type_name: str) -> None:
        remove_commit_type(self.config_file, type_name)

    def modify_commit_type(self, type_name: str, new_emoji: str) -> None:
        modify_commit_type(self.config_file, type_name, new_emoji)

    def reset_to_defaults(self) -> None:
        reset_to_defaults(self.config_file)
