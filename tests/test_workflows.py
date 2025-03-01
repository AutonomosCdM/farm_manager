import pytest
from farm_manager.core.exceptions import WorkflowTemplateError


def test_workflow_planting(workflow_manager, sample_planting_context):
    """Test planting workflow generation."""
    plan = workflow_manager.generate_workflow("planting", sample_planting_context)

    assert plan is not None
    assert plan["operation"] == "Planting"
    assert plan["crop"] == "avellano"
    assert plan["area"] == 5.5
    assert "planting_steps" in plan
    assert "equipment_needed" in plan


def test_workflow_harvest(workflow_manager, sample_harvest_context):
    """Test harvest workflow generation."""
    plan = workflow_manager.generate_workflow("harvest", sample_harvest_context)

    assert plan is not None
    assert plan["operation"] == "Harvest"
    assert plan["crop"] == "trigo"
    assert plan["area"] == 10.0
    assert "harvest_steps" in plan
    assert "equipment_needed" in plan


def test_workflow_maintenance(workflow_manager, sample_maintenance_context):
    """Test maintenance workflow generation."""
    plan = workflow_manager.generate_workflow("maintenance", sample_maintenance_context)

    assert plan is not None
    assert plan["operation"] == "Maintenance"
    assert plan["crop"] == "maíz"
    assert plan["area"] == 8.0
    assert "maintenance_steps" in plan
    assert "equipment_needed" in plan


def test_workflow_invalid_operation(workflow_manager):
    """Test handling of invalid workflow operation."""
    with pytest.raises(ValueError, match="No template found for operation type"):
        workflow_manager.generate_workflow("invalid_operation", {})


def test_workflow_missing_context(workflow_manager):
    """Test handling of missing context keys."""
    with pytest.raises(ValueError, match="Missing required context key"):
        workflow_manager.generate_workflow("planting", {})
