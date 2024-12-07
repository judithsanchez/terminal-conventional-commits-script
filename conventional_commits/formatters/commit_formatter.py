
from typing import Optional
from ..messages import Messages
from ..exceptions.format_errors import MessageFormatError

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
