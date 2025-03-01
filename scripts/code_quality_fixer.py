#!/usr/bin/env python3
import os
import subprocess
import sys


class CodeQualityFixer:
    """
    Automated code quality improvement script
    """

    @staticmethod
    def fix_code_formatting():
        """
        Apply black formatting to all Python files
        """
        print("Applying Black code formatting...")
        try:
            subprocess.run(["black", "farm_manager", "tests", "scripts"], check=True)
            print("✅ Code formatting completed successfully")
        except subprocess.CalledProcessError:
            print("❌ Code formatting failed")
            return False
        return True

    @staticmethod
    def run_pylint_and_fix():
        """
        Run pylint and generate a report with suggestions
        """
        print("Running Pylint and generating improvement suggestions...")
        try:
            # Generate detailed pylint report
            with open("pylint_report.txt", "w") as report_file:
                result = subprocess.run(
                    ["pylint", "farm_manager", "tests", "scripts"],
                    capture_output=True,
                    text=True,
                )
                report_file.write(result.stdout)

            print("Pylint report generated at pylint_report.txt")
            return True
        except Exception as e:
            print(f"❌ Pylint analysis failed: {e}")
            return False

    @staticmethod
    def improve_type_hints():
        """
        Run mypy and suggest type hint improvements
        """
        print("Checking type hints with MyPy...")
        try:
            with open("mypy_report.txt", "w") as report_file:
                result = subprocess.run(
                    ["mypy", "farm_manager", "tests", "scripts"],
                    capture_output=True,
                    text=True,
                )
                report_file.write(result.stdout)

            print("MyPy report generated at mypy_report.txt")
            return True
        except Exception as e:
            print(f"❌ Type checking failed: {e}")
            return False

    @staticmethod
    def improve_docstring_coverage():
        """
        Check and improve docstring coverage
        """
        print("Checking docstring coverage...")
        try:
            result = subprocess.run(
                ["interrogate", "-v", "-f", "farm_manager"],
                capture_output=True,
                text=True,
            )

            # Write detailed report
            with open("docstring_coverage_report.txt", "w") as report_file:
                report_file.write(result.stdout)

            print("Docstring coverage report generated at docstring_coverage_report.txt")
            return True
        except Exception as e:
            print(f"❌ Docstring coverage check failed: {e}")
            return False

    @staticmethod
    def update_gitignore():
        """
        Update .gitignore with comprehensive Python ignores
        """
        python_ignores = [
            "# Python",
            "*.py[cod]",
            "__pycache__/",
            "*.so",
            ".Python",
            "build/",
            "develop-eggs/",
            "dist/",
            "downloads/",
            "eggs/",
            ".eggs/",
            "lib/",
            "lib64/",
            "parts/",
            "sdist/",
            "var/",
            "wheels/",
            "*.egg-info/",
            ".installed.cfg",
            "*.egg",
            "MANIFEST",
            "# Virtual Environment",
            "venv/",
            "venv_*",
            ".env",
            ".venv",
            "ENV/",
            "# Testing",
            ".pytest_cache/",
            ".coverage",
            "htmlcov/",
            "# IDE",
            ".idea/",
            ".vscode/",
            "*.swp",
            "*.swo",
            "# Logs",
            "*.log",
            "# OS generated files",
            ".DS_Store",
            ".DS_Store?",
            "._*",
            ".Spotlight-V100",
            ".Trashes",
            "ehthumbs.db",
            "Thumbs.db",
        ]

        try:
            # Read existing .gitignore if it exists
            existing_ignores = set()
            if os.path.exists(".gitignore"):
                with open(".gitignore", "r") as f:
                    existing_ignores = set(f.read().splitlines())

            # Add new ignores
            new_ignores = set(python_ignores) - existing_ignores

            # Write updated .gitignore
            with open(".gitignore", "a") as f:
                f.write("\n" + "\n".join(new_ignores) + "\n")

            print("✅ .gitignore updated successfully")
            return True
        except Exception as e:
            print(f"❌ .gitignore update failed: {e}")
            return False

    @classmethod
    def run_all_fixes(cls):
        """
        Run all code quality improvement methods
        """
        fixes = [
            cls.fix_code_formatting,
            cls.run_pylint_and_fix,
            cls.improve_type_hints,
            cls.improve_docstring_coverage,
            cls.update_gitignore,
        ]

        results = [fix() for fix in fixes]
        return all(results)


def main():
    """
    Main function to run code quality fixes
    """
    success = CodeQualityFixer.run_all_fixes()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
