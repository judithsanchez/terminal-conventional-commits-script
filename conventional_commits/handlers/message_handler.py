import sys
from typing import Dict, Any
from ..colors import Colors
from ..messages import Messages
from .common import CommitInputError, show_current_preview, handle_quit

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
