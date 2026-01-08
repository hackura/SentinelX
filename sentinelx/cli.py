#!/usr/bin/env python3
import sys
import os

# Ensure the script can see the package if run locally
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from sentinelx.core.menu import main_menu
except ImportError:
    # Fallback for installed package
    from .core.menu import main_menu

def main():
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\nExiting SentinelX...")
        sys.exit(0)

if __name__ == "__main__":
    main()
