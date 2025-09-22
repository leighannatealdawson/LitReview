#!/usr/bin/env python3
"""
Quick script to run the example and test everything works!
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    print("🧪 Testing LitReview with example data")
    print("=" * 40)

    # Check if we're in a virtual environment
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("⚠️  Virtual environment not activated!")
        if os.name == 'nt':  # Windows
            print("   Run: venv\\Scripts\\activate")
        else:  # Mac/Linux
            print("   Run: source venv/bin/activate")
        print("   Then try again")
        return

    # Check if example file exists (go up one level from info/ directory)
    project_root = Path(__file__).parent.parent
    example_file = project_root / "data/input/example_papers.csv"
    extract_script = project_root / "scripts/extract_species.py"

    if not example_file.exists():
        print(f"❌ Example file not found: {example_file}")
        return

    if not extract_script.exists():
        print(f"❌ Extract script not found: {extract_script}")
        return

    # Run the example
    command = [sys.executable, str(extract_script), str(example_file)]

    print("🔍 Running species extraction on example papers...")
    print("   (This might take a minute or two)")
    print()

    try:
        subprocess.run(command, check=True)
        print("\n🎉 Example completed successfully!")
        print("   Check data/output/ for the results!")
    except subprocess.CalledProcessError:
        print("\n❌ Something went wrong. Check the error messages above.")
    except FileNotFoundError:
        print("\n❌ Could not find the extraction script.")

if __name__ == "__main__":
    main()