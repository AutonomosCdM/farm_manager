#!/usr/bin/env python3
import re
import sys
from pathlib import Path


def update_version(version_type):
    """
    Update project version across different files.
    Supports: major, minor, patch
    """
    # Files to update
    files_to_update = ["setup.py", "CHANGELOG.md"]

    # Read current version from setup.py
    setup_path = Path("setup.py")
    setup_content = setup_path.read_text()
    version_match = re.search(r"version='(\d+\.\d+\.\d+)'", setup_content)

    if not version_match:
        print("Could not find version in setup.py")
        sys.exit(1)

    current_version = version_match.group(1)
    major, minor, patch = map(int, current_version.split("."))

    # Update version based on type
    if version_type == "major":
        major += 1
        minor = 0
        patch = 0
    elif version_type == "minor":
        minor += 1
        patch = 0
    elif version_type == "patch":
        patch += 1
    else:
        print(f"Invalid version type: {version_type}. Use 'major', 'minor', or 'patch'.")
        sys.exit(1)

    new_version = f"{major}.{minor}.{patch}"

    # Update files
    for file_path in files_to_update:
        file = Path(file_path)
        content = file.read_text()

        if file_path == "setup.py":
            # Update version in setup.py
            updated_content = re.sub(
                r"version='(\d+\.\d+\.\d+)'", f"version='{new_version}'", content
            )
        elif file_path == "CHANGELOG.md":
            # Prepare changelog update
            changelog_path = Path(__file__).parent.parent / "CHANGELOG.md"
            changelog_content = changelog_path.read_text()
            first_line = changelog_content.split("\n")[0]

            updated_content = content.replace(
                f"## [{current_version}]",
                f"## [{new_version}] - {first_line.split('- ')[1]}",
            )

            # Add new Unreleased section
            updated_content = updated_content.replace(
                "## [Unreleased]",
                f"## [Unreleased]\n\n## [{current_version}] - {first_line.split('- ')[1]}",
            )

        file.write_text(updated_content)

    print(f"Updated version to {new_version}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python version_manager.py [major|minor|patch]")
        sys.exit(1)

    update_version(sys.argv[1])
