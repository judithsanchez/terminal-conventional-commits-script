import pytest
from conventional_commits.formatters.commit_formatter import format_commit_message
from conventional_commits.formatters.preview_formatter import preview_commit_message
from tests.test_fixtures import GARBAGE_VALUES
from conventional_commits.messages import Messages

def test_format_commit_message_basic():
    result = format_commit_message(
        commit_type="feat",
        message="add new feature",
        emoji="✨",
    )
    assert result == "✨  feat: add new feature"

def test_format_commit_message_different_types():
    test_cases = [
        {
            "type": "build",
            "message": "update dependencies",
            "emoji": "🔧",
            "expected": "🔧  build: update dependencies"
        },
        {
            "type": "ci",
            "message": "add GitHub actions",
            "emoji": "👷",
            "expected": "👷  ci: add GitHub actions"
        },
        {
            "type": "perf",
            "message": "optimize database queries",
            "emoji": "⚡️",
            "expected": "⚡️  perf: optimize database queries"
        }
    ]
    
    for case in test_cases:
        result = format_commit_message(
            commit_type=case["type"],
            message=case["message"],
            emoji=case["emoji"]
        )
        assert result == case["expected"]

def test_format_commit_message_with_scope():
    result = format_commit_message(
        commit_type="fix",
        message="fix bug in auth",
        emoji="🐛",
        scope="auth"
    )
    assert result == "🐛  fix (auth): fix bug in auth"

def test_format_commit_message_with_breaking_change():
    result = format_commit_message(
        commit_type="feat",
        message="completely new API",
        emoji="✨",
        breaking_change="BREAKING CHANGE: This changes the entire API"
    )
    assert result == "✨  feat!: completely new API\n\nBREAKING CHANGE: This changes the entire API"

def test_format_commit_message_with_footer():
    result = format_commit_message(
        commit_type="docs",
        message="update README",
        emoji="📝",
        footer="Closes #42"
    )
    assert result == "📝  docs: update README\n\nCloses #42"

def test_format_commit_message_with_all_fields():
    result = format_commit_message(
        commit_type="feat",
        message="new API implementation",
        emoji="✨",
        scope="api",
        breaking_change="BREAKING CHANGE: Complete API overhaul",
        footer="Refs: #123"
    )
    assert result == "✨  feat (api)!: new API implementation\n\nBREAKING CHANGE: Complete API overhaul\n\nRefs: #123"

# Error handling tests
@pytest.mark.parametrize("garbage", GARBAGE_VALUES)
def test_format_commit_message_with_garbage_values(garbage):
    with pytest.raises(ValueError, match=Messages.FORMAT_ERROR.format(".*")):
        format_commit_message(
            commit_type=garbage,
            message=garbage,
            emoji=garbage
        )

@pytest.mark.parametrize("garbage", GARBAGE_VALUES)
def test_preview_commit_message_with_garbage_values(garbage):
    result = preview_commit_message(
        commit_type=garbage,
        message=garbage,
        emoji=garbage
    )
    assert result == ""
