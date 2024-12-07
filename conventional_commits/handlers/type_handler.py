from typing import Dict, Any
from ..colors import Colors
from ..messages import Messages
from ..config.config_manager import ConfigManager
from .common import CommitInputError, print_divider, show_current_preview, handle_quit, clear_screen

def get_commit_type(current_state: Dict[str, Any]) -> str:
    try:
        config = ConfigManager()
        all_types = config.load_commit_types()
        types_list = list(all_types.items())
        page_size = 10
        total_pages = (len(types_list) + page_size - 1) // page_size
        current_page = 0
        
        while True:
            clear_screen()
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
