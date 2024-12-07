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
    CONFIRM_COMMIT = "Do you want to proceed with this commit? (y/n): "
    PUSH_PROMPT = "Would you like to push changes? (y/n/f for force-with-lease): "

    # Info
    PUSHING_CHANGES = "Pushing changes..."

    # Success messages
    TEST_MODE_ACTIVE = "🧪 Running in test mode - no actual commits will be made"
    TEST_MODE_MESSAGE = "TEST MODE: Commit message would have been:\n{}"    
    COMMIT_SUCCESS = "Commit successful! 🎉"
    TEST_SUCCESS = "✅ Test successful! This would have created a commit with message:"
    GENERATED_MESSAGE = "Generated commit message:"
    PUSH_SUCCESS = "Changes pushed successfully!"

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
    PUSH_ERROR = "Error pushing changes: {}"

    NO_CHANGES = "🧹 Everything is squeaky clean! Nothing to commit here. Maybe it's time to write some code? 😉"
    STATUS_CHECK = "Checking git status..."
    ADD_FILES_PROMPT = "Would you like to add files? (a for all, s for select, c to cancel): "
    SELECT_FILES = "Enter file numbers (comma-separated) to add: "

    COMMIT_TYPE_REQUIRED = "Commit type must be a non-empty string"
    MESSAGE_REQUIRED = "Message must be a non-empty string"
    EMOJI_REQUIRED = "Emoji must be a non-empty string"
    INVALID_COMMIT_TYPE = "Commit type contains invalid characters"
    FORMAT_ERROR = "Failed to format commit message: {}"