#!/usr/bin/env python3
"""
Windows Setup Script for LitReview Species Extractor

Run this once to set everything up on Windows!
"""

import subprocess
import sys
import os
import platform
from pathlib import Path

def run_command(command, description, show_output=False):
    """Run a command and handle errors nicely."""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        if show_output and result.stdout:
            print(f"   {result.stdout.strip()}")
        print(f"✓ {description} - Done!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Error:")
        if e.stderr:
            print(f"   {e.stderr.strip()}")
        if e.stdout:
            print(f"   {e.stdout.strip()}")
        return False

def check_compiler():
    """Check if a C++ compiler is available on Windows."""
    compilers_to_check = [
        ('cl', 'Microsoft Visual C++ (MSVC)'),
        ('gcc', 'GCC'),
        ('clang', 'Clang')
    ]

    available_compilers = []
    for compiler, name in compilers_to_check:
        try:
            result = subprocess.run([compiler, '--version'], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                available_compilers.append(name)
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.CalledProcessError):
            try:
                # Try alternative flags for MSVC
                if compiler == 'cl':
                    result = subprocess.run([compiler, '/?'], capture_output=True, text=True, timeout=10)
                    if result.returncode == 0:
                        available_compilers.append(name)
            except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.CalledProcessError):
                pass

    return available_compilers

def install_with_fallbacks(pip_cmd, requirements_path):
    """Try multiple installation strategies for better Windows compatibility."""

    # Strategy 1: Try installing with pre-built wheels first
    print("\n📦 Attempting installation with pre-built wheels...")
    wheel_strategy_cmd = f'"{pip_cmd}" install --only-binary=all -r "{requirements_path}"'
    if run_command(wheel_strategy_cmd, "Installing with pre-built wheels only"):
        return True

    # Strategy 2: Try upgrading pip and setuptools first
    print("\n🔧 Upgrading build tools...")
    run_command(f'"{pip_cmd}" install --upgrade pip setuptools wheel', "Upgrading pip, setuptools, and wheel")

    # Strategy 3: Install specific problematic packages individually with wheels
    print("\n📦 Installing core scientific packages individually...")
    core_packages = [
        "numpy>=1.24.0",  # Use slightly older numpy version with better wheel support
        "pandas>=1.5.0",
        "spacy>=3.4.0"
    ]

    for package in core_packages:
        wheel_cmd = f'"{pip_cmd}" install --only-binary=:all: "{package}"'
        if not run_command(wheel_cmd, f"Installing {package} (wheel only)"):
            print(f"⚠️  Could not install {package} as wheel, trying regular install...")
            regular_cmd = f'"{pip_cmd}" install "{package}"'
            if not run_command(regular_cmd, f"Installing {package} (regular)"):
                print(f"❌ Failed to install {package}")
                return False

    # Strategy 4: Install taxonerd last (it depends on the above packages)
    print("\n🧬 Installing TaxoNERD...")
    taxonerd_cmd = f'"{pip_cmd}" install taxonerd>=1.5.0'
    if not run_command(taxonerd_cmd, "Installing TaxoNERD"):
        print("⚠️  TaxoNERD installation failed, trying with --no-deps...")
        nodeps_cmd = f'"{pip_cmd}" install --no-deps taxonerd>=1.5.0'
        if not run_command(nodeps_cmd, "Installing TaxoNERD (no dependencies)"):
            return False

    return True

def main():
    print("🧬 Setting up LitReview Species Extractor for Windows")
    print("=" * 55)

    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required. Please upgrade Python.")
        print("   Download from: https://python.org/downloads")
        return

    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    print(f"✓ Python {python_version} detected")

    # Check for very new Python versions that may not have wheels
    if sys.version_info >= (3, 13):
        print("⚠️  You're using a very new Python version (3.13+).")
        print("   Some packages may need to be compiled from source.")
        print("   This setup script will try to use pre-built wheels when possible.\n")

    # Check for C++ compiler availability
    print("🔍 Checking for C++ compiler...")
    available_compilers = check_compiler()
    if available_compilers:
        print(f"✓ Found compiler(s): {', '.join(available_compilers)}")
    else:
        print("⚠️  No C++ compiler detected.")
        print("   Don't worry - we'll try to use pre-built packages!")
        print("   If installation fails, consider installing:")
        print("   - Microsoft C++ Build Tools: https://visualstudio.microsoft.com/visual-cpp-build-tools/")
        print("   - Or Visual Studio Community: https://visualstudio.microsoft.com/vs/community/\n")

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

    # Install requirements using fallback strategy
    script_dir = Path(__file__).parent
    requirements_path = script_dir / "requirements.txt"

    # Try compatible requirements for newer Python versions
    compatible_requirements = script_dir / "requirements-compatible.txt"
    if sys.version_info >= (3, 13) and compatible_requirements.exists():
        print(f"\n📋 Using Python 3.13+ compatible requirements...")
        requirements_path = compatible_requirements

    print(f"\n📋 Installing packages from {requirements_path}")
    if not install_with_fallbacks(pip_cmd, requirements_path):
        print("\n❌ Package installation failed!")
        print("\nTroubleshooting suggestions:")
        print("1. Install Microsoft C++ Build Tools:")
        print("   https://visualstudio.microsoft.com/visual-cpp-build-tools/")
        print("2. Try using Python 3.11 or 3.12 instead of 3.13")
        print("3. Use Anaconda/Miniconda which includes compiled packages:")
        print("   https://docs.conda.io/en/latest/miniconda.html")
        return

    # Download spaCy model
    print("\n📚 Setting up language models...")
    spacy_python = f"venv\\Scripts\\python"
    if not run_command(f'"{spacy_python}" -m spacy download en_core_web_sm', "Downloading spaCy English model"):
        print("⚠️  SpaCy model download failed. You may need to download it manually later.")
        print('   Run: python -m spacy download en_core_web_sm')

    # Test the installation
    print("\n🧪 Testing installation...")
    test_cmd = f'"{pip_cmd}" list'
    if run_command(test_cmd, "Listing installed packages", show_output=False):
        # Check for key packages
        try:
            result = subprocess.run(f'"{pip_cmd}" show taxonerd', shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                print("✓ TaxoNERD installation verified!")
                print("\n🎉 Setup complete!")
            else:
                print("⚠️  TaxoNERD may not be properly installed.")
                print("🎉 Setup mostly complete!")
        except:
            print("🎉 Setup complete!")

        print("\nNext steps:")
        print(f"1. Activate the environment: {activate_cmd}")
        print("2. Navigate to the main LitReview directory")
        print('3. Try the example: python scripts\\extract_species.py data\\input\\example_papers.csv')
        print("4. Put your own CSV files in data\\input\\ and run the script!")
        print("\n💡 Pro tips:")
        print("• You can drag files into Command Prompt to get their full path!")
        print("• If you get import errors, try restarting Command Prompt")
        print("• For large files, processing may take several minutes")

    else:
        print("⚠️  Could not verify installation, but packages may still work.")
        print("Try running the example script to test!")

if __name__ == "__main__":
    main()