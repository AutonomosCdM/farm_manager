#!/bin/bash

# Ensure virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Activating virtual environment..."
    source venv_farm_manager/bin/activate
fi

# Install required tools if not already installed
echo "Checking and installing required tools..."
pip install pylint black mypy radon sphinx interrogate pytest

# Run final review and release preparation script
echo "Running final review and release preparation..."
python scripts/final_review_and_release.py

# Check the result
if [ $? -eq 0 ]; then
    echo "✅ Project passed final review and is ready for release!"
    echo "Review report generated at release_reports/final_review_report.md"
else
    echo "❌ Project requires improvements before release."
    echo "Please check the detailed report at release_reports/final_review_report.md"
    exit 1
fi
