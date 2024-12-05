import json
from pathlib import Path

class ConfigManager:
    def __init__(self):
        self.config_dir = Path(__file__).parent
        self.config_file = self.config_dir / 'commit_types.json'

    def load_commit_types(self) -> dict:
        with open(self.config_file) as f:
            data = json.load(f)
            return {**data['defaultCommits'], **data['customCommits']}

    def add_commit_type(self, type_name: str, emoji: str) -> None:
        with open(self.config_file, 'r+') as f:
            data = json.load(f)
            data['customCommits'][type_name] = emoji
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()

    def remove_commit_type(self, type_name: str) -> None:
        with open(self.config_file, 'r+') as f:
            data = json.load(f)
            if type_name in data['defaultCommits']:
                del data['defaultCommits'][type_name]
            if type_name in data['customCommits']:
                del data['customCommits'][type_name]
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()

    def modify_commit_type(self, type_name: str, new_emoji: str) -> None:
        with open(self.config_file, 'r+') as f:
            data = json.load(f)
            if type_name in data['defaultCommits']:
                data['defaultCommits'][type_name] = new_emoji
            elif type_name in data['customCommits']:
                data['customCommits'][type_name] = new_emoji
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()

    def reset_to_defaults(self) -> None:
        with open(self.config_file, 'r+') as f:
            data = json.load(f)
            data['customCommits'] = {}
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()