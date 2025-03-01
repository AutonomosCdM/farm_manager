import pytest
import os
import sys
from farm_manager.cli import main
from farm_manager.core.config import load_config
from farm_manager.resources.manager import ResourceManager
from farm_manager.irrigation.decision_system import IrrigationDecisionSystem
from farm_manager.weather.client import WeatherClient
from farm_manager.workflows.planting import generate_planting_workflow
from farm_manager.workflows.harvest import generate_harvest_workflow


class IntegrationTestSuite:
    """
    Comprehensive integration test suite for Farm Manager
    Covers end-to-end scenarios and interactions between different system components
    """

    @pytest.fixture
    def config(self):
        """Load configuration for testing"""
        return load_config()

    @pytest.fixture
    def resource_manager(self, config):
        """Initialize resource manager for testing"""
        return ResourceManager(config)

    @pytest.fixture
    def weather_client(self, config):
        """Initialize weather client for testing"""
        return WeatherClient(config)

    @pytest.fixture
    def irrigation_system(self, config, weather_client):
        """Initialize irrigation decision system"""
        return IrrigationDecisionSystem(config, weather_client)

    def test_complete_workflow_integration(
        self, resource_manager, irrigation_system, weather_client
    ):
        """
        Test a complete agricultural workflow integration
        Simulates a full cycle from resource planning to harvest
        """
        # 1. Resource Planning
        available_machinery = resource_manager.list_available_machinery()
        available_personnel = resource_manager.list_available_personnel()

        assert len(available_machinery) > 0, "No machinery available for workflow"
        assert len(available_personnel) > 0, "No personnel available for workflow"

        # 2. Weather Forecast
        forecast = weather_client.get_forecast(location="Santiago", days=7)
        assert forecast is not None, "Weather forecast retrieval failed"

        # 3. Planting Workflow
        planting_plan = generate_planting_workflow(
            crop_type="avellano",
            area=5.5,
            date="2025-07-15",
            machinery=available_machinery[0],
            personnel=available_personnel[0],
            weather_forecast=forecast,
        )
        assert planting_plan is not None, "Planting workflow generation failed"

        # 4. Irrigation Decision
        irrigation_recommendation = irrigation_system.recommend_irrigation(
            crop_type="avellano", area=5.5, weather_forecast=forecast
        )
        assert irrigation_recommendation is not None, "Irrigation recommendation failed"

        # 5. Harvest Workflow
        harvest_plan = generate_harvest_workflow(
            crop_type="avellano",
            area=5.5,
            date="2025-12-10",
            machinery=available_machinery[0],
            personnel=available_personnel[0],
        )
        assert harvest_plan is not None, "Harvest workflow generation failed"

    def test_resource_optimization(self, resource_manager):
        """
        Test resource optimization across different workflows
        """
        # Optimize machinery usage
        optimized_machinery = resource_manager.optimize_machinery_usage()
        assert len(optimized_machinery) > 0, "Machinery optimization failed"

        # Optimize personnel allocation
        optimized_personnel = resource_manager.optimize_personnel_allocation()
        assert len(optimized_personnel) > 0, "Personnel optimization failed"

    def test_knowledge_base_integration(self):
        """
        Test integration with knowledge base
        """
        from farm_manager.knowledge.base import KnowledgeBase

        kb = KnowledgeBase()
        crop_info = kb.get_crop_information("avellano")
        assert crop_info is not None, "Knowledge base crop information retrieval failed"

        climate_recommendations = kb.get_climate_recommendations("avellano")
        assert climate_recommendations is not None, "Climate recommendations retrieval failed"


def run_integration_tests():
    """
    Run the integration test suite and generate a report
    """
    import xmlrunner

    # Ensure test output directory exists
    os.makedirs("test_reports", exist_ok=True)

    # Run tests with XML output for detailed reporting
    pytest.main(
        [
            "tests/integration_test_suite.py",
            "-v",
            "--junitxml=test_reports/integration_test_results.xml",
        ]
    )


if __name__ == "__main__":
    run_integration_tests()
