import pytest
from src.workflow_templates import WorkflowTemplateManager

def test_planting_workflow():
    manager = WorkflowTemplateManager()
    
    avellano_context = {
        'crop_type': 'avellano',
        'area_hectares': 5.5,
        'soil_type': 'franco',
        'planting_date': '2025-07-15'
    }
    
    plan = manager.generate_workflow('planting', avellano_context)
    
    assert plan is not None, "Planting workflow plan should not be None"
    assert plan['operation'] == 'Planting', "Operation should be Planting"
    assert plan['crop'] == 'avellano', "Crop type should match input"
    assert plan['area'] == 5.5, "Area should match input"
    assert len(plan['planting_steps']) > 0, "Planting steps should be generated"
    assert len(plan['equipment_needed']) > 0, "Equipment should be recommended"

def test_harvest_workflow():
    manager = WorkflowTemplateManager()
    
    harvest_context = {
        'crop_type': 'trigo',
        'area_hectares': 10.0,
        'expected_yield': 3.5,
        'harvest_date': '2025-12-10'
    }
    
    plan = manager.generate_workflow('harvest', harvest_context)
    
    assert plan is not None, "Harvest workflow plan should not be None"
    assert plan['operation'] == 'Harvest', "Operation should be Harvest"
    assert plan['crop'] == 'trigo', "Crop type should match input"
    assert plan['area'] == 10.0, "Area should match input"
    assert plan['expected_total_yield'] == 3.5 * 10.0, "Total yield should be calculated correctly"
    assert len(plan['harvest_steps']) > 0, "Harvest steps should be generated"
    assert len(plan['equipment_needed']) > 0, "Equipment should be recommended"

def test_maintenance_workflow():
    manager = WorkflowTemplateManager()
    
    maintenance_context = {
        'crop_type': 'maíz',
        'area_hectares': 8.0,
        'maintenance_type': 'pest_control',
        'maintenance_date': '2025-09-20'
    }
    
    plan = manager.generate_workflow('maintenance', maintenance_context)
    
    assert plan is not None, "Maintenance workflow plan should not be None"
    assert plan['operation'] == 'Maintenance', "Operation should be Maintenance"
    assert plan['crop'] == 'maíz', "Crop type should match input"
    assert plan['area'] == 8.0, "Area should match input"
    assert plan['maintenance_type'] == 'pest_control', "Maintenance type should match input"
    assert len(plan['maintenance_steps']) > 0, "Maintenance steps should be generated"
    assert len(plan['equipment_needed']) > 0, "Equipment should be recommended"

def test_invalid_workflow_type():
    manager = WorkflowTemplateManager()
    
    with pytest.raises(ValueError, match="No template found for operation type"):
        manager.generate_workflow('invalid_type', {})

def test_missing_context_keys():
    manager = WorkflowTemplateManager()
    
    # Test planting workflow with missing keys
    with pytest.raises(ValueError, match="Missing required context key"):
        manager.generate_workflow('planting', {})
    
    # Test harvest workflow with missing keys
    with pytest.raises(ValueError, match="Missing required context key"):
        manager.generate_workflow('harvest', {})
    
    # Test maintenance workflow with missing keys
    with pytest.raises(ValueError, match="Missing required context key"):
        manager.generate_workflow('maintenance', {})
