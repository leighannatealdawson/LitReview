#!/usr/bin/env python3
"""
Windows Setup Script for LitReview Species Extractor

Run this once to set everything up on Windows!
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors nicely."""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} - Done!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Error:")
        print(f"   {e.stderr}")
        return False

def main():
    print("🧬 Setting up LitReview Species Extractor for Windows")
    print("=" * 55)

    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required. Please upgrade Python.")
        print("   Download from: https://python.org/downloads")
        return

    print(f"✓ Python {sys.version.split()[0]} detected")

    # Determine which Python command to use
    python_cmd = sys.executable

    # Create virtual environment if it doesn't exist
    if not Path("venv").exists():
        if not run_command(f'"{python_cmd}" -m venv venv', "Creating virtual environment"):
            return
    else:
        print("✓ Virtual environment already exists")

    # Windows paths
    activate_cmd = "venv\\Scripts\\activate"
    pip_cmd = "venv\\Scripts\\pip"

    # Install requirements (look for it in the info directory where this script is)
    script_dir = Path(__file__).parent
    requirements_path = script_dir / "requirements.txt"

    if not run_command(f'"{pip_cmd}" install -r {requirements_path}', "Installing Python packages (this may take a few minutes)"):
        print("\n⚠️  Installation had issues. Let's try upgrading pip first...")
        run_command(f'"{pip_cmd}" install --upgrade pip', "Upgrading pip")
        if not run_command(f'"{pip_cmd}" install -r {requirements_path}', "Retrying package installation"):
            return

    # Download spaCy model
    run_command(f'"{python_cmd}" -m spacy download en_core_web_sm', "Downloading spaCy English model")

    # Test the installation
    test_cmd = f'"{pip_cmd}" list | findstr taxonerd'
    if run_command(test_cmd, "Verifying TaxoNERD installation"):
        print("\n🎉 Setup complete!")
        print("\nNext steps:")
        print(f"1. Activate the environment: {activate_cmd}")
        print(f'2. Try the example: "{python_cmd}" scripts\\extract_species.py data\\input\\example_papers.csv')
        print("3. Put your own CSV files in data\\input\\ and run the script!")
        print("\n💡 Pro tip: You can drag files into Command Prompt to get their full path!")
    else:
        print("\n⚠️  Setup completed but couldn't verify TaxoNERD installation.")
        print("Try running the example anyway - it might still work!")

if __name__ == "__main__":
    main()