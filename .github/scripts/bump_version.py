#!/usr/bin/env python3
"""Bump version in __about__.py file."""

import os
import re
import sys

def bump_version(about_file: str, new_version: str) -> None:
    """Update version in __about__.py file.
    
    Args:
        about_file: Path to __about__.py file
        new_version: New version string (e.g., "1.0.0")
    """
    if not os.path.exists(about_file):
        print(f"Error: File {about_file} not found", file=sys.stderr)
        sys.exit(1)
    
    with open(about_file, "r", encoding="utf-8") as f:
        data = f.read()
    
    # Check which format is used and update accordingly
    if "__version__" in data:
        updated = re.sub(
            r'__version__\s*=\s*"[^"]*"',
            f'__version__ = "{new_version}"',
            data
        )
    else:
        updated = re.sub(
            r'version\s*=\s*"[^"]*"',
            f'version = "{new_version}"',
            data
        )
    
    with open(about_file, "w", encoding="utf-8") as f:
        f.write(updated)
    
    print(f"✓ Updated {about_file} to version {new_version}")


if __name__ == "__main__":
    about_file = os.environ.get("ABOUT_FILE")
    new_version = os.environ.get("NEW_VERSION")
    
    if not about_file or not new_version:
        print("Error: ABOUT_FILE and NEW_VERSION environment variables required", file=sys.stderr)
        sys.exit(1)
    
    bump_version(about_file, new_version)
