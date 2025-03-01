#!/usr/bin/env python3
import os
import sys
import time
import logging
import psutil
import tracemalloc
from memory_profiler import memory_usage

# Add project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from farm_manager.core.logging_config import setup_logging
from farm_manager.resources.manager import ResourceManager
from farm_manager.irrigation.decision_system import IrrigationDecisionSystem
from farm_manager.weather.client import WeatherClient


class PerformanceTest:
    def __init__(self):
        # Setup logging
        self.loggers = setup_logging(logging.DEBUG)
        self.logger = self.loggers["main_logger"]
        self.performance_logger = self.loggers["performance_logger"]

    def measure_resource_allocation(self, iterations=100):
        """
        Measure performance of resource allocation operations.

        Args:
            iterations (int): Number of iterations to test
        """
        resource_manager = ResourceManager()

        # Start memory and CPU tracking
        tracemalloc.start()
        process = psutil.Process()

        start_time = time.time()
        start_memory = process.memory_info().rss

        try:
            for _ in range(iterations):
                # Simulate resource allocation
                resource_manager.allocate_resources(resource_type="machinery", quantity=5)

            end_time = time.time()
            end_memory = process.memory_info().rss

            # Performance metrics
            total_time = end_time - start_time
            memory_used = end_memory - start_memory

            self.performance_logger.info(
                f"Resource Allocation Performance:\n"
                f"Iterations: {iterations}\n"
                f"Total Time: {total_time:.4f} seconds\n"
                f"Average Time per Iteration: {total_time/iterations:.6f} seconds\n"
                f"Memory Used: {memory_used / (1024 * 1024):.2f} MB"
            )
        except Exception as e:
            self.logger.error(f"Performance test failed: {e}")
        finally:
            tracemalloc.stop()

    def measure_irrigation_decision(self, iterations=50):
        """
        Measure performance of irrigation decision system.

        Args:
            iterations (int): Number of iterations to test
        """
        irrigation_system = IrrigationDecisionSystem()
        weather_client = WeatherClient()

        tracemalloc.start()
        process = psutil.Process()

        start_time = time.time()
        start_memory = process.memory_info().rss

        try:
            for _ in range(iterations):
                # Simulate irrigation decision process
                weather_data = weather_client.get_forecast("Central Valley")
                irrigation_decision = irrigation_system.calculate_irrigation_needs(
                    crop_type="wheat", weather_data=weather_data
                )

            end_time = time.time()
            end_memory = process.memory_info().rss

            # Performance metrics
            total_time = end_time - start_time
            memory_used = end_memory - start_memory

            self.performance_logger.info(
                f"Irrigation Decision Performance:\n"
                f"Iterations: {iterations}\n"
                f"Total Time: {total_time:.4f} seconds\n"
                f"Average Time per Iteration: {total_time/iterations:.6f} seconds\n"
                f"Memory Used: {memory_used / (1024 * 1024):.2f} MB"
            )
        except Exception as e:
            self.logger.error(f"Performance test failed: {e}")
        finally:
            tracemalloc.stop()

    def run_comprehensive_test(self):
        """
        Run a comprehensive performance test suite.
        """
        self.logger.info("Starting Comprehensive Performance Test")

        try:
            self.measure_resource_allocation()
            self.measure_irrigation_decision()
        except Exception as e:
            self.logger.error(f"Comprehensive performance test failed: {e}")

        self.logger.info("Comprehensive Performance Test Complete")


def main():
    performance_test = PerformanceTest()
    performance_test.run_comprehensive_test()


if __name__ == "__main__":
    main()
