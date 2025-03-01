class FarmManagerBaseError(Exception):
    """Base exception for Farm Manager errors."""

    pass


class WeatherClientError(FarmManagerBaseError):
    """Exception raised for errors in weather client operations."""

    pass


class IrrigationDecisionError(FarmManagerBaseError):
    """Exception raised for errors in irrigation decision system."""

    pass


class ResourceManagementError(FarmManagerBaseError):
    """Exception raised for errors in resource management."""

    pass


class WorkflowTemplateError(FarmManagerBaseError):
    """Exception raised for errors in workflow template generation."""

    pass
