import subprocess
from ..colors import Colors
from ..messages import Messages

def execute_git_push(force: bool = False, test_mode: bool = False) -> bool:
    if test_mode:
        print(Colors.SUCCESS + "TEST MODE: Would execute git push" + (" --force-with-lease" if force else ""))
        return True

    try:
        if force:
            result = subprocess.run(["git", "push", "--force-with-lease"], 
                                  capture_output=True, 
                                  text=True)
        else:
            result = subprocess.run(["git", "push"], 
                                  capture_output=True, 
                                  text=True)
        
        if result.returncode != 0:
            print(Colors.ERROR + Messages.PUSH_ERROR.format(result.stderr))
            return False
        return True
    except subprocess.SubprocessError as e:
        print(Colors.ERROR + Messages.PUSH_ERROR.format(str(e)))
        return False
