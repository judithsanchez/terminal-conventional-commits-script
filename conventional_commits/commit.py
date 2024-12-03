#!/usr/bin/env python3

import subprocess
import sys
import re
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Define custom colors based on your terminal palette
class Colors:
    PROMPT = Fore.LIGHTMAGENTA_EX  # Light purple for general prompts
    INPUT = Fore.LIGHTCYAN_EX      # Soft cyan for user inputs
    SUCCESS = Fore.LIGHTGREEN_EX   # Light green for success messages
    ERROR = Fore.LIGHTRED_EX       # Pastel red for errors
    DIVIDER = Fore.LIGHTBLACK_EX   # Neutral gray for dividers
    OUTPUT = Fore.LIGHTWHITE_EX    # Light pinkish white for displayed results

# Test mode flag
TEST_MODE = len(sys.argv) > 1 and sys.argv[1] == "testingthisPythonScript"

# Comprehensive list of commit types
COMMIT_TYPES = {
    "feat": "✨",        # A new feature
    "wip": "🚧",         # Work in progress
    "fix": "🐛",         # A bug fix
    "docs": "📝",        # Documentation only changes
    "style": "💄",       # Code style changes
    "refactor": "♻️",    # Code refactoring
    "test": "✅",        # Adding tests
    "typo": "✏️",        # Fixed a typo
    "finally": "🎯",     # Finally got something to work
    "ui": "💅🏻",         # User interface changes
    "oops": "🤦🏻‍♀️",     # Fixing my own mistake
    "revert": "⏪️",      # Reverting a commit
    "init": "🎉",        # Initial commit
    "debug": "🐞",       # Debugging changes
    "hotfix": "🔥",      # Critical hotfix
    "lazy": "💤",        # Shortcut added for convenience
    "yolo": "🚀",        # Experimental change
    "ux": "🛋️",          # Improved user experience
    # "perf": "⚡️",       # Code changes that improve performance
    # "style": "💄",       # Changes that do not affect the meaning of the code
    # "merge": "🔀",       # Merge branches
    # "deps": "📦",        # Dependency updates
    # "security": "🔒",    # Security patches or updates
    # "config": "⚙️",      # Configuration file changes
    # "localization": "🌐",# Language localization changes
    # "analytics": "📊",   # Changes related to analytics or tracking
    # "petproject": "🐾",  # A fun personal project
    # "build": "🔧",       # Changes that affect the build system or dependencies
    # "ci": "👷",          # Changes to CI configuration files and scripts
    # "chore": "🗃️",      # Other changes that don't modify src or test files
    # "placeholder": "🚧"  # Added placeholder code or content
}

def print_divider():
    print(Colors.DIVIDER + "-" * 40)

def get_commit_type():
    commit_types_list = list(COMMIT_TYPES.keys())
    page_size = 10
    current_page = 0
    total_pages = (len(commit_types_list) + page_size - 1) // page_size

    while True:
        start_idx = current_page * page_size
        end_idx = min(start_idx + page_size, len(commit_types_list))

        print_divider()
        print(Colors.PROMPT + "Select a commit type (or type 'q' to quit):")
        print_divider()

        for i, t in enumerate(commit_types_list[start_idx:end_idx], start_idx + 1):
            print(Colors.INPUT + f"{i}. {t} {COMMIT_TYPES[t]}")

        if current_page + 1 < total_pages:
            print(Colors.INPUT + "\nPress 'm' to see more options.")

        choice = input(Colors.INPUT + "\nEnter the number for the commit type: ").strip().lower()

        if choice in ["q", "quit"]:
            print(Colors.ERROR + "Process exited.")
            sys.exit(0)
        elif choice == 'm' and current_page + 1 < total_pages:
            current_page += 1
            continue

        try:
            return commit_types_list[int(choice) - 1]
        except (IndexError, ValueError):
            print(Colors.ERROR + "Invalid choice. Try again.")

def get_scope():
    scope = input(Colors.INPUT + "Enter the scope (optional, press Enter to skip or type 'q' to quit): ").strip()
    if scope.lower() in ["q", "quit"]:
        print(Colors.ERROR + "Process exited.")
        sys.exit(0)
    if scope and not re.match(r'^[a-zA-Z0-9\-]+$', scope):
        print(Colors.ERROR + "Scope can only contain alphanumeric characters and hyphens. Try again.")
        return get_scope()
    return scope

def get_message():
    message = input(Colors.INPUT + "Enter the commit message (or type 'q' to quit): ").strip()
    if message.lower() in ["q", "quit"]:
        print(Colors.ERROR + "Process exited.")
        sys.exit(0)
    if not message:
        print(Colors.ERROR + "Commit message cannot be empty.")
        return get_message()
    return message

def get_breaking_change():
    breaking = input(Colors.INPUT + "Is this a breaking change? (y/n): ").strip().lower()
    if breaking == "y":
        description = input(Colors.INPUT + "Describe the breaking change: ").strip()
        return f"BREAKING CHANGE: {description}"
    elif breaking == "n":
        return ""
    else:
        print(Colors.ERROR + "Invalid input. Please enter 'y' or 'n'.")
        return get_breaking_change()

def get_footer():
    footer = input(Colors.INPUT + "Enter any additional footers (optional, press Enter to skip): ").strip()
    return footer

def main():
    if TEST_MODE:
        print(Colors.SUCCESS + "🧪 Running in test mode - no actual commits will be made")

    commit_type = get_commit_type()
    scope = get_scope()
    message = get_message()
    breaking_change = get_breaking_change()
    footer = get_footer()

    # Get the emoji for the selected commit type
    emoji = COMMIT_TYPES[commit_type]

    # Construct the commit message
    if scope:
        formatted_message = f"{emoji}  {commit_type} ({scope}): {message}"
    else:
        formatted_message = f"{emoji}  {commit_type}: {message}"
    if breaking_change:
        formatted_message += f"\n\n{breaking_change}"
    if footer:
        formatted_message += f"\n\n{footer}"

    print_divider()
    print(Colors.SUCCESS + "Generated commit message:")
    print(Colors.OUTPUT + f"> {formatted_message}")
    print_divider()

    confirm = input(Colors.INPUT + "Do you want to proceed with this commit? (y/n, or 'q' to quit) [default: y]: ").strip().lower()

    if confirm in ["q", "quit"]:
        print(Colors.ERROR + "Process exited.")
        sys.exit(0)
    elif confirm in ["", "y", "yes"]:
        if TEST_MODE:
            print(Colors.SUCCESS + "✅ Test successful! This would have created a commit with message:")
            print(Colors.OUTPUT + f"'{formatted_message}'")
        else:
            result = subprocess.run(["git", "commit", "-m", formatted_message])
            if result.returncode == 0:
                print(Colors.SUCCESS + "Commit successful!")
            else:
                print(Colors.ERROR + "Commit failed. Check the error above.")
    else:
        print(Colors.ERROR + "Commit aborted.")

if __name__ == "__main__":
    main()