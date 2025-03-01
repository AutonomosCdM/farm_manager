import pytest
from farm_manager.core.exceptions import IrrigationDecisionError


def test_irrigation_plan_generation(irrigation_system):
    """Test irrigation plan generation for a crop."""
    crop = "trigo"
    area = 10.0

    irrigation_plan = irrigation_system.generate_irrigation_plan(crop, area)

    assert irrigation_plan is not None
    assert irrigation_plan["crop"] == crop
    assert irrigation_plan["area"] == area
    assert "total_water_volume" in irrigation_plan
    assert "irrigation_frequency" in irrigation_plan
    assert "weather_conditions" in irrigation_plan
    assert "recommended_time" in irrigation_plan


def test_irrigation_plan_different_crops(irrigation_system):
    """Test irrigation plans for different crop types."""
    test_crops = [("avellano", 5.5), ("maíz", 8.0), ("trigo", 10.0)]

    for crop, area in test_crops:
        irrigation_plan = irrigation_system.generate_irrigation_plan(crop, area)
        assert irrigation_plan["crop"] == crop
        assert irrigation_plan["area"] == area


def test_irrigation_plan_zero_area(irrigation_system):
    """Test irrigation plan generation with zero area."""
    with pytest.raises(IrrigationDecisionError):
        irrigation_system.generate_irrigation_plan("trigo", 0)


def test_irrigation_plan_negative_area(irrigation_system):
    """Test irrigation plan generation with negative area."""
    with pytest.raises(IrrigationDecisionError):
        irrigation_system.generate_irrigation_plan("trigo", -5)


def test_irrigation_plan_unknown_crop(irrigation_system):
    """Test irrigation plan generation for an unknown crop type."""
    crop = "desconocido"
    area = 7.0

    irrigation_plan = irrigation_system.generate_irrigation_plan(crop, area)

    # Verify fallback behavior for unknown crop
    assert irrigation_plan["crop"] == crop
    assert irrigation_plan["irrigation_frequency"] == "cada 5 días"
