from dataclasses import dataclass, field
from typing import Dict, Any, Optional
from datetime import datetime


@dataclass
class WeatherData:
    """
    Standardized weather data model for Chilean regions.
    """

    region: str
    temperature: Optional[float] = None
    temperature_unit: str = "°C"
    humidity: Optional[float] = None
    humidity_unit: str = "%"
    wind_speed: Optional[float] = None
    wind_speed_unit: str = "m/s"
    conditions: Optional[str] = None
    timestamp: Optional[datetime] = None
    source: str = "agromonitoring"

    @classmethod
    def from_agromonitoring(cls, raw_data: Dict[str, Any], region: str) -> "WeatherData":
        """
        Create WeatherData from AgroMonitoring API response.

        :param raw_data: Raw JSON response from AgroMonitoring
        :param region: Chilean region name
        :return: WeatherData instance
        """
        # Convert temperature from Kelvin to Celsius
        temp_kelvin = raw_data.get("main", {}).get("temp")
        temp_celsius = round(temp_kelvin - 273.15, 2) if temp_kelvin is not None else None

        return cls(
            region=region,
            temperature=temp_celsius,
            humidity=raw_data.get("main", {}).get("humidity"),
            wind_speed=raw_data.get("wind", {}).get("speed"),
            conditions=raw_data.get("weather", [{}])[0].get("description"),
            timestamp=(
                datetime.fromtimestamp(raw_data.get("dt", 0)) if raw_data.get("dt") else None
            ),
            source="agromonitoring",
        )


@dataclass
class WeatherAlert:
    """
    Weather alert model for tracking and managing meteorological warnings.
    """

    region: str
    alert_type: str
    severity: str = "moderate"
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    affected_areas: Optional[list] = field(default_factory=list)

    @classmethod
    def create_alert(
        cls,
        region: str,
        alert_type: str,
        severity: str = "moderate",
        description: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        affected_areas: Optional[list] = None,
    ) -> "WeatherAlert":
        """
        Factory method to create a weather alert.

        :param region: Region where the alert is issued
        :param alert_type: Type of weather alert (e.g., 'frost', 'heatwave', 'storm')
        :param severity: Alert severity level
        :param description: Detailed description of the alert
        :param start_time: When the alert begins
        :param end_time: When the alert is expected to end
        :param affected_areas: List of specific areas affected
        :return: WeatherAlert instance
        """
        return cls(
            region=region,
            alert_type=alert_type,
            severity=severity,
            description=description or f"{severity.capitalize()} {alert_type} alert in {region}",
            start_time=start_time or datetime.now(),
            end_time=end_time,
            affected_areas=affected_areas or [],
        )
