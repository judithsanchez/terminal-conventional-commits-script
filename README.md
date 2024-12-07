# Conventional Commits CLI

Interactive command-line tool for creating fun conventional commits.

## Installation

### Option 1: Using Virtual Environment (Recommended)

1. Create virtual environment

python3 -m venv venv

2. Activate virtual environment

# On Linux/macOS:

source venv/bin/activate

# On Windows:

.\venv\Scripts\activate

3. Install package

pip install -e .

### Option 2: Using pipx

1. Install pipx if not installed

# On Ubuntu/Debian:

sudo apt update && sudo apt install pipx

# On macOS:

brew install pipx

2. Install package

pipx install conventional-commits

## Usage

### Configuration Commands

#### List all available commit types

python3 -m conventional_commits.config_cli list

#### Add a new commit type

python3 -m conventional_commits.config_cli add "deploy" "🚀"

#### Modify existing commit type

python3 -m conventional_commits.config_cli modify "feat" "🌟"

#### Remove unused commit type

python3 -m conventional_commits.config_cli remove "wip"

#### Reset to default types

python3 -m conventional_commits.config_cli reset

### Creating Commits

#### Basic Usage

python3 -m conventional_commits.commit

#### Help Command

commit --help

#### Test Mode

gcommit testingthisPythonScript
