from conventional_commits.colors import Colors
from conventional_commits.config.settings import TEST_MODE
from conventional_commits.git.commit import execute_git_commit
from conventional_commits.git.push import execute_git_push
from conventional_commits.git.status import show_final_status
from conventional_commits.messages import Messages


def confirm_and_execute(formatted_message: str) -> None:
    while True:
        print("\nCommit message:")
        print(Colors.OUTPUT + formatted_message)
        choice = input(Colors.INPUT + "Approve (y), Edit (e), or Cancel (n)? ").strip().lower()
        
        if choice == 'y':
            if execute_git_commit(formatted_message, TEST_MODE):
                print(Colors.SUCCESS + Messages.COMMIT_SUCCESS)
                
                push_choice = input(Colors.INPUT + Messages.PUSH_PROMPT).strip().lower()
                if push_choice in ('y', 'f'):
                    print(Colors.INFO + Messages.PUSHING_CHANGES)
                    if execute_git_push(force=push_choice == 'f', test_mode=TEST_MODE):
                        print(Colors.SUCCESS + Messages.PUSH_SUCCESS)
                        show_final_status()
            break
        elif choice == 'e':
            edited_message = input(Colors.INPUT + "Enter your edited commit message:\n").strip()
            if edited_message:
                formatted_message = edited_message
            continue
        else:
            print(Colors.WARNING + Messages.PROCESS_INTERRUPTED)
            break
