#!/usr/bin/env python3
import sys
import os

# Resolve the actual path of this script (chasing symlinks)
script_path = os.path.abspath(os.path.realpath(__file__))
current_dir = os.path.dirname(script_path)
package_root = os.path.dirname(current_dir)

# Add the package root to sys.path
if package_root not in sys.path:
    sys.path.insert(0, package_root)

# Debug: Print paths if import fails
try:
    from sentinelx.core.menu import main_menu
except ImportError as e:
    print(f"Error: Could not import sentinelx package: {e}")
    print(f"Script Path: {script_path}")
    print(f"Package Root Calculated: {package_root}")
    print(f"Sys Path: {sys.path}")
    sys.exit(1)

def main():
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\nExiting SentinelX...")
        sys.exit(0)

if __name__ == "__main__":
    main()
