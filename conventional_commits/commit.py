#!/usr/bin/env python3

import subprocess
import sys
from colorama import init
from typing import Optional, Dict, Any, Tuple, List

from .colors import Colors
from .config.config_manager import ConfigManager
from .messages import Messages
from .message_formatter import format_commit_message, MessageFormatError, preview_commit_message
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

def get_git_status() -> Tuple[List[str], bool]:
    result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
    # Get all unstaged files (including modified and untracked)
    unstaged_files = []
    for line in result.stdout.splitlines():
        if line.startswith(' M') or line.startswith('MM') or line.startswith('??'):
            unstaged_files.append(line[3:])
    
    has_changes = bool(unstaged_files)
    return unstaged_files, not has_changes

def select_files(files: List[str]) -> List[str]:
    print("\nAvailable files:")
    for i, file in enumerate(files, 1):
        print(f"{i}. {file}")
    
    selection = input(Messages.SELECT_FILES).strip()
    try:
        indices = [int(i.strip()) - 1 for i in selection.split(",")]
        return [files[i] for i in indices if 0 <= i < len(files)]
    except (ValueError, IndexError):
        return []

def handle_git_add(files: List[str]) -> bool:
    if TEST_MODE:
        print(Colors.SUCCESS + "TEST MODE: Would add files to git")
        return True

    choice = input(Messages.ADD_FILES_PROMPT).strip().lower()
    if choice == 'a':
        subprocess.run(["git", "add", "."], check=True)
        return True
    elif choice == 's':
        selected = select_files(files)
        if selected:
            subprocess.run(["git", "add"] + selected, check=True)
            return True
    return False

def execute_git_commit(commit_message: str) -> bool:
    if TEST_MODE:
        print(Colors.SUCCESS + Messages.TEST_MODE_MESSAGE.format(commit_message))
        return True

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

def execute_git_push(force: bool = False) -> bool:
    if TEST_MODE:
        print(Colors.SUCCESS + "TEST MODE: Would execute git push" + (" --force-with-lease" if force else ""))
        return True

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
        
        push_choice = input(Colors.INPUT + Messages.PUSH_PROMPT).strip().lower()
        if push_choice in ('y', 'f'):
            print(Colors.INFO + Messages.PUSHING_CHANGES)
            if execute_git_push(force=push_choice == 'f'):
                print(Colors.SUCCESS + Messages.PUSH_SUCCESS)

def main() -> None:
    try:
        if TEST_MODE:
            print(Colors.SUCCESS + Messages.TEST_MODE_ACTIVE)

        print(Colors.INFO + Messages.STATUS_CHECK)
        files, has_changes = get_git_status()
        
        if not has_changes and not files:
            print(Colors.WARNING + Messages.NO_CHANGES)
            return
            
        if not has_changes:
            if not handle_git_add(files):
                return

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
