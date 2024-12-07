from typing import Optional, Dict, Any

from conventional_commits.messages import Messages

def _validate_inputs(commit_type: str, message: str, emoji: str) -> None:
    """Validate required inputs for commit message formatting."""
    if not isinstance(commit_type, str) or not commit_type.strip():
        raise ValueError(Messages.COMMIT_TYPE_REQUIRED)
    if not isinstance(message, str) or not message.strip():
        raise ValueError(Messages.MESSAGE_REQUIRED) 
    if not isinstance(emoji, str) or not emoji.strip():
        raise ValueError(Messages.EMOJI_REQUIRED)
    if any(char in "!@#$%^&*()+=<>?/" for char in commit_type):
        raise ValueError(Messages.INVALID_COMMIT_TYPE)

def _clean_inputs(inputs: Dict[str, Any]) -> Dict[str, str]:
    """Clean and strip input strings."""
    return {key: str(value).strip() if value else "" for key, value in inputs.items()}

def format_commit_message(
    commit_type: str,
    message: str,
    emoji: str,
    scope: Optional[str] = None,
    breaking_change: Optional[str] = None,
    footer: Optional[str] = None
) -> str:
    """Format a conventional commit message with optional fields."""
    try:
        # Validate inputs
        _validate_inputs(commit_type, message, emoji)
        
        # Clean all inputs
        inputs = {
            'commit_type': commit_type,
            'message': message,
            'emoji': emoji,
            'scope': scope,
            'breaking_change': breaking_change,
            'footer': footer
        }
        cleaned = _clean_inputs(inputs)
        
        # Build commit message
        if cleaned['scope']:
            formatted_message = (
                f"{cleaned['emoji']}  {cleaned['commit_type']} "
                f"({cleaned['scope']})"
                f"{'!' if cleaned['breaking_change'] else ''}"
                f": {cleaned['message']}"
            )
        else:
            formatted_message = (
                f"{cleaned['emoji']}  {cleaned['commit_type']}"
                f"{'!' if cleaned['breaking_change'] else ''}"
                f": {cleaned['message']}"
            )

        # Add optional sections
        if cleaned['breaking_change']:
            formatted_message += f"\n\n{cleaned['breaking_change']}"

        if cleaned['footer']:
            formatted_message += f"\n\n{cleaned['footer']}"

        return formatted_message

    except Exception as e:
        raise ValueError(Messages.FORMAT_ERROR.format(str(e)))
