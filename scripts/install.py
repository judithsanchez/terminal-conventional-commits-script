import os
import platform
import subprocess
import sys

def install_dependencies():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-e", "."])

def setup_windows():
    print("Setting up for Windows...")
    install_dependencies()
    # Add Windows-specific setup here if needed

def setup_linux():
    print("Setting up for Linux...")
    
    # Create virtual environment
    venv_path = os.path.join(os.getcwd(), "venv")
    subprocess.check_call([sys.executable, "-m", "venv", venv_path])
    
    # Get path to pip in virtual environment
    if platform.system().lower() == "windows":
        pip_path = os.path.join(venv_path, "Scripts", "pip")
        python_path = os.path.join(venv_path, "Scripts", "python")
    else:
        pip_path = os.path.join(venv_path, "bin", "pip")
        python_path = os.path.join(venv_path, "bin", "python")
    
    # Install dependencies using venv pip
    subprocess.check_call([python_path, "-m", "pip", "install", "-e", "."])
    
    print(f"\nVirtual environment created at: {venv_path}")
    print("To activate the virtual environment:")
    print(f"source {os.path.join(venv_path, 'bin', 'activate')}")

def setup_macos():
    print("Setting up for macOS...")
    try:
        # Check if Homebrew is installed
        subprocess.run(["brew", "--version"], check=True)
    except FileNotFoundError:
        print("Installing Homebrew...")
        homebrew_install = '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
        os.system(homebrew_install)
    
    install_dependencies()

def main():
    system = platform.system().lower()
    
    if system == "windows":
        setup_windows()
    elif system == "linux":
        setup_linux()
    elif system == "darwin":
        setup_macos()
    else:
        print(f"Unsupported operating system: {system}")
        sys.exit(1)
    
    print("Installation completed successfully!")

if __name__ == "__main__":
    main()
