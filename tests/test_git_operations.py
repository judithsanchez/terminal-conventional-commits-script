import pytest
from unittest.mock import patch, Mock, call
from conventional_commits.git.reset import unstage_all_files
from conventional_commits.git.status import get_git_status, show_final_status
from conventional_commits.git.push import execute_git_push
from conventional_commits.git.commit import execute_git_commit
from conventional_commits.git.add import handle_git_add, select_files
@pytest.fixture
def mock_subprocess():
    with patch('subprocess.run') as mock_run:
        yield mock_run

def test_execute_git_push_no_upstream_branch(mock_subprocess):
    # Simulate the error message for no upstream branch
    mock_subprocess.side_effect = [
        Mock(
            returncode=1,
            stderr="fatal: The current branch js/learning/beginners has no upstream branch.\n"
                   "To push the current branch and set the remote as upstream, use\n\n"
                   "    git push --set-upstream origin js/learning/beginners\n"
        ),
        Mock(returncode=0)  # Simulate successful upstream branch set
    ]
    
    with patch('builtins.input', return_value='y'):
        assert execute_git_push() is True
        mock_subprocess.assert_any_call(
            ["git", "push", "--set-upstream", "origin", "js/learning/beginners"],
            capture_output=True,
            text=True
        )
def test_execute_git_push_no_upstream_branch_user_aborts(mock_subprocess):
    # Simulate the error message for no upstream branch
    mock_subprocess.return_value = Mock(
        returncode=1,
        stderr="fatal: The current branch js/learning/beginners has no upstream branch.\n"
                "To push the current branch and set the remote as upstream, use\n\n"
                "    git push --set-upstream origin js/learning/beginners\n"
    )
    
    with patch('builtins.input', return_value='n'):
        assert execute_git_push() is False
        mock_subprocess.assert_called_once_with(
            ["git", "push"],
            capture_output=True,
            text=True
        )

def test_execute_git_push_success(mock_subprocess):
    mock_subprocess.return_value = Mock(returncode=0)
    assert execute_git_push() is True
    mock_subprocess.assert_called_with(
        ["git", "push"],
        capture_output=True,
        text=True
    )

def test_execute_git_push_force_success(mock_subprocess):
    mock_subprocess.return_value = Mock(returncode=0)
    assert execute_git_push(force=True) is True
    mock_subprocess.assert_called_with(
        ["git", "push", "--force-with-lease"],
        capture_output=True,
        text=True
    )

def test_execute_git_push_test_mode(mock_subprocess):
    assert execute_git_push(test_mode=True) is True
    mock_subprocess.assert_not_called()
def test_execute_git_commit_success(mock_subprocess):
    commit_message = "test: add unit tests"
    mock_subprocess.return_value = Mock(returncode=0)
    assert execute_git_commit(commit_message) is True
    mock_subprocess.assert_called_with(
        ["git", "commit", "-m", commit_message],
        capture_output=True,
        text=True
    )

def test_execute_git_commit_test_mode(mock_subprocess):
    commit_message = "test: add unit tests"
    assert execute_git_commit(commit_message, test_mode=True) is True
    mock_subprocess.assert_not_called()

@patch('builtins.input')
def test_handle_git_add_all(mock_input, mock_subprocess):
    mock_input.return_value = 'a'
    files = ["file1.py", "file2.py"]
    assert handle_git_add(files) is True
    mock_subprocess.assert_called_with(
        ["git", "add", "."],
        check=True
    )

@patch('builtins.input')
def test_handle_git_add_select(mock_input, mock_subprocess):
    mock_input.side_effect = ['s', '1,2']
    files = ["file1.py", "file2.py"]
    assert handle_git_add(files) is True
    mock_subprocess.assert_called_with(
        ["git", "add"] + files,
        check=True
    )

@patch('builtins.input')
def test_handle_git_add_cancel(mock_input, mock_subprocess):
    mock_input.return_value = 'c'
    files = ["file1.py", "file2.py"]
    assert handle_git_add(files) is False
    mock_subprocess.assert_not_called()

@patch('builtins.input')
def test_handle_git_add_test_mode(mock_input, mock_subprocess):
    mock_input.return_value = 'a'
    files = ["file1.py", "file2.py"]
    assert handle_git_add(files, test_mode=True) is True
    mock_subprocess.assert_not_called()

def test_select_files_single():
    files = ["file1.py", "file2.py", "file3.py"]
    with patch('builtins.input', return_value="2"):
        selected = select_files(files)
        assert selected == ["file2.py"]

def test_select_files_multiple():
    files = ["file1.py", "file2.py", "file3.py"]
    with patch('builtins.input', return_value="1,3"):
        selected = select_files(files)
        assert selected == ["file1.py", "file3.py"]

def test_select_files_invalid_input():
    files = ["file1.py", "file2.py", "file3.py"]
    with patch('builtins.input', return_value="invalid"):
        selected = select_files(files)
        assert selected == []

def test_select_files_out_of_range():
    files = ["file1.py", "file2.py", "file3.py"]
    with patch('builtins.input', return_value="1,4"):
        selected = select_files(files)
        assert selected == ["file1.py"]

def test_unstage_all_files(mock_subprocess):
    unstage_all_files()
    mock_subprocess.assert_called_with(
        ["git", "reset", "HEAD"],
        capture_output=True,
        text=True
    )

def test_unstage_all_files_success(mock_subprocess):
    mock_subprocess.return_value = Mock(returncode=0)
    unstage_all_files()
    mock_subprocess.assert_called_once()

def test_get_git_status_unstaged_files(mock_subprocess):
    mock_subprocess.return_value = Mock(
        stdout=" M file1.py\n?? file2.py\n D file3.py\nMM file4.py",
        returncode=0
    )
    unstaged, staged = get_git_status()
    assert unstaged == ["file1.py", "file2.py", "file3.py", "file4.py"]
    assert staged is False

def test_get_git_status_staged_files(mock_subprocess):
    mock_subprocess.return_value = Mock(
        stdout="M  file1.py\nA  file2.py\nD  file3.py",
        returncode=0
    )
    unstaged, staged = get_git_status()
    assert unstaged == []
    assert staged is True

def test_show_final_status(mock_subprocess):
    show_final_status()
    mock_subprocess.assert_called_with(
        ["git", "status"],
        check=True
    )
