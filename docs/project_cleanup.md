# Project Cleanup Guide

This guide explains the cleanup process for the farm management project to improve organization and remove redundant files.

## Overview

The project has accumulated duplicate code, redundant test files, and multiple versions of similar scripts. This cleanup process aims to:

1. Remove duplicate code
2. Consolidate test files
3. Remove redundant scripts
4. Organize report files
5. Consolidate knowledge base and resource data directories

## Cleanup Plan

A detailed cleanup plan is available in `cleanup_plan.md`. It identifies specific issues and recommends actions to address them.

## Cleanup Script

The `scripts/project_cleanup.py` script automates the cleanup process. It will:

- Back up files before removing them
- Move test files to the `tests/` directory
- Remove redundant scripts
- Move report files to the `release_reports/` directory
- Consolidate knowledge base and resource data directories

## How to Use

1. **Review the cleanup plan**:
   ```
   cat cleanup_plan.md
   ```

2. **Run the cleanup script**:
   ```
   ./scripts/project_cleanup.py
   ```
   
   The script will ask for confirmation before making changes and create backups of removed files.

3. **Verify the changes**:
   After running the script, verify that the project structure is as expected and that all functionality is preserved.

4. **Run tests**:
   ```
   pytest
   ```
   
   Ensure that all tests pass after the cleanup.

## Project Structure After Cleanup

After cleanup, the project structure should be:

```
farm_manager/           # Main package
├── calendar/           # Calendar functionality
├── core/               # Core functionality
├── irrigation/         # Irrigation functionality
├── knowledge/          # Knowledge base functionality
├── resources/          # Resource management
├── weather/            # Weather functionality
└── workflows/          # Workflow templates

data/                   # Data directory
├── knowledge_base/     # Knowledge base data
└── resources/          # Resource data

tests/                  # All test files
release_reports/        # All report files
scripts/                # Utility scripts
docs/                   # Documentation
```

## Backup Directories

The cleanup script creates the following backup directories:

- `src_backup/`: Backup of removed files from the `src/` directory
- `scripts_backup/`: Backup of removed script files

These backups can be removed once you've verified that the cleanup was successful.
