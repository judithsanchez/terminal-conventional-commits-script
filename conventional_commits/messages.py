class Messages:
    # Prompts
    COMMIT_TYPE_PROMPT = "Select a commit type (or type 'q' to quit):"
    SCOPE_PROMPT = "Enter the scope (optional, press Enter to skip or type 'q' to quit): "
    MESSAGE_PROMPT = "Enter the commit message (or type 'q' to quit): "
    BREAKING_CHANGE_PROMPT = "Is this a breaking change? (y/n): "
    BREAKING_CHANGE_DESC_PROMPT = "Describe the breaking change: "
    FOOTER_PROMPT = "Enter any additional footers (optional, press Enter to skip): "
    CONFIRM_PROMPT = "Do you want to proceed with this commit? (y/n, or 'q' to quit) [default: y]: "
    MORE_OPTIONS = "Press 'm' to see more options."

    # Success messages
    TEST_MODE_ACTIVE = "🧪 Running in test mode - no actual commits will be made"
    COMMIT_SUCCESSFUL = "Commit successful!"
    TEST_SUCCESSFUL = "✅ Test successful! This would have created a commit with message:"
    GENERATED_MESSAGE = "Generated commit message:"

    # Error messages
    PROCESS_EXIT = "Process exited."
    PROCESS_INTERRUPTED = "Process interrupted by user."
    COMMIT_ABORTED = "Commit aborted."
    INVALID_CHOICE = "Invalid choice. Please enter a number from the list."
    EMPTY_MESSAGE = "Commit message cannot be empty"
    INVALID_SCOPE = "Scope can only contain alphanumeric characters and hyphens"
    INVALID_BREAKING_CHANGE = "Invalid input. Please enter 'y' or 'n'"
    EMPTY_BREAKING_DESC = "Breaking change description cannot be empty"
    MISSING_REQUIRED = "Commit type, message, and emoji are required"

    # Git errors
    GIT_COMMIT_FAILED = "Git commit failed: {}"
    GIT_ERROR = "Error executing git commit: {}"
    
    # Generic errors
    UNEXPECTED_ERROR = "Unexpected error: {}"
    FORMAT_ERROR = "Error formatting message: {}"
    COMMIT_TYPE_ERROR = "Invalid commit type: {}"
