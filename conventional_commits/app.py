#!/usr/bin/env python3

import sys
from colorama import init
from typing import Dict, Any

from conventional_commits.config.settings import TEST_MODE
from conventional_commits.handlers.confirm_handler import confirm_and_execute

from .colors import Colors
from .config.config_manager import ConfigManager
from .messages import Messages
from .formatters.commit_formatter import format_commit_message
from .handlers.common import CommitInputError
from .handlers.main import create_commit
from .git.status import get_git_status
from .git.add import handle_git_add



init(autoreset=True)


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
