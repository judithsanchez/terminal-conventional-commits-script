from typing     import Dict, Any, Optional
import re
from .messages import Messages
from .colors import Colors
from .message_formatter import preview_commit_message
from .config.config_manager import ConfigManager

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

import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_commit_type(current_state: Dict[str, Any]) -> str:
    try:
        config = ConfigManager()
        all_types = config.load_commit_types()
        types_list = list(all_types.items())
        page_size = 10
        total_pages = (len(types_list) + page_size - 1) // page_size
        current_page = 0
        
        while True:
            clear_screen()  # Clear screen before showing new page
            print_divider()
            print(Colors.PROMPT + Messages.COMMIT_TYPE_PROMPT)
            print_divider()
            
            start_idx = current_page * page_size
            end_idx = min(start_idx + page_size, len(types_list))
            
            for i, (type_name, emoji) in enumerate(types_list[start_idx:end_idx], start=start_idx + 1):
                print(f"{i}. {type_name} {emoji}")
            
            print(f"\nPage {current_page + 1} of {total_pages}")
            print("Press 'm' for next page, 'b' for previous page\n")
            
            choice = input(Colors.INPUT + "Enter the number for the commit type: ").strip().lower()
            handle_quit(choice)
            
            if choice == 'm':
                current_page = (current_page + 1) % total_pages
                continue
            elif choice == 'b':
                current_page = (current_page - 1) % total_pages
                continue
                
            try:
                index = int(choice) - 1
                if 0 <= index < len(types_list):
                    commit_type = types_list[index][0]
                    current_state['commit_type'] = commit_type
                    current_state['emoji'] = all_types[commit_type]
                    show_current_preview(current_state)
                    return commit_type
                else:
                    raise CommitInputError(Messages.INVALID_CHOICE)
            except ValueError:
                raise CommitInputError(Messages.INVALID_CHOICE)
                
    except CommitInputError as e:
        print(Colors.ERROR + str(e))
        return get_commit_type(current_state)
    except Exception as e:
        print(Colors.ERROR + Messages.UNEXPECTED_ERROR.format(str(e)))
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
