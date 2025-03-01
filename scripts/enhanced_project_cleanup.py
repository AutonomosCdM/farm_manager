#!/usr/bin/env python3
"""
Enhanced Project Cleanup Script

This script implements the enhanced cleanup plan to thoroughly reorganize 
the project structure and create a cleaner directory layout.
"""

import os
import shutil
import sys
from pathlib import Path
import filecmp
import re

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

def ensure_directory(directory):
    """Ensure a directory exists, creating it if necessary."""
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")
    return directory

def move_file(src, dest_dir, new_name=None):
    """Move a file to a destination directory, optionally renaming it."""
    if not os.path.exists(src):
        print(f"Warning: Source file {src} does not exist")
        return False
    
    ensure_directory(dest_dir)
    
    dest_name = new_name if new_name else os.path.basename(src)
    dest = os.path.join(dest_dir, dest_name)
    
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

def create_directory_structure():
    """Create the enhanced directory structure."""
    print("\n=== Creating directory structure ===")
    
    directories = [
        "config",
        "config/linting",
        "config/mypy",
        "reports",
        "reports/code_quality",
        "reports/test_results",
        "reports/release",
    ]
    
    for directory in directories:
        ensure_directory(directory)

def move_configuration_files():
    """Move configuration files to the config directory."""
    print("\n=== Moving configuration files ===")
    
    config_files = [
        (".pylintrc", "config/linting", "pylintrc"),
        ("mypy.ini", "config/mypy", "mypy.ini"),
        ("setup.cfg", "config", None)
    ]
    
    for src, dest_dir, new_name in config_files:
        if os.path.exists(src):
            move_file(src, dest_dir, new_name)

def move_report_files():
    """Move report files to the reports directory."""
    print("\n=== Moving report files ===")
    
    code_quality_reports = [
        "pylint_report.txt",
        "pylint_detailed_report.txt",
        "pylint_strict_report.txt",
        "mypy_report.txt",
        "mypy_detailed_report.txt",
        "mypy_strict_report.txt",
        "docstring_coverage_report.txt"
    ]
    
    test_results = [
        "test_results.txt",
        "comprehensive_test_results.txt"
    ]
    
    # Move existing release reports
    if os.path.exists("release_reports"):
        for file in os.listdir("release_reports"):
            src = os.path.join("release_reports", file)
            if os.path.isfile(src):
                move_file(src, "reports/release")
        
        # Remove the old directory if it's empty
        if not os.listdir("release_reports"):
            os.rmdir("release_reports")
            print("Removed empty directory: release_reports")
    
    # Move code quality reports
    for file in code_quality_reports:
        if os.path.exists(file):
            move_file(file, "reports/code_quality")
    
    # Move test results
    for file in test_results:
        if os.path.exists(file):
            move_file(file, "reports/test_results")

def move_documentation_files():
    """Move documentation files to the docs directory."""
    print("\n=== Moving documentation files ===")
    
    doc_files = [
        "NOTES.md",
        "plan_agricola.md",
        "plan_reestructuracion.md",
        "cleanup_plan.md",
        "enhanced_cleanup_plan.md",
        ("PROJECT_CLEANUP_README.md", "project_cleanup.md")
    ]
    
    for file in doc_files:
        if isinstance(file, tuple):
            src, new_name = file
            if os.path.exists(src):
                move_file(src, "docs", new_name)
        else:
            if os.path.exists(file):
                move_file(file, "docs")

def move_test_files():
    """Move test files to the tests directory."""
    print("\n=== Moving test files ===")
    
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
    
    # Move test_resource_data to tests if it exists
    if os.path.exists("test_resource_data"):
        ensure_directory("tests/test_resource_data")
        for file in os.listdir("test_resource_data"):
            src = os.path.join("test_resource_data", file)
            if os.path.isfile(src):
                move_file(src, "tests/test_resource_data")
        
        # Remove the old directory if it's empty
        if not os.listdir("test_resource_data"):
            os.rmdir("test_resource_data")
            print("Removed empty directory: test_resource_data")

def consolidate_knowledge_base():
    """Consolidate knowledge base directories."""
    print("\n=== Consolidating knowledge base directories ===")
    
    if os.path.exists("knowledge_base") and os.path.exists("data/knowledge_base"):
        print("Checking knowledge_base and data/knowledge_base directories...")
        
        # Simple check: if knowledge_base is empty or only has UUID directories, it can be removed
        kb_is_empty = True
        for item in os.listdir("knowledge_base"):
            # Check if item is a UUID directory (common for vector stores)
            if not (os.path.isdir(os.path.join("knowledge_base", item)) and 
                   re.match(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', item)):
                kb_is_empty = False
                break
        
        if kb_is_empty:
            print("knowledge_base directory appears to contain only UUID directories")
            if confirm("Remove knowledge_base directory?"):
                shutil.rmtree("knowledge_base")
                print("Removed knowledge_base directory")
        else:
            print("Warning: knowledge_base directory contains non-UUID files/directories")
            if confirm("Merge knowledge_base into data/knowledge_base? (This will require manual review)"):
                print("Please merge these directories manually and review the results")

def consolidate_resource_data():
    """Consolidate resource data directories."""
    print("\n=== Consolidating resource data directories ===")
    
    if os.path.exists("resource_data") and os.path.exists("data/resources"):
        print("Checking resource_data and data/resources directories...")
        
        # Check if the directories have the same files
        resource_files = set(os.listdir("resource_data"))
        data_resource_files = set(os.listdir("data/resources"))
        
        if resource_files == data_resource_files:
            all_identical = True
            for file in resource_files:
                src = os.path.join("resource_data", file)
                dest = os.path.join("data/resources", file)
                if not (os.path.isfile(src) and os.path.isfile(dest) and filecmp.cmp(src, dest)):
                    all_identical = False
                    break
            
            if all_identical:
                print("resource_data and data/resources contain identical files")
                if confirm("Remove resource_data directory?"):
                    shutil.rmtree("resource_data")
                    print("Removed resource_data directory")
            else:
                print("Warning: Files with the same names differ between directories")
                if confirm("Merge resource_data into data/resources? (This will require manual review)"):
                    print("Please merge these directories manually and review the results")
        else:
            print("Warning: resource_data and data/resources contain different files")
            if confirm("Merge resource_data into data/resources? (This will require manual review)"):
                print("Please merge these directories manually and review the results")

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
    ensure_directory(backup_dir)
    
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

def update_imports():
    """Update imports in Python files to reflect the new structure."""
    print("\n=== Updating imports (this is a placeholder) ===")
    print("Note: You may need to manually update imports in your Python files")
    print("This would require parsing and modifying Python files, which is beyond the scope of this script")

def main():
    """Main function to run the enhanced cleanup process."""
    print("=== Enhanced Project Cleanup Script ===")
    
    if not confirm("This script will thoroughly reorganize the project structure. Continue?"):
        print("Cleanup cancelled")
        return
    
    # Create the directory structure
    create_directory_structure()
    
    # Move files to their appropriate locations
    move_configuration_files()
    move_report_files()
    move_documentation_files()
    move_test_files()
    
    # Consolidate directories
    consolidate_knowledge_base()
    consolidate_resource_data()
    cleanup_src_directory()
    
    # Update imports (placeholder)
    update_imports()
    
    print("\n=== Enhanced cleanup completed ===")
    print("Please review the changes and run tests to ensure everything works correctly.")
    print("You may need to manually update imports in your Python files.")

if __name__ == "__main__":
    main()
