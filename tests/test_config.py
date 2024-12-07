import pytest
import json
from conventional_commits.config.config_manager import ConfigManager
from conventional_commits.config.config_loader import load_commit_types

@pytest.fixture
def config_manager(tmp_path):
    config = {
        "defaultCommits": {
            "feat": "✨",
            "fix": "🐛"
        },
        "customCommits": {}
    }
    config_file = tmp_path / "commit_types.json"
    config_file.write_text(json.dumps(config))
    
    manager = ConfigManager()
    manager.config_file = config_file
    return manager

@pytest.fixture
def test_config_file(tmp_path):
    config = {
        "defaultCommits": {
            "feat": "✨",
            "fix": "🐛"
        },
        "customCommits": {}
    }
    config_file = tmp_path / "test_commit_types.json"
    config_file.write_text(json.dumps(config))
    return config_file

@pytest.fixture
def empty_config_file(tmp_path):
    config = {
        "defaultCommits": {},
        "customCommits": {}
    }
    config_file = tmp_path / "empty_commit_types.json"
    config_file.write_text(json.dumps(config))
    return config_file

@pytest.fixture
def full_config_file(tmp_path):
    config = {
        "defaultCommits": {
            "feat": "✨",
            "fix": "🐛",
            "docs": "📝"
        },
        "customCommits": {
            "custom1": "🎯",
            "custom2": "🎨"
        }
    }
    config_file = tmp_path / "full_commit_types.json"
    config_file.write_text(json.dumps(config))
    return config_file

def test_load_commit_types(test_config_file):
    commit_types = load_commit_types(test_config_file)
    assert "feat" in commit_types
    assert commit_types["feat"] == "✨"
    assert "fix" in commit_types
    assert commit_types["fix"] == "🐛"

def test_load_combined_commit_types(full_config_file):
    commit_types = load_commit_types(full_config_file)
    assert len(commit_types) == 5
    assert all(type in commit_types for type in ["feat", "fix", "docs", "custom1", "custom2"])

def test_add_commit_type(config_manager):
    config_manager.add_commit_type("custom", "🎯")
    commit_types = config_manager.load_commit_types()
    assert "custom" in commit_types
    assert commit_types["custom"] == "🎯"

def test_modify_commit_type(config_manager):
    config_manager.modify_commit_type("feat", "🌟")
    commit_types = config_manager.load_commit_types()
    assert commit_types["feat"] == "🌟"

def test_remove_commit_type(config_manager):
    config_manager.remove_commit_type("feat")
    commit_types = config_manager.load_commit_types()
    assert "feat" not in commit_types

def test_reset_to_defaults(config_manager):
    config_manager.add_commit_type("custom", "🎯")
    
    config_manager.reset_to_defaults()
    
    commit_types = config_manager.load_commit_types()
    assert "custom" not in commit_types

def test_multiple_commit_type_operations(config_manager):
    config_manager.add_commit_type("test1", "🎯")
    config_manager.add_commit_type("test2", "🎨")
    
    config_manager.modify_commit_type("test1", "🌟")
    
    commit_types = config_manager.load_commit_types()
    assert commit_types["test1"] == "🌟"
    assert commit_types["test2"] == "🎨"
    
    config_manager.remove_commit_type("test2")
    commit_types = config_manager.load_commit_types()
    assert "test2" not in commit_types
    assert "test1" in commit_types

def test_modify_commit_type(config_manager):
    initial_types = config_manager.load_commit_types()
    assert "feat" in initial_types
    
    config_manager.modify_commit_type("feat", "🌟")
    commit_types = config_manager.load_commit_types()
    assert commit_types["feat"] == "🌟"

def test_overwrite_existing_commit_type(config_manager):
    original_types = config_manager.load_commit_types()
    assert "feat" in original_types
    original_feat_emoji = original_types["feat"]
    
    config_manager.add_commit_type("feat", "🌟")
    updated_types = config_manager.load_commit_types()
    assert updated_types["feat"] == "🌟"
    assert updated_types["feat"] != original_feat_emoji

def test_config_persistence(config_manager):
    initial_types = config_manager.load_commit_types()
    assert "feat" in initial_types
    
    config_manager.add_commit_type("test", "🎯")
    config_manager.modify_commit_type("feat", "🌟")
    
    new_config_manager = ConfigManager()
    new_config_manager.config_file = config_manager.config_file
    commit_types = new_config_manager.load_commit_types()
    
    assert commit_types["test"] == "🎯"
    assert commit_types["feat"] == "🌟"