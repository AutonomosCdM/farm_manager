"""
Core exceptions and utilities for Farm Manager.
"""

from .exceptions import (
    FarmManagerBaseError,
    WeatherClientError,
    IrrigationDecisionError,
    ResourceManagementError,
    WorkflowTemplateError,
)

__all__ = [
    "FarmManagerBaseError",
    "WeatherClientError",
    "IrrigationDecisionError",
    "ResourceManagementError",
    "WorkflowTemplateError",
]
