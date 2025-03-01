import pytest
from farm_manager.core.exceptions import ResourceManagementError


def test_resource_list_all(resource_manager):
    """Test listing all resources."""
    resources = resource_manager.list_resources()

    assert resources is not None
    assert len(resources) > 0

    # Check that each resource has required keys
    for resource in resources:
        assert "type" in resource
        assert "name" in resource
        assert "quantity" in resource


def test_resource_list_by_type(resource_manager):
    """Test listing resources by specific type."""
    resource_types = ["machinery", "personnel"]

    for resource_type in resource_types:
        resources = resource_manager.list_resources(resource_type)

        assert resources is not None
        assert all(r["type"] == resource_type for r in resources)


def test_resource_optimization_all(resource_manager):
    """Test resource optimization for all resources."""
    optimization_result = resource_manager.optimize_resources()

    assert optimization_result is not None
    assert "total_resources" in optimization_result
    assert "optimization_potential" in optimization_result
    assert "recommendations" in optimization_result
    assert len(optimization_result["recommendations"]) > 0


def test_resource_optimization_by_type(resource_manager):
    """Test resource optimization for specific resource types."""
    resource_types = ["machinery", "personnel"]

    for resource_type in resource_types:
        optimization_result = resource_manager.optimize_resources(resource_type)

        assert optimization_result is not None
        assert "total_resources" in optimization_result
        assert "optimization_potential" in optimization_result
        assert "recommendations" in optimization_result


def test_resource_list_unknown_type(resource_manager):
    """Test listing resources with an unknown type."""
    unknown_type = "unknown_resource_type"
    resources = resource_manager.list_resources(unknown_type)

    assert resources == [], "Unknown resource type should return an empty list"
