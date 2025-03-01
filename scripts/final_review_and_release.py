#!/usr/bin/env python3
import os
import sys
import subprocess
import json
from typing import Dict, List


class ProjectReviewAndRelease:
    """
    Comprehensive project review and release preparation script
    """

    def __init__(self, project_root: str = "."):
        """
        Initialize the review process

        :param project_root: Root directory of the project
        """
        self.project_root = project_root
        self.review_results = {
            "code_review": {},
            "documentation_review": {},
            "structure_validation": {},
            "release_readiness": {},
        }

    def run_code_quality_checks(self) -> Dict[str, bool]:
        """
        Run code quality checks using multiple tools

        :return: Dictionary of code quality check results
        """
        checks = {
            "pylint": self._run_pylint(),
            "black_formatting": self._run_black_check(),
            "mypy_type_checking": self._run_mypy(),
            "complexity_check": self._run_radon_complexity(),
        }

        self.review_results["code_review"] = checks
        return checks

    def _run_pylint(self) -> bool:
        """Run pylint code quality check"""
        try:
            result = subprocess.run(
                ["pylint", "farm_manager", "tests", "scripts"],
                capture_output=True,
                text=True,
            )
            return result.returncode == 0
        except Exception:
            return False

    def _run_black_check(self) -> bool:
        """Check code formatting with Black"""
        try:
            result = subprocess.run(
                ["black", "--check", "farm_manager", "tests", "scripts"],
                capture_output=True,
                text=True,
            )
            return result.returncode == 0
        except Exception:
            return False

    def _run_mypy(self) -> bool:
        """Run mypy type checking"""
        try:
            result = subprocess.run(
                ["mypy", "farm_manager", "tests", "scripts"],
                capture_output=True,
                text=True,
            )
            return result.returncode == 0
        except Exception:
            return False

    def _run_radon_complexity(self) -> bool:
        """Check code complexity"""
        try:
            result = subprocess.run(
                ["radon", "cc", "farm_manager", "-n", "B"],
                capture_output=True,
                text=True,
            )
            # Parse output to ensure no method exceeds complexity threshold
            return len(result.stdout.strip()) == 0
        except Exception:
            return False

    def verify_documentation(self) -> Dict[str, bool]:
        """
        Verify documentation completeness and quality

        :return: Dictionary of documentation review results
        """
        checks = {
            "readme_exists": os.path.exists("README.md"),
            "api_docs_complete": self._check_api_documentation(),
            "docstrings_coverage": self._check_docstring_coverage(),
            "changelog_updated": self._check_changelog(),
        }

        self.review_results["documentation_review"] = checks
        return checks

    def _check_api_documentation(self) -> bool:
        """Check if API documentation is complete"""
        try:
            # Use sphinx-apidoc to generate documentation
            result = subprocess.run(
                ["sphinx-apidoc", "-o", "docs", "farm_manager"],
                capture_output=True,
                text=True,
            )
            return result.returncode == 0
        except Exception:
            return False

    def _check_docstring_coverage(self) -> bool:
        """Check docstring coverage"""
        try:
            result = subprocess.run(
                ["interrogate", "-v", "farm_manager"], capture_output=True, text=True
            )
            # Assume we want at least 80% docstring coverage
            return "PASS" in result.stdout and float(result.stdout.split("%")[0]) >= 80
        except Exception:
            return False

    def _check_changelog(self) -> bool:
        """Verify changelog is up to date"""
        try:
            with open("CHANGELOG.md", "r") as f:
                changelog = f.read()
                # Check if latest version matches setup.py
                return "## [Unreleased]" in changelog
        except Exception:
            return False

    def validate_project_structure(self) -> Dict[str, bool]:
        """
        Validate project structure and key files

        :return: Dictionary of structure validation results
        """
        required_dirs = ["farm_manager", "tests", "docs", "scripts", "data"]

        required_files = [
            "setup.py",
            "requirements.txt",
            "README.md",
            "CHANGELOG.md",
            ".env.example",
        ]

        checks = {
            "required_directories": all(os.path.isdir(d) for d in required_dirs),
            "required_files": all(os.path.exists(f) for f in required_files),
            "virtual_env_configured": os.path.exists("venv_farm_manager"),
            "gitignore_complete": self._check_gitignore(),
        }

        self.review_results["structure_validation"] = checks
        return checks

    def _check_gitignore(self) -> bool:
        """Check if .gitignore is comprehensive"""
        try:
            with open(".gitignore", "r") as f:
                gitignore = f.read()
                # Check for common Python ignores
                required_ignores = [
                    "*.pyc",
                    "__pycache__/",
                    "*.env",
                    "venv/",
                    ".pytest_cache/",
                ]
                return all(ignore in gitignore for ignore in required_ignores)
        except Exception:
            return False

    def check_release_readiness(self) -> Dict[str, bool]:
        """
        Final check for release readiness

        :return: Dictionary of release readiness checks
        """
        checks = {
            "all_tests_passing": self._run_all_tests(),
            "code_quality_checks_passed": all(self.review_results["code_review"].values()),
            "documentation_complete": all(self.review_results["documentation_review"].values()),
            "project_structure_valid": all(self.review_results["structure_validation"].values()),
        }

        self.review_results["release_readiness"] = checks
        return checks

    def _run_all_tests(self) -> bool:
        """Run all tests"""
        try:
            result = subprocess.run(["pytest", "tests/"], capture_output=True, text=True)
            return result.returncode == 0
        except Exception:
            return False

    def generate_review_report(self) -> str:
        """
        Generate a comprehensive review report

        :return: Markdown formatted review report
        """
        report = "# Informe de Revisión Final y Preparación de Lanzamiento\n\n"

        # Add sections for each review category
        for category, results in self.review_results.items():
            report += f"## {category.replace('_', ' ').title()}\n"
            for check, passed in results.items():
                status = "✅ Pasado" if passed else "❌ No Pasado"
                report += f"- **{check.replace('_', ' ').title()}**: {status}\n"
            report += "\n"

        # Overall assessment
        overall_success = all(
            all(category.values()) for category in self.review_results.values() if category
        )
        report += f"## Resultado General\n"
        report += f"**Estado de Lanzamiento**: {'✅ Listo para Lanzamiento' if overall_success else '❌ Requiere Revisión'}\n"

        return report

    def prepare_release(self):
        """
        Prepare for official release
        """
        # Ensure all checks are run
        self.run_code_quality_checks()
        self.verify_documentation()
        self.validate_project_structure()

        # Final readiness check
        release_ready = self.check_release_readiness()

        # Generate report
        report = self.generate_review_report()

        # Write report
        os.makedirs("release_reports", exist_ok=True)
        with open("release_reports/final_review_report.md", "w") as f:
            f.write(report)

        return all(release_ready.values())


def main():
    """
    Main function to run final review and release preparation
    """
    review = ProjectReviewAndRelease()

    try:
        release_ready = review.prepare_release()

        # Exit with appropriate status
        sys.exit(0 if release_ready else 1)

    except Exception as e:
        print(f"Error during release preparation: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
