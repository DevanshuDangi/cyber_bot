#!/usr/bin/env python3
"""
Cross-platform setup script for 1930 Cyber Crime Helpline WhatsApp Chatbot
Works on Windows, macOS, and Linux
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

# Colors for terminal output (ANSI codes)
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color

def print_info(msg):
    print(f"{Colors.BLUE}[INFO]{Colors.NC} {msg}")

def print_success(msg):
    print(f"{Colors.GREEN}[SUCCESS]{Colors.NC} {msg}")

def print_warning(msg):
    print(f"{Colors.YELLOW}[WARNING]{Colors.NC} {msg}")

def print_error(msg):
    print(f"{Colors.RED}[ERROR]{Colors.NC} {msg}")

def check_command(cmd, name, install_url=None):
    """Check if a command exists"""
    if shutil.which(cmd):
        version = subprocess.run([cmd, "--version"], capture_output=True, text=True)
        print_success(f"{name} found: {version.stdout.split()[0] if version.returncode == 0 else 'installed'}")
        return True
    else:
        print_error(f"{name} is not installed.")
        if install_url:
            print_info(f"Install from: {install_url}")
        return False

def run_command(cmd, cwd=None, check=True):
    """Run a command and handle errors"""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, check=check, 
                              capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        return False, e.stdout, e.stderr

def main():
    print("")
    print("=" * 50)
    print("  1930 Cyber Crime Helpline Chatbot")
    print("  Automated Setup Script")
    print("=" * 50)
    print("")
    
    # Check Python
    print_info("Checking Python installation...")
    if not check_command("python3", "Python 3", "https://www.python.org/downloads/"):
        if platform.system() == "Windows":
            if not check_command("python", "Python"):
                sys.exit(1)
        else:
            sys.exit(1)
    
    # Check Node.js
    print_info("Checking Node.js installation...")
    if not check_command("node", "Node.js", "https://nodejs.org/"):
        sys.exit(1)
    
    # Check npm
    print_info("Checking npm installation...")
    if not check_command("npm", "npm"):
        sys.exit(1)
    
    print("")
    print_info("Starting setup process...")
    print("")
    
    # Step 1: Create virtual environment
    print_info("Step 1: Setting up Python virtual environment...")
    venv_path = Path("venv")
    if venv_path.exists():
        print_warning("Virtual environment already exists. Skipping creation.")
    else:
        python_cmd = "python3" if shutil.which("python3") else "python"
        success, _, _ = run_command(f"{python_cmd} -m venv venv")
        if success:
            print_success("Virtual environment created")
        else:
            print_error("Failed to create virtual environment")
            sys.exit(1)
    
    # Step 2: Activate and install backend dependencies
    print_info("Step 2: Installing backend dependencies...")
    
    # Determine activation script based on OS
    if platform.system() == "Windows":
        activate_script = "venv\\Scripts\\activate"
        pip_cmd = "venv\\Scripts\\pip"
        python_cmd = "venv\\Scripts\\python"
    else:
        activate_script = "venv/bin/activate"
        pip_cmd = "venv/bin/pip"
        python_cmd = "venv/bin/python"
    
    # Upgrade pip
    print_info("Upgrading pip...")
    run_command(f"{pip_cmd} install --upgrade pip", check=False)
    
    # Install requirements
    print_info("Installing Python packages...")
    requirements_file = Path("backend/requirements.txt")
    if not requirements_file.exists():
        print_error("backend/requirements.txt not found")
        sys.exit(1)
    
    success, _, error = run_command(f"{pip_cmd} install -r {requirements_file}")
    if success:
        print_success("Backend dependencies installed")
    else:
        print_error(f"Failed to install backend dependencies: {error}")
        sys.exit(1)
    
    # Step 3: Install frontend dependencies
    print_info("Step 3: Installing frontend dependencies...")
    admin_ui_path = Path("admin-ui")
    if not admin_ui_path.exists():
        print_warning("admin-ui directory not found. Skipping frontend setup.")
    else:
        package_json = admin_ui_path / "package.json"
        if not package_json.exists():
            print_error("package.json not found in admin-ui directory")
            sys.exit(1)
        
        print_info("Running npm install...")
        success, _, error = run_command("npm install", cwd=admin_ui_path)
        if success:
            print_success("Frontend dependencies installed")
        else:
            print_error(f"Failed to install frontend dependencies: {error}")
            sys.exit(1)
    
    # Step 4: Create .env file
    print_info("Step 4: Checking environment configuration...")
    env_file = Path(".env")
    if not env_file.exists():
        print_warning(".env file not found. Creating template...")
        env_content = """# WhatsApp Business API Configuration
VERIFY_TOKEN=cyberbot123
WHATSAPP_TOKEN=
PHONE_NUMBER_ID=
GRAPH_VERSION=v21.0
DEBUG_PRINT_REPLY=1

# Google Gemini API Configuration
GEMINI_API_KEY=

# Note: Fill in the above values with your actual API credentials
"""
        env_file.write_text(env_content)
        print_success(".env template created")
        print_warning("Please update .env file with your API credentials")
    else:
        print_success(".env file exists")
    
    # Step 5: Create directories
    print_info("Step 5: Creating necessary directories...")
    for dir_name in ["media", "reports"]:
        dir_path = Path(dir_name)
        dir_path.mkdir(exist_ok=True)
    print_success("Directories created")
    
    print("")
    print_success("Setup completed successfully!")
    print("")
    print("=" * 50)
    print("  Setup Complete!")
    print("=" * 50)
    print("")
    print("Next steps:")
    print("1. Update .env file with your API credentials")
    print("2. Run './start.sh' (Linux/macOS) or 'start.bat' (Windows) to start servers")
    print("")

if __name__ == "__main__":
    main()

