import os
import sys
from typing import Dict, Any

from conventional_commits.git.reset import unstage_all_files
from ..colors import Colors
from ..formatters.preview_formatter import preview_commit_message

class CommitInputError(Exception):
    pass

def print_divider():
    print("-" * 40)

def show_current_preview(current_state: Dict[str, Any]):
    print_divider()
    print(Colors.SUCCESS + "Current message preview:")
    preview = preview_commit_message(**current_state)
    print(Colors.OUTPUT + f"> {preview}")
    print_divider()

def handle_quit(value: str):
    if value.lower() == 'q':
        unstage_all_files()
        if 'pytest' in sys.modules:
            return
        print(Colors.SUCCESS + "Process exited.")
        exit(0)
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
