#!/usr/bin/env python3
"""
Project Cleanup Script

This script implements the cleanup plan to reorganize the project structure,
remove redundant files, and consolidate directories.
"""

import os
import shutil
import sys
from pathlib import Path
import filecmp

def confirm(message):
    """Ask for confirmation before proceeding."""
    response = input(f"{message} (y/n): ").lower().strip()
    return response == 'y'

def backup_file(file_path):
    """Create a backup of a file before modifying it."""
    backup_path = f"{file_path}.bak"
    if os.path.exists(file_path):
        shutil.copy2(file_path, backup_path)
        print(f"Backed up {file_path} to {backup_path}")
    return backup_path

def compare_directories(dir1, dir2):
    """Compare two directories to check if they have the same content."""
    if not os.path.exists(dir1) or not os.path.exists(dir2):
        return False
    
    dir1_files = set(os.listdir(dir1))
    dir2_files = set(os.listdir(dir2))
    
    # Check if all files in dir1 exist in dir2
    for file in dir1_files:
        path1 = os.path.join(dir1, file)
        path2 = os.path.join(dir2, file)
        
        if os.path.isdir(path1):
            if not os.path.isdir(path2) or not compare_directories(path1, path2):
                return False
        elif not os.path.exists(path2) or not filecmp.cmp(path1, path2):
            return False
    
    return True

def move_file(src, dest_dir):
    """Move a file to a destination directory."""
    if not os.path.exists(src):
        print(f"Warning: Source file {src} does not exist")
        return False
    
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    
    dest = os.path.join(dest_dir, os.path.basename(src))
    
    # Check if destination already exists
    if os.path.exists(dest):
        if filecmp.cmp(src, dest):
            print(f"File {src} is identical to {dest}, removing source")
            os.remove(src)
            return True
        else:
            print(f"Warning: Destination file {dest} already exists and differs from source")
            if confirm(f"Overwrite {dest} with {src}?"):
                backup_file(dest)
                shutil.copy2(src, dest)
                os.remove(src)
                return True
            return False
    
    # Move the file
    shutil.move(src, dest)
    print(f"Moved {src} to {dest}")
    return True

def cleanup_src_directory():
    """Clean up the src directory."""
    print("\n=== Cleaning up src directory ===")
    
    # Files to keep for testing
    keep_files = [
        "irrigation_decision_system_mock.py",
        "irrigation_decision_system_simplified.py",
        "mock_regional_knowledge_base.py"
    ]
    
    # Check if src directory exists
    if not os.path.exists("src"):
        print("src directory does not exist, skipping")
        return
    
    # Create a backup directory
    backup_dir = "src_backup"
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    # Process each file in src
    for file in os.listdir("src"):
        if file == "__init__.py":
            continue  # Keep __init__.py
        
        src_file = os.path.join("src", file)
        if os.path.isdir(src_file):
            continue  # Skip directories
        
        if file in keep_files:
            print(f"Keeping {src_file} for testing purposes")
            continue
        
        # Backup the file
        backup_path = os.path.join(backup_dir, file)
        shutil.copy2(src_file, backup_path)
        print(f"Backed up {src_file} to {backup_path}")
        
        # Remove the file
        os.remove(src_file)
        print(f"Removed {src_file}")

def consolidate_test_files():
    """Move test files to the tests directory."""
    print("\n=== Consolidating test files ===")
    
    test_files = [
        "test_irrigation_decision_system.py",
        "test_irrigation_mock.py",
        "test_irrigation_simplified.py",
        "test_machinery_optimization.py",
        "test_weather_client.py"
    ]
    
    for file in test_files:
        if os.path.exists(file):
            move_file(file, "tests")

def consolidate_scripts():
    """Clean up redundant scripts."""
    print("\n=== Consolidating scripts ===")
    
    scripts_to_remove = [
        "scripts/code_quality_fixer.py",
        "scripts/aggressive_code_quality_fixer.py",
        "scripts/final_release_preparation.py"
    ]
    
    # Create a backup directory
    backup_dir = "scripts_backup"
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    for script in scripts_to_remove:
        if os.path.exists(script):
            # Backup the script
            backup_path = os.path.join(backup_dir, os.path.basename(script))
            shutil.copy2(script, backup_path)
            print(f"Backed up {script} to {backup_path}")
            
            # Remove the script
            os.remove(script)
            print(f"Removed {script}")

def cleanup_report_files():
    """Move report files to the release_reports directory."""
    print("\n=== Cleaning up report files ===")
    
    report_files = [
        "comprehensive_test_results.txt",
        "docstring_coverage_report.txt",
        "mypy_detailed_report.txt",
        "mypy_report.txt",
        "mypy_strict_report.txt",
        "pylint_detailed_report.txt",
        "pylint_report.txt",
        "pylint_strict_report.txt",
        "test_results.txt"
    ]
    
    for file in report_files:
        if os.path.exists(file):
            move_file(file, "release_reports")

def consolidate_knowledge_base():
    """Consolidate knowledge base directories."""
    print("\n=== Consolidating knowledge base directories ===")
    
    if os.path.exists("knowledge_base") and os.path.exists("data/knowledge_base"):
        if compare_directories("knowledge_base", "data/knowledge_base"):
            print("knowledge_base and data/knowledge_base are identical")
            if confirm("Remove knowledge_base directory?"):
                shutil.rmtree("knowledge_base")
                print("Removed knowledge_base directory")
        else:
            print("Warning: knowledge_base and data/knowledge_base differ")
            if confirm("Merge knowledge_base into data/knowledge_base?"):
                # Implement merging logic here
                print("Merging not implemented yet, please do this manually")

def consolidate_resource_data():
    """Consolidate resource data directories."""
    print("\n=== Consolidating resource data directories ===")
    
    if os.path.exists("resource_data") and os.path.exists("data/resources"):
        if compare_directories("resource_data", "data/resources"):
            print("resource_data and data/resources are identical")
            if confirm("Remove resource_data directory?"):
                shutil.rmtree("resource_data")
                print("Removed resource_data directory")
        else:
            print("Warning: resource_data and data/resources differ")
            if confirm("Merge resource_data into data/resources?"):
                # Implement merging logic here
                print("Merging not implemented yet, please do this manually")

def main():
    """Main function to run the cleanup process."""
    print("=== Project Cleanup Script ===")
    
    if not confirm("This script will reorganize the project structure. Continue?"):
        print("Cleanup cancelled")
        return
    
    # Run cleanup functions
    cleanup_src_directory()
    consolidate_test_files()
    consolidate_scripts()
    cleanup_report_files()
    consolidate_knowledge_base()
    consolidate_resource_data()
    
    print("\n=== Cleanup completed ===")
    print("Please review the changes and run tests to ensure everything works correctly.")

if __name__ == "__main__":
    main()
