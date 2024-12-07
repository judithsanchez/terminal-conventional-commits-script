import pytest
from unittest.mock import patch, Mock, call
from conventional_commits.git.status import get_git_status, show_final_status
from conventional_commits.git.push import execute_git_push
from conventional_commits.git.commit import execute_git_commit
from conventional_commits.git.add import handle_git_add, select_files

@pytest.fixture
def mock_subprocess():
    with patch('subprocess.run') as mock_run:
        mock_run.return_value = Mock(
            returncode=0,
            stdout="M  file1.py\nA  file2.py\n?? file3.py",
            stderr=""
        )
        yield mock_run

def test_get_git_status_with_mixed_changes(mock_subprocess):
    unstaged_files, staged_changes = get_git_status()
    assert len(unstaged_files) == 1
    assert "file3.py" in unstaged_files
    assert staged_changes is True

def test_get_git_status_no_changes(mock_subprocess):
    mock_subprocess.return_value.stdout = ""
    unstaged_files, staged_changes = get_git_status()
    assert len(unstaged_files) == 0
    assert staged_changes is False

def test_show_final_status(mock_subprocess):
    show_final_status()
    assert mock_subprocess.call_count == 1
    mock_subprocess.assert_called_with(["git", "status"], check=True)

def test_execute_git_push_success(mock_subprocess):
    assert execute_git_push() is True
    mock_subprocess.assert_called_with(
        ["git", "push"],
        capture_output=True,
        text=True
    )

def test_execute_git_push_force_success(mock_subprocess):
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
