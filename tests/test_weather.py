import pytest
from farm_manager.core.exceptions import WeatherClientError


def test_weather_forecast_generation(weather_client):
    """Test weather forecast generation."""
    location = "Santiago"
    days = 3

    forecast = weather_client.get_forecast(location, days)

    assert forecast is not None
    assert len(forecast) == days

    for day_forecast in forecast:
        assert "date" in day_forecast
        assert "temperature" in day_forecast
        assert "conditions" in day_forecast


def test_weather_forecast_default_days(weather_client):
    """Test weather forecast with default number of days."""
    location = "Santiago"

    forecast = weather_client.get_forecast(location)

    assert forecast is not None
    assert len(forecast) == 3  # Default 3 days


def test_weather_forecast_multiple_locations(weather_client):
    """Test weather forecast for multiple locations."""
    locations = ["Santiago", "Valparaíso", "Concepción"]

    for location in locations:
        forecast = weather_client.get_forecast(location)
        assert forecast is not None
        assert len(forecast) == 3


def test_weather_forecast_conditions_variety(weather_client):
    """Test variety of weather conditions."""
    location = "Santiago"
    days = 5

    forecast = weather_client.get_forecast(location, days)

    conditions = [day["conditions"] for day in forecast]
    assert len(set(conditions)) > 1, "Weather conditions should have some variety"
