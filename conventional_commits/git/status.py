import subprocess
from typing import Tuple, List

from conventional_commits.colors import Colors

def get_git_status() -> Tuple[List[str], bool]:
    result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
    unstaged_files = []
    for line in result.stdout.splitlines():
        if line.startswith(' M') or line.startswith('MM') or line.startswith('??'):
            unstaged_files.append(line[3:])
    
    staged_changes = any(
        line for line in result.stdout.splitlines()
        if line.startswith('M ') or line.startswith('A ')
    )
    
    return unstaged_files, staged_changes

def show_final_status() -> None:
    print("\n" + Colors.INFO + "Final status check... 🕵️")
    subprocess.run(["git", "status"], check=True)
    print("\n" + Colors.SUCCESS + "All done! Time to grab a ☕ and celebrate! 🎉")
