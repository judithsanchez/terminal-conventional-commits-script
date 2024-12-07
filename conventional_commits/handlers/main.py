from typing import Dict, Any
from ..handlers.type_handler import get_commit_type
from ..handlers.scope_handler import get_scope
from ..handlers.message_handler import get_message
from ..handlers.breaking_change_handler import get_breaking_change
from ..handlers.footer_handler import get_footer

def create_commit():
    current_state: Dict[str, Any] = {
        'commit_type': '',
        'emoji': '',
        'scope': None,
        'message': '',
        'breaking_change': '',
        'footer': None
    }
    
    get_commit_type(current_state)
    get_scope(current_state)
    get_message(current_state)
    get_breaking_change(current_state)
    get_footer(current_state)
    
    return current_state

if __name__ == "__main__":
    create_commit()
