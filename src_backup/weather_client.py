import os
import requests
from typing import Dict, Any, Optional
from cachetools import TTLCache, cached
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChileanWeatherClient:
    """
    Client for retrieving meteorological data for Chilean regions.
    Supports multiple data sources with local caching and fallback mechanisms.
    """
    
    CHILEAN_REGIONS = [
        "Arica y Parinacota", "Tarapacá", "Antofagasta", "Atacama", 
        "Coquimbo", "Valparaíso", "Metropolitana", "O'Higgins", 
        "Maule", "Ñuble", "Biobío", "La Araucanía", 
        "Los Ríos", "Los Lagos", "Aysén", "Magallanes"
    ]
    
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # Cache with 5-minute TTL (Time To Live)
        self.cache = TTLCache(maxsize=100, ttl=300)
        
        # API key from environment variables
        self.agromonitoring_api_key = os.getenv('AGROMONITORING_API_KEY')
    
    def _validate_region(self, region: str) -> bool:
        """
        Validate if the provided region is a valid Chilean region.
        
        Args:
            region (str): Region name to validate
        
        Returns:
            bool: Whether the region is valid
        """
        return region in self.CHILEAN_REGIONS
    
    def _normalize_weather_data(self, raw_data: Dict[str, Any], source: str) -> Dict[str, Any]:
        """
        Normalize weather data from different sources to a consistent format.
        
        Args:
            raw_data (Dict): Raw weather data from API
            source (str): Source of the data (e.g., 'agromonitoring')
        
        Returns:
            Dict with normalized weather data
        """
        normalized_data = {
            "source": source,
            "temperature": None,
            "humidity": None,
            "wind_speed": None,
            "precipitation": None,
            "conditions": None
        }
        
        if source == 'agromonitoring':
            # Convert temperature from Kelvin to Celsius
            temp_kelvin = raw_data.get('main', {}).get('temp')
            temp_celsius = round(temp_kelvin - 273.15, 2) if temp_kelvin is not None else None
            
            normalized_data.update({
                "temperature": temp_celsius,
                "temperature_unit": "°C",
                "humidity": raw_data.get('main', {}).get('humidity'),
                "humidity_unit": "%",
                "wind_speed": raw_data.get('wind', {}).get('speed'),
                "wind_speed_unit": "m/s",
                "conditions": raw_data.get('weather', [{}])[0].get('description'),
                "timestamp": raw_data.get('dt')
            })
        
        return normalized_data
    
    def get_weather_by_region(self, region: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve current weather data for a specific Chilean region.
        
        Args:
            region (str): Name of the Chilean region
        
        Returns:
            Dict with normalized weather data or None if retrieval fails
        """
        if not self._validate_region(region):
            logger.error(f"Invalid region: {region}")
            return None
        
        # Check cache first
        cache_key = f"weather_{region}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        try:
            # Use AgroMonitoring API
            if self.agromonitoring_api_key:
                # Use region's main city or capital for coordinates
                city_coords = {
                    "Metropolitana": {"lat": -33.4489, "lon": -70.6693},  # Santiago
                    "Biobío": {"lat": -36.8261, "lon": -73.0498},  # Concepción
                    "Antofagasta": {"lat": -23.6509, "lon": -70.3975},  # Antofagasta
                    "Valparaíso": {"lat": -33.0472, "lon": -71.6127},  # Valparaíso
                    "Maule": {"lat": -35.4264, "lon": -71.6553},  # Talca
                    "La Araucanía": {"lat": -38.7359, "lon": -72.5904},  # Temuco
                    "Coquimbo": {"lat": -29.9533, "lon": -71.3436},  # La Serena
                    "Los Lagos": {"lat": -41.4693, "lon": -72.9424},  # Puerto Montt
                    "Tarapacá": {"lat": -20.2307, "lon": -70.1356},  # Iquique
                    "O'Higgins": {"lat": -34.1708, "lon": -70.7444},  # Rancagua
                    "Atacama": {"lat": -27.3668, "lon": -70.3321},  # Copiapó
                    "Ñuble": {"lat": -36.6062, "lon": -72.1025},  # Chillán
                    "Los Ríos": {"lat": -39.8142, "lon": -73.2459},  # Valdivia
                    "Arica y Parinacota": {"lat": -18.4746, "lon": -70.2979},  # Arica
                    "Aysén": {"lat": -45.5712, "lon": -72.0685},  # Coyhaique
                    "Magallanes": {"lat": -53.1638, "lon": -70.9171}  # Punta Arenas
                }
                
                if region in city_coords:
                    coords = city_coords[region]
                    url = f"https://api.agromonitoring.com/agro/1.0/weather?lat={coords['lat']}&lon={coords['lon']}&appid={self.agromonitoring_api_key}"
                    
                    response = requests.get(url)
                    response.raise_for_status()
                    
                    weather_data = self._normalize_weather_data(response.json(), 'agromonitoring')
                    self.cache[cache_key] = weather_data
                    return weather_data
            
            logger.warning(f"No weather data available for {region}")
            return None
        
        except requests.RequestException as e:
            logger.error(f"Weather API request failed: {e}")
            return None
    
    def get_weather_alerts(self, region: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve weather alerts for a specific Chilean region.
        
        Args:
            region (str): Name of the Chilean region
        
        Returns:
            Dict with weather alerts or None if no alerts
        """
        # Placeholder for future implementation
        # Will integrate with official sources like ONEMI or DMC
        return None

# Example usage and testing
if __name__ == "__main__":
    client = ChileanWeatherClient()
    santiago_weather = client.get_weather_by_region("Metropolitana")
    print(santiago_weather)
