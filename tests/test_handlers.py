import pytest
from unittest.mock import patch, Mock, MagicMock
from conventional_commits.handlers.main import create_commit
from conventional_commits.handlers.type_handler import get_commit_type
from conventional_commits.handlers.scope_handler import get_scope
from conventional_commits.handlers.message_handler import get_message
from conventional_commits.handlers.breaking_change_handler import get_breaking_change
from conventional_commits.handlers.footer_handler import get_footer
from conventional_commits.handlers.confirm_handler import confirm_and_execute

@pytest.fixture
def mock_inputs():
    with patch('builtins.input') as mock_input:
        yield mock_input

@pytest.fixture
def current_state():
    return {
        'commit_type': '',
        'emoji': '',
        'scope': None,
        'message': '',
        'breaking_change': '',
        'footer': None
    }

@pytest.fixture
def mock_config():
    with patch('conventional_commits.config.config_manager.ConfigManager') as mock:
        instance = mock.return_value
        instance.load_commit_types.return_value = {
            "feat": "✨",
            "fix": "🐛"
        }
        yield mock

@patch('conventional_commits.handlers.common.clear_screen')
def test_get_commit_type(mock_clear, mock_inputs, current_state, mock_config):
    mock_inputs.side_effect = ["1"]
    result = get_commit_type(current_state)
    assert result == current_state['commit_type']
    assert current_state['emoji'] != ''
def test_get_scope(mock_inputs, current_state):
    mock_inputs.return_value = "auth"
    result = get_scope(current_state)
    assert result == "auth"
    assert current_state['scope'] == "auth"

def test_get_message(mock_inputs, current_state):
    mock_inputs.return_value = "test commit message"
    result = get_message(current_state)
    assert result == "test commit message"
    assert current_state['message'] == "test commit message"

def test_get_breaking_change(mock_inputs, current_state):
    mock_inputs.side_effect = ["y", "Breaking API change"]
    result = get_breaking_change(current_state)
    assert "BREAKING CHANGE: Breaking API change" in result
    assert current_state['breaking_change'] == "BREAKING CHANGE: Breaking API change"

def test_get_footer(mock_inputs, current_state):
    mock_inputs.return_value = "Closes #123"
    result = get_footer(current_state)
    assert result == "Closes #123"
    assert current_state['footer'] == "Closes #123"

# @patch('builtins.input')
# @patch('conventional_commits.git.commit.execute_git_commit')
# @patch('conventional_commits.git.push.execute_git_push')
# @patch('conventional_commits.git.status.show_final_status')
# def test_confirm_and_execute(mock_status, mock_push, mock_commit, mock_input):
#     mock_input.side_effect = ["y", "y"]  # First y for commit, second for push
#     mock_commit.return_value = True
#     mock_push.return_value = True
    
#     formatted_message = "feat: test commit"
#     confirm_and_execute(formatted_message)
    
#     mock_commit.assert_called_once_with(formatted_message, False)
#     mock_push.assert_called_once_with(force=False, test_mode=False)
#     mock_status.assert_called_once()

# @patch('conventional_commits.config.config_manager.ConfigManager')
# @patch('conventional_commits.handlers.type_handler.get_commit_type')
# @patch('conventional_commits.handlers.scope_handler.get_scope')
# @patch('conventional_commits.handlers.message_handler.get_message')
# @patch('conventional_commits.handlers.breaking_change_handler.get_breaking_change')
# @patch('conventional_commits.handlers.footer_handler.get_footer')
# def test_create_commit(mock_footer, mock_breaking, mock_message, mock_scope, mock_type, mock_config):
#     # Setup mock config
#     instance = mock_config.return_value
#     instance.load_commit_types.return_value = {
#         "feat": "✨",
#         "fix": "🐛"
#     }
    
#     # Setup return values
#     mock_type.return_value = "feat"
#     mock_scope.return_value = "auth"
#     mock_message.return_value = "add login"
#     mock_breaking.return_value = ""
#     mock_footer.return_value = "Closes #123"
    
#     result = create_commit()
    
#     assert result['commit_type'] == "feat"
#     assert result['scope'] == "auth"
#     assert result['message'] == "add login"
#     assert result['footer'] == "Closes #123"    
#     assert result['footer'] == "Closes #123"