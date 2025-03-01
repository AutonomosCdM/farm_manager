from typing import List, Optional, Dict
from datetime import datetime, timedelta
import logging

from .models import WeatherAlert, WeatherData
from ..core.config import FarmManagerConfig
from ..core.exceptions import WeatherAlertError


class WeatherAlertSystem:
    """
    System for managing and generating weather alerts.
    """

    def __init__(self, config: Optional[FarmManagerConfig] = None):
        """
        Initialize the Weather Alert System.

        :param config: Optional configuration object
        """
        self.config = config or FarmManagerConfig.get_config()
        self.logger = logging.getLogger(__name__)

        # Active alerts storage
        self.active_alerts: Dict[str, List[WeatherAlert]] = {}

    def generate_alert(self, region: str, weather_data: WeatherData) -> Optional[WeatherAlert]:
        """
        Generate weather alerts based on current weather conditions.

        :param region: Region to check for alerts
        :param weather_data: Current weather data
        :return: Generated WeatherAlert or None
        """
        try:
            # Temperature-based alerts
            if weather_data.temperature is not None:
                if weather_data.temperature > 35:  # Extreme heat
                    return WeatherAlert.create_alert(
                        region=region,
                        alert_type="heatwave",
                        severity="high",
                        description=f"Extreme heat warning: Temperature {weather_data.temperature}°C",
                        end_time=datetime.now() + timedelta(days=2),
                    )
                elif weather_data.temperature < 0:  # Frost
                    return WeatherAlert.create_alert(
                        region=region,
                        alert_type="frost",
                        severity="high",
                        description=f"Frost warning: Temperature {weather_data.temperature}°C",
                        end_time=datetime.now() + timedelta(days=1),
                    )

            # Humidity and wind-based alerts
            if weather_data.humidity is not None and weather_data.wind_speed is not None:
                if weather_data.humidity < 20 and weather_data.wind_speed > 10:  # Dry and windy
                    return WeatherAlert.create_alert(
                        region=region,
                        alert_type="fire_risk",
                        severity="moderate",
                        description=f"Fire risk: Low humidity {weather_data.humidity}% and high winds {weather_data.wind_speed} m/s",
                        end_time=datetime.now() + timedelta(days=1),
                    )

            return None

        except Exception as e:
            self.logger.error(f"Error generating weather alert: {e}")
            return None

    def add_alert(self, alert: WeatherAlert) -> None:
        """
        Add an alert to the active alerts for a region.

        :param alert: WeatherAlert to add
        """
        if alert.region not in self.active_alerts:
            self.active_alerts[alert.region] = []

        self.active_alerts[alert.region].append(alert)
        self.logger.info(f"New alert added for {alert.region}: {alert.description}")

    def get_active_alerts(self, region: Optional[str] = None) -> List[WeatherAlert]:
        """
        Retrieve active weather alerts.

        :param region: Optional region to filter alerts
        :return: List of active weather alerts
        """
        # Remove expired alerts
        self._cleanup_expired_alerts()

        if region:
            return self.active_alerts.get(region, [])

        # Flatten and return all active alerts
        return [alert for region_alerts in self.active_alerts.values() for alert in region_alerts]

    def _cleanup_expired_alerts(self) -> None:
        """
        Remove expired alerts from the active alerts list.
        """
        now = datetime.now()
        for region in list(self.active_alerts.keys()):
            # Remove alerts that have ended
            self.active_alerts[region] = [
                alert
                for alert in self.active_alerts[region]
                if alert.end_time is None or alert.end_time > now
            ]

            # Remove empty region lists
            if not self.active_alerts[region]:
                del self.active_alerts[region]
