#!/usr/bin/env python3
import json
import os
from typing import Dict, List


class IntegrationTestSuccessValidator:
    """
    Validates the success criteria for integration tests
    """

    @staticmethod
    def validate_test_results(test_results_path: str) -> Dict[str, bool]:
        """
        Validate test results against success criteria

        :param test_results_path: Path to the test results JSON
        :return: Dictionary of success criteria validation
        """
        with open(test_results_path, "r") as f:
            test_results = json.load(f)

        success_criteria = {
            "all_tests_passing": test_results["failed"] == 0 and test_results["errors"] == 0,
            "system_coherence": test_results["success_percentage"] >= 95,
            "problems_identified_and_tracked": len(test_results["failure_details"]) > 0,
            "real_use_cases_validated": all(
                [
                    test_results["success_percentage"] >= 90,
                    test_results["total_tests"] > 10,  # Ensure comprehensive testing
                ]
            ),
        }

        return success_criteria

    @staticmethod
    def generate_validation_report(success_criteria: Dict[str, bool]) -> str:
        """
        Generate a human-readable validation report

        :param success_criteria: Dictionary of success criteria validation
        :return: Markdown formatted report
        """
        report = "# Validación de Criterios de Éxito\n\n"

        for criterion, passed in success_criteria.items():
            status = "✅ Pasado" if passed else "❌ No Pasado"
            report += f"## {criterion.replace('_', ' ').title()}\n"
            report += f"**Estado**: {status}\n\n"

        overall_success = all(success_criteria.values())
        report += f"## Resultado General\n"
        report += f"**Estado Final**: {'✅ Éxito' if overall_success else '❌ Requiere Revisión'}\n"

        return report

    @classmethod
    def validate_and_report(cls, test_results_path: str) -> bool:
        """
        Validate success criteria and generate a report

        :param test_results_path: Path to the test results JSON
        :return: Boolean indicating overall success
        """
        success_criteria = cls.validate_test_results(test_results_path)
        report = cls.generate_validation_report(success_criteria)

        # Ensure reports directory exists
        os.makedirs("test_reports", exist_ok=True)

        # Write validation report
        with open("test_reports/success_criteria_validation.md", "w") as f:
            f.write(report)

        return all(success_criteria.values())


def main():
    """
    Main function to run success criteria validation
    """
    test_results_path = "test_reports/test_results.json"

    if not os.path.exists(test_results_path):
        print(f"Error: Test results not found at {test_results_path}")
        exit(1)

    validation_passed = IntegrationTestSuccessValidator.validate_and_report(test_results_path)

    # Exit with appropriate status
    exit(0 if validation_passed else 1)


if __name__ == "__main__":
    main()
