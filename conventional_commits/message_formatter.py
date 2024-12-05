from typing import Optional
from .messages import Messages

class MessageFormatError(Exception):
    """Custom exception for message formatting errors"""
    pass

def preview_commit_message(
    commit_type: str = "",
    message: str = "",
    emoji: str = "",
    scope: Optional[str] = None,
    breaking_change: Optional[str] = None,
    footer: Optional[str] = None
) -> str:
    preview = ""
    
    if commit_type and emoji:
        if scope:
            preview = f"{emoji}  {commit_type} ({scope})" + ("!" if breaking_change else "")
        else:
            preview = f"{emoji}  {commit_type}" + ("!" if breaking_change else "")
            
    if message:
        preview += f": {message}" if preview else message
        
    if breaking_change:
        preview += f"\n\n{breaking_change}"
        
    if footer:
        preview += f"\n\n{footer}"
        
    return preview

def format_commit_message(
    commit_type: str,
    message: str,
    emoji: str,
    scope: Optional[str] = None,
    breaking_change: Optional[str] = None,
    footer: Optional[str] = None
) -> str:
    try:
        if not commit_type or not message or not emoji:
            raise MessageFormatError(Messages.MISSING_REQUIRED)

        if scope:
            formatted_message = f"{emoji}  {commit_type} ({scope})" + ("!" if breaking_change else "") + f": {message}"
        else:
            formatted_message = f"{emoji}  {commit_type}" + ("!" if breaking_change else "") + f": {message}"

        if breaking_change:
            formatted_message += f"\n\n{breaking_change}"

        if footer:
            formatted_message += f"\n\n{footer}"

        return formatted_message

    except Exception as e:
        raise MessageFormatError(Messages.FORMAT_ERROR.format(str(e)))
