#!/usr/bin/env python3
"""
Complete Cleanup Script

This script completes the cleanup process by:
1. Merging knowledge_base into data/knowledge_base
2. Providing options for virtual environment management
3. Checking for import issues in Python files
"""

import os
import shutil
import sys
from pathlib import Path
import re
import subprocess

def confirm(message):
    """Ask for confirmation before proceeding."""
    response = input(f"{message} (y/n): ").lower().strip()
    return response == 'y'

def merge_knowledge_base():
    """Merge knowledge_base into data/knowledge_base."""
    print("\n=== Merging knowledge_base directories ===")
    
    if not os.path.exists("knowledge_base") or not os.path.exists("data/knowledge_base"):
        print("One or both knowledge_base directories do not exist, skipping")
        return
    
    # Check what's in each directory
    kb_files = set(os.listdir("knowledge_base"))
    data_kb_files = set(os.listdir("data/knowledge_base"))
    
    print("Files in knowledge_base/:")
    for file in kb_files:
        print(f"  - {file}")
    
    print("\nFiles in data/knowledge_base/:")
    for file in data_kb_files:
        print(f"  - {file}")
    
    print("\nMerging strategy:")
    print("1. Copy chroma.sqlite3 from knowledge_base/ to data/knowledge_base/")
    print("2. Copy UUID directories from knowledge_base/ to data/knowledge_base/")
    print("3. Keep config.json in data/knowledge_base/")
    
    if confirm("\nProceed with merge?"):
        # Copy chroma.sqlite3
        if os.path.exists("knowledge_base/chroma.sqlite3"):
            shutil.copy2("knowledge_base/chroma.sqlite3", "data/knowledge_base/")
            print("Copied chroma.sqlite3 to data/knowledge_base/")
        
        # Copy UUID directories
        for item in os.listdir("knowledge_base"):
            src_path = os.path.join("knowledge_base", item)
            if os.path.isdir(src_path) and re.match(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', item):
                dest_path = os.path.join("data/knowledge_base", item)
                if os.path.exists(dest_path):
                    print(f"Warning: {dest_path} already exists, skipping")
                else:
                    shutil.copytree(src_path, dest_path)
                    print(f"Copied {src_path} to {dest_path}")
        
        # Create a backup of the knowledge_base directory
        backup_dir = "knowledge_base_backup"
        if os.path.exists(backup_dir):
            shutil.rmtree(backup_dir)
        shutil.copytree("knowledge_base", backup_dir)
        print(f"Created backup of knowledge_base in {backup_dir}")
        
        # Ask if the user wants to remove the original knowledge_base directory
        if confirm("Remove original knowledge_base directory?"):
            shutil.rmtree("knowledge_base")
            print("Removed knowledge_base directory")
        
        print("Merge completed successfully")
    else:
        print("Merge cancelled")

def manage_virtual_environments():
    """Provide options for virtual environment management."""
    print("\n=== Virtual Environment Management ===")
    
    venv_farm_manager_exists = os.path.exists("venv_farm_manager")
    venv_stable_exists = os.path.exists("venv_stable")
    
    if not venv_farm_manager_exists and not venv_stable_exists:
        print("No virtual environment directories found, skipping")
        return
    
    print("Virtual environment directories found:")
    if venv_farm_manager_exists:
        print("  - venv_farm_manager")
    if venv_stable_exists:
        print("  - venv_stable")
    
    print("\nOptions:")
    print("1. Keep both virtual environments")
    print("2. Keep only venv_farm_manager (recommended if it's the active one)")
    print("3. Keep only venv_stable")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice == "1":
        print("Keeping both virtual environments")
    elif choice == "2" and venv_stable_exists:
        if confirm("Remove venv_stable directory?"):
            shutil.rmtree("venv_stable")
            print("Removed venv_stable directory")
    elif choice == "3" and venv_farm_manager_exists:
        if confirm("Remove venv_farm_manager directory?"):
            shutil.rmtree("venv_farm_manager")
            print("Removed venv_farm_manager directory")
            print("Note: You may need to create a new virtual environment and reinstall dependencies")
    else:
        print("Invalid choice or virtual environment does not exist")

def check_import_issues():
    """Check for potential import issues in Python files."""
    print("\n=== Checking for Import Issues ===")
    
    # Find all Python files
    python_files = []
    for root, _, files in os.walk("."):
        if ".git" in root or "venv" in root:
            continue
        for file in files:
            if file.endswith(".py"):
                python_files.append(os.path.join(root, file))
    
    print(f"Found {len(python_files)} Python files")
    
    # Look for imports that might need to be updated
    old_imports = [
        r"from\s+src\.",
        r"import\s+src\.",
        r"from\s+test_resource_data\.",
        r"import\s+test_resource_data\."
    ]
    
    files_with_issues = []
    
    for file_path in python_files:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
            for pattern in old_imports:
                if re.search(pattern, content):
                    files_with_issues.append((file_path, pattern))
    
    if files_with_issues:
        print("\nPotential import issues found:")
        for file_path, pattern in files_with_issues:
            print(f"  - {file_path}: {pattern}")
        
        print("\nYou may need to manually update these imports to reflect the new structure.")
    else:
        print("No obvious import issues found")

def main():
    """Main function to run the complete cleanup process."""
    print("=== Complete Cleanup Script ===")
    
    if not confirm("This script will complete the cleanup process. Continue?"):
        print("Cleanup cancelled")
        return
    
    # Merge knowledge_base directories
    merge_knowledge_base()
    
    # Manage virtual environments
    manage_virtual_environments()
    
    # Check for import issues
    check_import_issues()
    
    print("\n=== Complete cleanup finished ===")
    print("Please review the changes and run tests to ensure everything works correctly.")

if __name__ == "__main__":
    main()
