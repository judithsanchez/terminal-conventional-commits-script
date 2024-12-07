import subprocess
from ..colors import Colors
from ..messages import Messages

def execute_git_commit(commit_message: str, test_mode: bool = False) -> bool:
    if test_mode:
        print(Colors.SUCCESS + Messages.TEST_MODE_MESSAGE.format(commit_message))
        return True

    try:
        result = subprocess.run(["git", "commit", "-m", commit_message], 
                              capture_output=True, 
                              text=True)
        if result.returncode != 0:
            print(Colors.ERROR + Messages.GIT_COMMIT_FAILED.format(result.stderr))
            return False
        return True
    except subprocess.SubprocessError as e:
        print(Colors.ERROR + Messages.GIT_ERROR.format(str(e)))
        return False
