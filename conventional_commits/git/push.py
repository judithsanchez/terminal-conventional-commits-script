import subprocess
from ..colors import Colors
from ..messages import Messages

def execute_git_push(force: bool = False, test_mode: bool = False) -> bool:
    if test_mode:
        print(Colors.SUCCESS + Messages.TEST_MODE_PUSH + (" --force-with-lease" if force else ""))
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
            if "no upstream branch" in result.stderr:
                print(Colors.ERROR + Messages.ERROR_PUSHING_CHANGES.format(result.stderr))
                user_input = input(Messages.SET_UPSTREAM_PROMPT).strip().lower()
                if user_input == 'y':
                    branch_name = result.stderr.split()[-1]  
                    set_upstream_result = subprocess.run(
                        ["git", "push", "--set-upstream", "origin", branch_name],
                        capture_output=True,
                        text=True
                    )
                    if set_upstream_result.returncode == 0:
                        print(Colors.SUCCESS + Messages.BRANCH_SET_SUCCESS)
                        return True
                    else:
                        print(Colors.ERROR + Messages.PUSH_ERROR.format(set_upstream_result.stderr))
                        return False
                else:
                    print(Colors.WARNING + Messages.PUSH_ABORTED)
                    return False
            else:
                print(Colors.ERROR + Messages.PUSH_ERROR.format(result.stderr))
                return False
        return True
    except subprocess.SubprocessError as e:
        print(Colors.ERROR + Messages.PUSH_ERROR.format(str(e)))
        return False
