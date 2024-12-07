import json
from pathlib import Path

def load_commit_types(config_file: Path) -> dict:
    with open(config_file) as f:
        data = json.load(f)
        return {**data['defaultCommits'], **data['customCommits']}
