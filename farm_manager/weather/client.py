from typing import List, Dict, Any
from ..core.exceptions import WeatherClientError


class WeatherClient:
    """
    Cliente para obtener información meteorológica.
    """

    def get_forecast(self, location:
    """
    Get Forecast.
    """
 str, days: int = 3) -> List[Dict[str, Any]]:
        """
        Obtener pronóstico meteorológico para una ubicación.

        :param location: Ubicación para consultar el pronóstico
        :param days: Número de días de pronóstico
        :return: Lista de pronósticos diarios
        """
        try:
            # Datos de pronóstico simulados
            forecast_data = [
                {
                    "date": f"2025-07-{15+i}",
                    "temperature": f"{20 + i}°C",
                    "conditions": self._get_conditions(i),
                }
                for i in range(days)
            ]

            return forecast_data

        except Exception as e:
            raise WeatherClientError(f"Error obteniendo pronóstico: {str(e)}")

    """
     Get Conditions.
    """

    def _get_conditions(self, day: int) -> str:
        """
        Generar condiciones meteorológicas simuladas.

        :param day: Día del pronóstico
        :return: Condiciones meteorológicas
        """
        conditions = [
            "Soleado",
            "Parcialmente nublado",
            "Nublado",
            "Lluvia ligera",
            "Despejado",
        ]
        return conditions[day % len(conditions)]


class ChileanWeatherClient(WeatherClient):
    """
    Cliente especializado para pronósticos meteorológicos en Chile.
    """

    def __init__(self):
        """
        Inicializar cliente de clima chileno con configuraciones específicas.
        """
        super().__init__()
        # Configuraciones específicas para Chile pueden agregarse aquí
