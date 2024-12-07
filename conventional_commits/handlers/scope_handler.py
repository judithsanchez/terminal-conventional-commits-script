import re
import sys
from typing import Dict, Any, Optional
from ..colors import Colors
from ..messages import Messages
from .common import CommitInputError, show_current_preview, handle_quit

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
