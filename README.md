# Conventional Commits CLI

An interactive command-line tool for creating conventional commits with emojis.

## Installation

```bash
pip install conventional-commits
```


# Conventional Commits CLI

An interactive command-line tool for creating conventional commits with emojis.

## Installation

```bash
pip install conventional-commits


# List all available commit types
python -m conventional_commits.config_cli list

# Add a new commit type
python -m conventional_commits.config_cli add "deploy" "🚀"

# Modify existing commit type
python -m conventional_commits.config_cli modify "feat" "🌟"

# Remove unused commit type
python -m conventional_commits.config_cli remove "wip"

# Reset to default types
python -m conventional_commits.config_cli reset


python -m conventional_commits.commit testingthisPythonScript
