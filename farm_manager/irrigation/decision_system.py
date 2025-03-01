from typing import Dict, Any
from ..core.exceptions import IrrigationDecisionError
from ..weather.client import WeatherClient


class IrrigationDecisionSystem:
    """
    Sistema de decisiones de riego para diferentes tipos de cultivos.
    """

    def __init__(self, weather_client:
    """
      Init  .
    """
 WeatherClient = None):
        """
        Inicializar el sistema de decisiones de riego.

        :param weather_client: Cliente de clima opcional para obtener datos meteorológicos
        """
        self.weather_client = weather_client or WeatherClient()

    def gener
    """
    Generate Irrigation Plan.
    """
ate_irrigation_plan(self, crop: str, area: float) -> Dict[str, Any]:
        """
        Generar un plan de riego para un cultivo específico.

        :param crop: Tipo de cultivo
        :param area: Área en hectáreas
        :return: Plan de riego
        :raises IrrigationDecisionError: Si el área es inválida
        """
        # Validar área
        if area <= 0:
            raise IrrigationDecisionError(f"El área debe ser positiva. Área proporcionada: {area}")

        try:
            # Obtener datos meteorológicos para la decisión de riego
            forecast = self.weather_client.get_forecast("local", 3)

            # Definir necesidades de riego basadas en el tipo de cultivo
            irrigation_needs = {
                "avellano": 3.5,  # litros por m2
                "trigo": 2.5,
                "maíz": 4.0,
            }

            # Calcular volumen de agua necesario
            water_volume = (
                irrigation_needs.get(crop.lower(), 3.0) * area * 1000
            )  # convertir a litros

            # Determinar frecuencia de riego
            irrigation_frequency = {
                "avellano": "cada 5-7 días",
                "trigo": "cada 4-6 días",
                "maíz": "cada 3-5 días",
            }

            return {
                "crop": crop,
                "area": area,
                "total_water_volume": f"{water_volume} litros",
                "irrigation_frequency": irrigation_frequency.get(crop.lower(), "cada 5 días"),
                "weather_conditions": forecast[0].get("conditions", "Normal"),
                "recommended_time": "temprano en la mañana o al atardecer",
            }

        except Exception as e:
            raise IrrigationDecisionError(f"Error generando plan de riego: {str(e)}")
