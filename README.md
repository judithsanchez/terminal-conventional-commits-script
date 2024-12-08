# 🚀 Conventional Commits CLI

Welcome to the **Conventional Commits CLI**, an interactive and fun tool for creating conventional commits with ease! 🎉 Say goodbye to boring commit messages and hello to emojis and structured messages! 😎

## 🌟 Features
- Fully customizable commit types with emoji support 🎨
- Interactive prompts for commit creation 🤖
- Easy configuration management 🛠️
- Supports virtual environments and pipx for installation ✅


## 📦 Installation

### Global Installation with pipx (Recommended)
1. **Install pipx** (if not installed):
    - On Ubuntu/Debian:
      ```bash
      sudo apt update && sudo apt install pipx
      ```
    - On macOS:
      ```bash
      brew install pipx
      ```
    - On Windows:
      ```bash
      python -m pip install --user pipx
      ```

2. **Clone and Install**:
    ```bash
    # Clone repository
    git clone https://github.com/yourusername/terminal-conventional-commits-script.git
    
    # Navigate to project directory
    cd terminal-conventional-commits-script
    
    # Install globally with pipx
    pipx install -e .
    ```

3. **Verify Installation**:
    ```bash
    gcommit --help
    ```

After installation, you can use `gcommit` in any git repository on your system.s


### Local Installation with Virtual Environment
1. **Create and activate virtual environment**:
    ```bash
    # Create venv
    python3 -m venv venv
    
    # Activate venv
    # On Linux/macOS:
    source venv/bin/activate
    # On Windows:
    .\venv\Scripts\activate
    ```

2. **Install locally**:
    ```bash
    pip install -e .
    ```

Note: With this option, `gcommit` will only work when the virtual environment is activated.


## 🛠️ Usage

### ⚙️ Configuration Commands
#### List all available commit types:
```bash
python3 -m conventional_commits.config_cli list
```
#### Add a new commit type:
```bash
python3 -m conventional_commits.config_cli add "deploy" "🚀"
```
#### Modify an existing commit type:
```bash
python3 -m conventional_commits.config_cli modify "feat" "🌟"
```
#### Remove an unused commit type:
```bash
python3 -m conventional_commits.config_cli remove "wip"
```
#### Reset to default types:
```bash
python3 -m conventional_commits.config_cli reset
```

### 📝 Creating Commits
#### Basic Usage:
```bash
python3 -m conventional_commits.commit
```
#### Help Command:
```bash
commit --help
```
#### Test Mode:
```bash
gcommit testingthisPythonScript
```

## 📖 How It Works
1. The CLI guides you through the process of creating a structured commit message step-by-step.
2. Customize your commit with emojis, scopes, messages, and even breaking changes.
3. Ensure that your commit message is aligned with the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification.

## 👨‍💻 Example Commit Workflow
1. **Stage your changes** (if not already):
    ```bash
    git add .
    ```
2. **Run the commit command**:
    ```bash
    python3 -m conventional_commits.commit
    ```
3. **Follow the prompts** to select the type, emoji, scope, and message.
4. Confirm and enjoy your beautifully crafted commit message! 🎉

## 🛡️ Error Handling
- Handles input errors with friendly messages 😌
- Provides warnings if no changes are staged ⚠️
- Allows you to safely exit with `Ctrl+C` at any time 🛑

## 🧑‍🍳 Contributing
We welcome contributions from the community! Feel free to fork the repository, submit issues, or create pull requests. Let’s make committing fun for everyone! 🚀

## 📜 License
This project is licensed under the [MIT License](LICENSE).

---

Happy committing! 💾✨

