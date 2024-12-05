import sys
import re
from typing import Optional, Dict, Any
from .colors import Colors
from .commit_types import COMMIT_TYPES
from .messages import Messages
from .message_formatter import preview_commit_message

class CommitInputError(Exception):
    """Custom exception for commit input errors"""
    pass

def print_divider():
    print(Colors.DIVIDER + "-" * 40)

def show_current_preview(current_state: Dict[str, Any]):
    print_divider()
    print(Colors.SUCCESS + "Current message preview:")
    preview = preview_commit_message(**current_state)
    print(Colors.OUTPUT + f"> {preview}")
    print_divider()

def handle_quit(input_value: str):
    if input_value.lower() in ["q", "quit"]:
        print(Colors.ERROR + Messages.PROCESS_EXIT)
        sys.exit(0)

def get_commit_type(current_state: Dict[str, Any]) -> str:
    try:
        commit_types_list = list(COMMIT_TYPES.keys())
        page_size = 10
        current_page = 0
        total_pages = (len(commit_types_list) + page_size - 1) // page_size

        while True:
            start_idx = current_page * page_size
            end_idx = min(start_idx + page_size, len(commit_types_list))

            print_divider()
            print(Colors.PROMPT + Messages.COMMIT_TYPE_PROMPT)
            print_divider()

            for i, t in enumerate(commit_types_list[start_idx:end_idx], start_idx + 1):
                print(Colors.INPUT + f"{i}. {t} {COMMIT_TYPES[t]}")

            if current_page + 1 < total_pages:
                print(Colors.INPUT + f"\n{Messages.MORE_OPTIONS}")

            choice = input(Colors.INPUT + "\nEnter the number for the commit type: ").strip().lower()
            handle_quit(choice)

            if choice == 'm' and current_page + 1 < total_pages:
                current_page += 1
                continue

            try:
                selected_type = commit_types_list[int(choice) - 1]
                if selected_type not in COMMIT_TYPES:
                    raise CommitInputError(Messages.COMMIT_TYPE_ERROR.format(selected_type))
                current_state['commit_type'] = selected_type
                current_state['emoji'] = COMMIT_TYPES[selected_type]
                show_current_preview(current_state)
                return selected_type
            except (IndexError, ValueError):
                print(Colors.ERROR + Messages.INVALID_CHOICE)

    except Exception as e:
        print(Colors.ERROR + Messages.UNEXPECTED_ERROR.format(str(e)))
        sys.exit(1)

def get_scope(current_state: Dict[str, Any]) -> Optional[str]:
    try:
        scope = input(Colors.INPUT + Messages.SCOPE_PROMPT).strip()
        handle_quit(scope)
        
        if not scope:
            current_state['scope'] = None
            show_current_preview(current_state)
            return None
            
        if not re.match(r'^[a-zA-Z0-9\-]+$', scope):
            raise CommitInputError(Messages.INVALID_SCOPE)
        current_state['scope'] = scope
        show_current_preview(current_state)
        return scope
    except CommitInputError as e:
        print(Colors.ERROR + str(e))
        return get_scope(current_state)
    except Exception as e:
        print(Colors.ERROR + Messages.UNEXPECTED_ERROR.format(str(e)))
        sys.exit(1)

def get_message(current_state: Dict[str, Any]) -> str:
    try:
        message = input(Colors.INPUT + Messages.MESSAGE_PROMPT).strip()
        handle_quit(message)
        
        if not message:
            raise CommitInputError(Messages.EMPTY_MESSAGE)
        current_state['message'] = message
        show_current_preview(current_state)
        return message
    except CommitInputError as e:
        print(Colors.ERROR + str(e))
        return get_message(current_state)
    except Exception as e:
        print(Colors.ERROR + Messages.UNEXPECTED_ERROR.format(str(e)))
        sys.exit(1)

def get_breaking_change(current_state: Dict[str, Any]) -> str:
    try:
        breaking = input(Colors.INPUT + Messages.BREAKING_CHANGE_PROMPT).strip().lower()
        if breaking == "y":
            description = input(Colors.INPUT + Messages.BREAKING_CHANGE_DESC_PROMPT).strip()
            if not description:
                raise CommitInputError(Messages.EMPTY_BREAKING_DESC)
            breaking_change = f"BREAKING CHANGE: {description}"
            current_state['breaking_change'] = breaking_change
            show_current_preview(current_state)
            return breaking_change
        elif breaking == "n":
            current_state['breaking_change'] = ""
            show_current_preview(current_state)
            return ""
        else:
            raise CommitInputError(Messages.INVALID_BREAKING_CHANGE)
    except CommitInputError as e:
        print(Colors.ERROR + str(e))
        return get_breaking_change(current_state)
    except Exception as e:
        print(Colors.ERROR + Messages.UNEXPECTED_ERROR.format(str(e)))
        sys.exit(1)

def get_footer(current_state: Dict[str, Any]) -> Optional[str]:
    try:
        footer = input(Colors.INPUT + Messages.FOOTER_PROMPT).strip()
        current_state['footer'] = footer if footer else None
        show_current_preview(current_state)
        return footer if footer else None
    except Exception as e:
        print(Colors.ERROR + Messages.UNEXPECTED_ERROR.format(str(e)))
        sys.exit(1)
