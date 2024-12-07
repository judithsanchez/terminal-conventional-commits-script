import os
from typing import Dict, Any
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
        print(Colors.SUCCESS + "Process exited.")
        exit(0)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
