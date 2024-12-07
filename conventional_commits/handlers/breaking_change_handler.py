import sys
from typing import Dict, Any
from ..colors import Colors
from ..messages import Messages
from .common import CommitInputError, show_current_preview, handle_quit

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
