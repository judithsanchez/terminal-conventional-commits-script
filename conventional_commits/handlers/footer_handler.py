import sys
from typing import Dict, Any, Optional
from ..colors import Colors
from ..messages import Messages
from .common import show_current_preview

def get_footer(current_state: Dict[str, Any]) -> Optional[str]:
    try:
        footer = input(Colors.INPUT + Messages.FOOTER_PROMPT).strip()
        current_state['footer'] = footer if footer else None
        show_current_preview(current_state)
        return footer if footer else None
    except Exception as e:
        print(Colors.ERROR + Messages.UNEXPECTED_ERROR.format(str(e)))
        sys.exit(1)
