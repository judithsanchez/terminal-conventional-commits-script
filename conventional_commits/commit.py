#!/usr/bin/env python3

import subprocess
import sys
from colorama import init
from typing import Optional, Dict, Any

from .colors import Colors
from .config.config_manager import ConfigManager
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
        # Add all changes first
        subprocess.run(["git", "add", "."], check=True)
        
        # Then commit
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

def execute_git_push(force: bool = False) -> bool:
    try:
        if force:
            result = subprocess.run(["git", "push", "--force-with-lease"], 
                                  capture_output=True, 
                                  text=True)
        else:
            result = subprocess.run(["git", "push"], 
                                  capture_output=True, 
                                  text=True)
        
        if result.returncode != 0:
            print(Colors.ERROR + Messages.PUSH_ERROR.format(result.stderr))
            return False
        return True
    except subprocess.SubprocessError as e:
        print(Colors.ERROR + Messages.PUSH_ERROR.format(str(e)))
        return False

def confirm_and_execute(formatted_message: str) -> None:
    confirm = input(Colors.INPUT + Messages.CONFIRM_COMMIT).strip().lower()
    if confirm != 'y':
        print(Colors.WARNING + Messages.PROCESS_INTERRUPTED)
        return

    if execute_git_commit(formatted_message):
        print(Colors.SUCCESS + Messages.COMMIT_SUCCESS)
        
        # Ask about pushing
        push_choice = input(Colors.INPUT + Messages.PUSH_PROMPT).strip().lower()
        if push_choice in ('y', 'f'):
            print(Colors.INFO + Messages.PUSHING_CHANGES)
            if execute_git_push(force=push_choice == 'f'):
                print(Colors.SUCCESS + Messages.PUSH_SUCCESS)

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

        config = ConfigManager()
        commit_type = get_commit_type(current_state)
        scope = get_scope(current_state)
        message = get_message(current_state)
        breaking_change = get_breaking_change(current_state)
        footer = get_footer(current_state)

        all_types = config.load_commit_types()
        emoji = all_types.get(commit_type)
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

            if TEST_MODE:
                print(Colors.SUCCESS + Messages.TEST_MODE_MESSAGE.format(formatted_message))
                return

            confirm_and_execute(formatted_message)

        except MessageFormatError as e:
            print(Colors.ERROR + str(e))

    except CommitInputError as e:
        print(Colors.ERROR + str(e))
    except KeyboardInterrupt:
        print(Colors.WARNING + Messages.PROCESS_INTERRUPTED)
    except Exception as e:
        print(Colors.ERROR + Messages.UNEXPECTED_ERROR.format(str(e)))
if __name__ == '__main__':
    main()
