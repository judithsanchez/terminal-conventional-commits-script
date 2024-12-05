#!/usr/bin/env python3

import subprocess
import sys
from colorama import init
from typing import Optional, Dict, Any

from .colors import Colors
from .commit_types import COMMIT_TYPES
from .messages import Messages
from .message_formatter import format_commit_message, MessageFormatError
from .input_handlers import (
    print_divider,
    get_commit_type,
    get_scope,
    get_message,
    get_breaking_change,
    get_footer,
    CommitInputError
)

init(autoreset=True)

TEST_MODE = len(sys.argv) > 1 and sys.argv[1] == "testingthisPythonScript"

def execute_git_commit(commit_message: str) -> bool:
    try:
        result = subprocess.run(["git", "commit", "-m", commit_message], 
                              capture_output=True, 
                              text=True)
        if result.returncode != 0:
            print(Colors.ERROR + Messages.GIT_COMMIT_FAILED.format(result.stderr))
            return False
        return True
    except subprocess.SubprocessError as e:
        print(Colors.ERROR + Messages.GIT_ERROR.format(str(e)))
        return False

def main() -> None:
    try:
        if TEST_MODE:
            print(Colors.SUCCESS + Messages.TEST_MODE_ACTIVE)

        current_state: Dict[str, Any] = {
            'commit_type': '',
            'scope': None,
            'message': '',
            'breaking_change': '',
            'footer': None,
            'emoji': ''
        }

        commit_type = get_commit_type(current_state)
        scope = get_scope(current_state)
        message = get_message(current_state)
        breaking_change = get_breaking_change(current_state)
        footer = get_footer(current_state)

        emoji = COMMIT_TYPES.get(commit_type)
        if not emoji:
            raise CommitInputError(Messages.COMMIT_TYPE_ERROR.format(commit_type))

        try:
            formatted_message = format_commit_message(
                commit_type=commit_type,
                scope=scope,
                message=message,
                breaking_change=breaking_change,
                footer=footer,
                emoji=emoji
            )
        except MessageFormatError as e:
            print(Colors.ERROR + Messages.FORMAT_ERROR.format(str(e)))
            sys.exit(1)

        print_divider()
        print(Colors.SUCCESS + Messages.GENERATED_MESSAGE)
        print(Colors.OUTPUT + f"> {formatted_message}")
        print_divider()

        confirm = input(Colors.INPUT + Messages.CONFIRM_PROMPT).strip().lower()

        if confirm in ["q", "quit"]:
            print(Colors.ERROR + Messages.PROCESS_EXIT)
            sys.exit(0)
        elif confirm in ["", "y", "yes"]:
            if TEST_MODE:
                print(Colors.SUCCESS + Messages.TEST_SUCCESSFUL)
                print(Colors.OUTPUT + f"'{formatted_message}'")
            else:
                if execute_git_commit(formatted_message):
                    print(Colors.SUCCESS + Messages.COMMIT_SUCCESSFUL)
                else:
                    sys.exit(1)
        else:
            print(Colors.ERROR + Messages.COMMIT_ABORTED)

    except KeyboardInterrupt:
        print(Colors.ERROR + f"\n{Messages.PROCESS_INTERRUPTED}")
        sys.exit(1)
    except Exception as e:
        print(Colors.ERROR + Messages.UNEXPECTED_ERROR.format(str(e)))
        sys.exit(1)

if __name__ == "__main__":
    main()
