#!/bin/bash

# Ensure virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Activating virtual environment..."
    source venv_farm_manager/bin/activate
fi

# Run integration tests
echo "Running Integration Tests for Farm Manager..."

# Ensure test reports directory exists
mkdir -p test_reports

# Run pytest with detailed reporting
python -m pytest tests/integration_test_suite.py -v --junitxml=test_reports/integration_test_results.xml

# Generate human-readable report
python scripts/generate_test_report.py

# Check test results
if [ $? -eq 0 ]; then
    echo "Integration Tests Passed Successfully!"
    exit 0
else
    echo "Integration Tests Failed. Please review the report."
    exit 1
fi
