# Enhanced Project Cleanup Plan

## Current Issues

Looking at the root directory, there are still many files that could be better organized:

1. Multiple report files (mypy_*.txt, pylint_*.txt, etc.)
2. Test files in the root directory
3. Multiple configuration files
4. Documentation files scattered around
5. Virtual environment directories (venv_*)

## Enhanced Organization Plan

### 1. Create a More Structured Directory Layout

```
farm_manager/           # Main package
config/                 # Configuration files
├── linting/            # Linting configuration
└── mypy/               # Type checking configuration
data/                   # All data files
docs/                   # All documentation
reports/                # All report files
├── code_quality/       # Code quality reports
├── test_results/       # Test result reports
└── release/            # Release reports
tests/                  # All test files
scripts/                # Utility scripts
```

### 2. Move Files to Appropriate Directories

#### Configuration Files
- Move to `config/`:
  - `.pylintrc` → `config/linting/pylintrc`
  - `mypy.ini` → `config/mypy/mypy.ini`
  - `setup.cfg` → `config/setup.cfg`

#### Report Files
- Move to `reports/code_quality/`:
  - `pylint_report.txt`
  - `pylint_detailed_report.txt`
  - `pylint_strict_report.txt`
  - `mypy_report.txt`
  - `mypy_detailed_report.txt`
  - `mypy_strict_report.txt`
  - `docstring_coverage_report.txt`

- Move to `reports/test_results/`:
  - `test_results.txt`
  - `comprehensive_test_results.txt`

#### Documentation Files
- Move to `docs/`:
  - `NOTES.md`
  - `plan_agricola.md`
  - `plan_reestructuracion.md`
  - `cleanup_plan.md`
  - `PROJECT_CLEANUP_README.md` → `docs/project_cleanup.md`

#### Test Files
- Move to `tests/`:
  - `test_irrigation_decision_system.py`
  - `test_irrigation_mock.py`
  - `test_irrigation_simplified.py`
  - `test_machinery_optimization.py`
  - `test_weather_client.py`

### 3. Clean Up Virtual Environment Directories

- Consider removing or consolidating virtual environment directories:
  - `venv_farm_manager/`
  - `venv_stable/`

### 4. Consolidate or Remove Redundant Directories

- Remove `src/` directory (after verifying code is in `farm_manager/`)
- Consolidate `knowledge_base/` into `data/knowledge_base/`
- Consolidate `resource_data/` into `data/resources/`
- Consider if `test_resource_data/` can be moved into `tests/`

### 5. Keep Essential Files in Root

Only keep essential files in the root directory:
- `.env.example`
- `.envrc`
- `.gitignore`
- `CHANGELOG.md`
- `README.md`
- `requirements.txt`
- `setup.py`

## Implementation Approach

1. Create all necessary directories
2. Move files to their appropriate locations
3. Update imports and references in code
4. Update documentation to reflect new structure
5. Run tests to ensure everything still works
