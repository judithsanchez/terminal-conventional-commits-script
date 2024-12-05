import json
import os
from pathlib import Path
from typing import Dict
from .default_types import DEFAULT_COMMIT_TYPES
from ..colors import Colors

class ConfigManager:
    def __init__(self):
        self.config_dir = Path.home() / '.conventional_commits'
        self.config_file = self.config_dir / 'commit_types.json'
        self._ensure_config_exists()

    def _ensure_config_exists(self):
        """Create config directory and file if they don't exist"""
        self.config_dir.mkdir(exist_ok=True)
        if not self.config_file.exists():
            self.reset_to_defaults()

    def load_commit_types(self) -> Dict[str, str]:
        """Load commit types from config file"""
        with open(self.config_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_commit_types(self, commit_types: Dict[str, str]):
        """Save commit types to config file"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(commit_types, f, indent=2, ensure_ascii=False)

    def reset_to_defaults(self):
        """Reset config to default commit types"""
        self.save_commit_types(DEFAULT_COMMIT_TYPES)

    def add_commit_type(self, type_name: str, emoji: str):
        """Add new commit type"""
        types = self.load_commit_types()
        types[type_name] = emoji
        self.save_commit_types(types)

    def remove_commit_type(self, type_name: str):
        """Remove commit type"""
        types = self.load_commit_types()
        if type_name in types:
            del types[type_name]
            self.save_commit_types(types)

    def modify_commit_type(self, type_name: str, new_emoji: str):
        """Modify existing commit type emoji"""
        types = self.load_commit_types()
        if type_name in types:
            types[type_name] = new_emoji
            self.save_commit_types(types)
