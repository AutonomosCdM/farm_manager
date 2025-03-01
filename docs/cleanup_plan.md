# Project Cleanup Plan

## Identified Issues

1. **Duplicate Code**: The `src/` directory contains modules that duplicate functionality in the `farm_manager/` package
2. **Redundant Test Files**: Multiple test files in both root directory and `tests/` folder
3. **Redundant Scripts**: Several similar code quality scripts with overlapping functionality
4. **Multiple Report Files**: Various report files scattered in the root directory
5. **Duplicate Knowledge Base Directories**: Both `knowledge_base/` and `data/knowledge_base/`
6. **Duplicate Resource Data Directories**: Both `resource_data/` and `data/resources/`

## Recommended Actions

### 1. Remove Duplicate Code
The `src/` directory appears to be an older version of the code that has been refactored into the `farm_manager/` package:

| Remove (src/) | Keep (farm_manager/) |
|---------------|----------------------|
| agricultural_calendar.py | farm_manager/calendar/crop_calendar.py |
| irrigation_decision_system.py | farm_manager/irrigation/decision_system.py |
| irrigation_decision_system_mock.py | (Keep for testing if needed) |
| irrigation_decision_system_simplified.py | (Keep for testing if needed) |
| machinery_optimization_demo.py | farm_manager/resources/optimizer.py |
| mock_regional_knowledge_base.py | (Keep for testing if needed) |
| regional_knowledge_base.py | farm_manager/knowledge/base.py |
| resource_management.py | farm_manager/resources/manager.py |
| weather_client.py | farm_manager/weather/client.py |
| workflow_templates.py | farm_manager/workflows/template.py |

### 2. Consolidate Test Files
Move all test files to the `tests/` directory:

| Move | To |
|------|---|
| test_irrigation_decision_system.py | tests/ |
| test_irrigation_mock.py | tests/ |
| test_irrigation_simplified.py | tests/ |
| test_machinery_optimization.py | tests/ |
| test_weather_client.py | tests/ |

### 3. Consolidate Scripts
Keep only the most comprehensive script and remove redundant ones:

| Action | Script |
|--------|--------|
| Keep | scripts/comprehensive_code_improver.py |
| Remove | scripts/code_quality_fixer.py |
| Remove | scripts/aggressive_code_quality_fixer.py |
| Keep | scripts/final_review_and_release.py |
| Remove | scripts/final_release_preparation.py (functionality in final_review_and_release.py) |

### 4. Clean Up Report Files
Move all report files to the `release_reports/` directory:

| Move | To |
|------|---|
| comprehensive_test_results.txt | release_reports/ |
| docstring_coverage_report.txt | release_reports/ |
| mypy_detailed_report.txt | release_reports/ |
| mypy_report.txt | release_reports/ |
| mypy_strict_report.txt | release_reports/ |
| pylint_detailed_report.txt | release_reports/ |
| pylint_report.txt | release_reports/ |
| pylint_strict_report.txt | release_reports/ |
| test_results.txt | release_reports/ |

### 5. Consolidate Knowledge Base Directories
Consolidate to a single knowledge base directory:

| Action | Directory |
|--------|-----------|
| Keep | data/knowledge_base/ |
| Remove | knowledge_base/ (after verifying no unique data) |

### 6. Consolidate Resource Data
Consolidate to a single resource data directory:

| Action | Directory |
|--------|-----------|
| Keep | data/resources/ |
| Remove | resource_data/ (after verifying no unique data) |

### 7. Clean Up Shell Scripts
Review and consolidate shell scripts:

| Action | Script |
|--------|--------|
| Review | scripts/run_final_review.sh |
| Review | scripts/run_integration_tests.sh |
| Review | scripts/setup_environment.sh |

## Implementation Plan

1. First, verify that all tests pass with the current structure
2. Back up any files before removing them
3. Implement changes in the order listed above
4. Run tests after each major change to ensure functionality is preserved
5. Update documentation to reflect the new structure
