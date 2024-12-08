from typing import Optional, Dict, Any

from conventional_commits.messages import Messages

# this function doesn't return anything
def _validate_inputs(commit_type: str, message: str, emoji: str) -> None: 

    """Validate required inputs for commit message formatting.""" # docstring

    # if the commit type is not a string or is empty, raise a ValueError with the COMMIT_TYPE_REQUIRED message
    if not isinstance(commit_type, str) or not commit_type.strip(): 
        raise ValueError(Messages.COMMIT_TYPE_REQUIRED)

    if not isinstance(message, str) or not message.strip():
        # isinstance(), .strip() and ValueError() are built-in functions
        raise ValueError(Messages.MESSAGE_REQUIRED) 
    
    if not isinstance(emoji, str) or not emoji.strip():
        raise ValueError(Messages.EMOJI_REQUIRED)
    
    # if any special character is in the commit type, raise a ValueError 
    if any(char in "!@#$%^&*()+=<>?/" for char in commit_type):

    # any() is a built-in function    
        raise ValueError(Messages.INVALID_COMMIT_TYPE)

# Python's dictionaris are similar to JS objects
def _clean_inputs(inputs: Dict[str, Any]) -> Dict[str, str]:
    """Clean and strip input strings."""
    # iterate ver the array of inputs and create key-value pairs

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
        # check first if the inputs are valid by calling the first function
        _validate_inputs(commit_type, message, emoji)
        
        # if all the inputs are valid, create a dictionaty with them
        inputs = {
            'commit_type': commit_type,
            'message': message,
            'emoji': emoji,
            'scope': scope,
            'breaking_change': breaking_change,
            'footer': footer
        }

        # make sure the inputs are strings
        cleaned = _clean_inputs(inputs)
        
        # build commit message
        if cleaned['scope']:
            formatted_message = (
                # f"{xyz}{xyz}" is the Python way for string literals
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
            # \n is a new line
            formatted_message += f"\n\n{cleaned['breaking_change']}"

        if cleaned['footer']:
            formatted_message += f"\n\n{cleaned['footer']}"

        return formatted_message

    except Exception as e:
        raise ValueError(Messages.FORMAT_ERROR.format(str(e)))

# A leading underscore in a function or variable name is a convention used to indicate that the function or variable is intended for internal use within a module or class

# Tthey are helper functions that are not meant to be part of the module's public API. Python does not enforce access restrictions like some other languages (e.g., private or protected access modifiers in Java or C++)