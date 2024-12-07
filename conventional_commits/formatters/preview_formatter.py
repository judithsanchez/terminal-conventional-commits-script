from typing import Optional
import os

def preview_commit_message(
    commit_type: str = "",
    message: str = "",
    emoji: str = "",
    scope: Optional[str] = None,
    breaking_change: Optional[str] = None,
    footer: Optional[str] = None
) -> str:
    os.system('cls' if os.name == 'nt' else 'clear')
    
    try:
        if not all(isinstance(x, str) for x in [commit_type, message, emoji]):
            return ""
            
        commit_type = str(commit_type).strip()
        message = str(message).strip()
        emoji = str(emoji).strip()
        
        if not all([commit_type, message, emoji]):
            return ""
            
        if any(char in "!@#$%^&*()+=<>?/" for char in commit_type):
            return ""
            
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
        
    except Exception:
        return ""