import subprocess
from typing import List
from ..colors import Colors
from ..messages import Messages

def select_files(files: List[str]) -> List[str]:
    print("\nAvailable files:")
    for i, file in enumerate(files, 1):
        print(f"{i}. {file}")
    
    selection = input(Messages.SELECT_FILES).strip()
    try:
        indices = [int(i.strip()) - 1 for i in selection.split(",")]
        return [files[i] for i in indices if 0 <= i < len(files)]
    except (ValueError, IndexError):
        return []

def handle_git_add(files: List[str], test_mode: bool = False) -> bool:
    if test_mode:
        print(Colors.SUCCESS + "TEST MODE: Would add files to git")
        return True

    choice = input(Messages.ADD_FILES_PROMPT).strip().lower()
    if choice == 'a':
        subprocess.run(["git", "add", "."], check=True)
        return True
    elif choice == 's':
        selected = select_files(files)
        if selected:
            subprocess.run(["git", "add"] + selected, check=True)
            return True
    return False
