#!/usr/bin/env python3

import sys
from colorama import init
from typing import Dict, Any

from .colors import Colors
from .config.config_manager import ConfigManager
from .messages import Messages
from .formatters.commit_formatter import format_commit_message
from .handlers.common import CommitInputError
from .handlers.main import create_commit
from .git.status import get_git_status, show_final_status
from .git.add import handle_git_add
from .git.commit import execute_git_commit
from .git.push import execute_git_push

init(autoreset=True)

TEST_MODE = len(sys.argv) > 1 and sys.argv[1] == "testingthisPythonScript"

def confirm_and_execute(formatted_message: str) -> None:
    confirm = input(Colors.INPUT + Messages.CONFIRM_COMMIT).strip().lower()
    if confirm != 'y':
        print(Colors.WARNING + Messages.PROCESS_INTERRUPTED)
        return

    if execute_git_commit(formatted_message, TEST_MODE):
        print(Colors.SUCCESS + Messages.COMMIT_SUCCESS)
        
        push_choice = input(Colors.INPUT + Messages.PUSH_PROMPT).strip().lower()
        if push_choice in ('y', 'f'):
            print(Colors.INFO + Messages.PUSHING_CHANGES)
            if execute_git_push(force=push_choice == 'f', test_mode=TEST_MODE):
                print(Colors.SUCCESS + Messages.PUSH_SUCCESS)
                show_final_status()

def main() -> None:
    try:
        if TEST_MODE:
            print(Colors.SUCCESS + Messages.TEST_MODE_ACTIVE)

        print(Colors.INFO + Messages.STATUS_CHECK)
        files, has_staged_changes = get_git_status()
        
        if not files and not has_staged_changes:
            print(Colors.WARNING + Messages.NO_CHANGES)
            return
            
        if not has_staged_changes:
            if not handle_git_add(files, TEST_MODE):
                return

        current_state = create_commit()
        formatted_message = format_commit_message(**current_state)
        confirm_and_execute(formatted_message)

    except CommitInputError as e:
        print(Colors.ERROR + str(e))
    except KeyboardInterrupt:
        print(Colors.WARNING + Messages.PROCESS_INTERRUPTED)
    except Exception as e:
        print(Colors.ERROR + Messages.UNEXPECTED_ERROR.format(str(e)))

if __name__ == '__main__':
    main()
