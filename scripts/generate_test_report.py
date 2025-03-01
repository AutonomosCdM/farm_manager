#!/usr/bin/env python3
import os
import xml.etree.ElementTree as ET
from datetime import datetime
import json


def parse_junit_xml(xml_path):
    """Parse JUnit XML test results"""
    tree = ET.parse(xml_path)
    root = tree.getroot()

    test_results = {
        "total": 0,
        "passed": 0,
        "failed": 0,
        "errors": 0,
        "skipped": 0,
        "failure_details": [],
    }

    for testsuite in root.findall("testsuite"):
        test_results["total"] += int(testsuite.get("tests", 0))
        test_results["passed"] += (
            int(testsuite.get("tests", 0))
            - int(testsuite.get("failures", 0))
            - int(testsuite.get("errors", 0))
        )
        test_results["failed"] += int(testsuite.get("failures", 0))
        test_results["errors"] += int(testsuite.get("errors", 0))
        test_results["skipped"] += int(testsuite.get("skipped", 0))

        # Collect failure details
        for testcase in testsuite.findall("testcase"):
            failure = testcase.find("failure")
            error = testcase.find("error")

            if failure is not None:
                test_results["failure_details"].append(
                    {
                        "test_name": testcase.get("name"),
                        "class_name": testcase.get("classname"),
                        "message": failure.get("message"),
                        "type": "failure",
                    }
                )

            if error is not None:
                test_results["failure_details"].append(
                    {
                        "test_name": testcase.get("name"),
                        "class_name": testcase.get("classname"),
                        "message": error.get("message"),
                        "type": "error",
                    }
                )

    return test_results


def generate_report(test_results):
    """Generate a comprehensive test report"""
    report_template_path = "tests/integration_test_report_template.md"

    with open(report_template_path, "r") as f:
        report_template = f.read()

    # Calculate success percentage
    total_tests = test_results["total"]
    passed_tests = test_results["passed"]
    success_percentage = (passed_tests / total_tests * 100) if total_tests > 0 else 0

    # Categorize problems
    critical_problems = [
        problem for problem in test_results["failure_details"] if problem["type"] == "error"
    ]
    non_critical_problems = [
        problem for problem in test_results["failure_details"] if problem["type"] == "failure"
    ]

    # Prepare report content
    report_content = report_template.format(
        fecha=datetime.now().strftime("%Y-%m-%d"),
        version="0.1.0",  # Get from setup.py or another source
        entorno="Desarrollo",
        total_pruebas=total_tests,
        pruebas_pasadas=passed_tests,
        pruebas_fallidas=test_results["failed"] + test_results["errors"],
        porcentaje_exito=round(success_percentage, 2),
        estado_flujo_trabajo=("Parcialmente Exitoso" if success_percentage < 100 else "Exitoso"),
        estado_recursos=("Verificado" if success_percentage > 90 else "Requiere Revisión"),
        estado_clima="Verificado" if success_percentage > 90 else "Requiere Revisión",
        estado_plantacion=("Verificado" if success_percentage > 90 else "Requiere Revisión"),
        estado_riego="Verificado" if success_percentage > 90 else "Requiere Revisión",
        estado_cosecha="Verificado" if success_percentage > 90 else "Requiere Revisión",
        estado_optimizacion=("Parcialmente Exitoso" if success_percentage < 100 else "Exitoso"),
        estado_maquinaria=("Verificado" if success_percentage > 90 else "Requiere Revisión"),
        estado_personal=("Verificado" if success_percentage > 90 else "Requiere Revisión"),
        estado_base_conocimientos=(
            "Parcialmente Exitoso" if success_percentage < 100 else "Exitoso"
        ),
        estado_info_cultivos=("Verificado" if success_percentage > 90 else "Requiere Revisión"),
        estado_recomendaciones_clima=(
            "Verificado" if success_percentage > 90 else "Requiere Revisión"
        ),
        lista_problemas="\n".join(
            [f"- {p['test_name']}: {p['message']}" for p in test_results["failure_details"]]
        ),
        lista_problemas_criticos="\n".join(
            [f"- {p['test_name']}: {p['message']}" for p in critical_problems]
        ),
        lista_problemas_no_criticos="\n".join(
            [f"- {p['test_name']}: {p['message']}" for p in non_critical_problems]
        ),
        recomendaciones=(
            "Revisar componentes con problemas y realizar pruebas adicionales"
            if success_percentage < 100
            else "Ninguna recomendación adicional"
        ),
        conclusion=(
            "Las pruebas de integración revelan áreas de mejora"
            if success_percentage < 100
            else "Pruebas de integración completadas con éxito"
        ),
        proximos_pasos=(
            "Corregir problemas identificados, realizar pruebas de regresión"
            if success_percentage < 100
            else "Preparar para siguiente fase de desarrollo"
        ),
    )

    # Write report
    report_path = "test_reports/integration_test_report.md"
    os.makedirs(os.path.dirname(report_path), exist_ok=True)

    with open(report_path, "w") as f:
        f.write(report_content)

    return report_path


def main():
    """Main function to run test report generation"""
    xml_path = "test_reports/integration_test_results.xml"

    if not os.path.exists(xml_path):
        print(f"Error: Test results XML not found at {xml_path}")
        exit(1)

    test_results = parse_junit_xml(xml_path)
    report_path = generate_report(test_results)

    print(f"Integration test report generated: {report_path}")

    # Exit with non-zero status if tests failed
    if test_results["failed"] > 0 or test_results["errors"] > 0:
        exit(1)


if __name__ == "__main__":
    main()
