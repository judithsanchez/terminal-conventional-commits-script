import subprocess
from typing import Tuple, List

from conventional_commits.colors import Colors
from conventional_commits.messages import Messages

def get_git_status() -> Tuple[List[str], bool]:
    result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
    unstaged_files = []
    for line in result.stdout.splitlines():
        if line.startswith(' M') or line.startswith('MM') or line.startswith('??') or line.startswith(' D'):
            unstaged_files.append(line[3:])
    
    staged_changes = any(
        line for line in result.stdout.splitlines()
        if line.startswith('M ') or line.startswith('A ') or line.startswith('D ')
    )
    
    return unstaged_files, staged_changes
def show_final_status() -> None:
    print("\n" + Colors.INFO + Messages.FINAL_STATUS_CHECK)
    subprocess.run(["git", "status"], check=True)
    print("\n" + Colors.SUCCESS + Messages.ALL_DONE)