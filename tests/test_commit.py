
import unittest
from unittest.mock import patch
from conventional_commits.commit import get_commit_type, get_scope, get_message, GitOperations

class TestCommitScript(unittest.TestCase):
    def setUp(self):
        self.git_ops = GitOperations()

    @patch('builtins.input', return_value='1')
    def test_get_commit_type(self, mock_input):
        commit_type = get_commit_type()
        self.assertIn(commit_type, COMMIT_TYPES.keys())

    @patch('builtins.input', return_value='auth')
    def test_get_scope(self, mock_input):
        scope = get_scope()
        self.assertEqual(scope, 'auth')

    @patch('builtins.input', return_value='Add new feature')
    def test_get_message(self, mock_input):
        message = get_message()
        self.assertEqual(message, 'Add new feature')

    def test_git_operations_test_mode(self):
        self.assertTrue(self.git_ops.is_git_repository())
        self.assertTrue(self.git_ops.create_commit("test commit"))
