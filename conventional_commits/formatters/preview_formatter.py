
from typing import Optional

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
