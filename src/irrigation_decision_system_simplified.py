import logging
from typing import Dict, Any, Optional
from datetime import datetime

from src.weather_client import ChileanWeatherClient
from src.regional_knowledge_base import RegionalKnowledgeBase
from src.agricultural_calendar import CropCalendar

class IrrigationDecisionSystem:
    """
    Sistema de decisión inteligente para recomendaciones de riego
    basado en condiciones climáticas, tipo de suelo, etapa del cultivo 
    y conocimiento regional.
    
    Versión simplificada sin dependencias de machine learning.
    """
    
    def __init__(self, region: str = 'Los Ríos'):
        """
        Inicializa el sistema de decisión de riego.
        
        :param region: Región chilena para la cual se generarán recomendaciones
        """
        self.weather_client = ChileanWeatherClient()
        self.knowledge_base = RegionalKnowledgeBase()
        self.crop_calendar = CropCalendar()
        self.region = region
        self.logger = logging.getLogger(__name__)
        
        # Umbrales base para decisiones de riego con mayor granularidad
        self.IRRIGATION_THRESHOLDS = {
            'low_moisture': {
                'general': 30,  # Porcentaje de humedad del suelo general
                'sandy': 20,    # Suelos arenosos
                'clay': 40,     # Suelos arcillosos
                'loam': 35      # Suelos francos
            },
            'high_temperature': {
                'low_stress': 25,   # Temperatura de estrés bajo
                'medium_stress': 30,  # Temperatura de estrés medio
                'high_stress': 35    # Temperatura de estrés alto
            },
            'low_precipitation': 5,  # mm de precipitación
        }
        
        # Historial de retroalimentación
        self.feedback_history = []
    
    def _get_crop_water_requirements(self, crop_name: str) -> Dict[str, Any]:
        """
        Consulta los requerimientos de agua para un cultivo específico.
        
        :param crop_name: Nombre del cultivo
        :return: Diccionario con requerimientos de agua
        """
        crop_results = self.knowledge_base.query_crops(crop_name)
        
        if not crop_results:
            self.logger.warning(f"No se encontraron datos para el cultivo: {crop_name}")
            return {
                'water_need': 'medium',
                'sensitivity': 'moderate'
            }
        
        return {
            'water_need': crop_results[0].get('metadata', {}).get('water_need', 'medium'),
            'sensitivity': crop_results[0].get('metadata', {}).get('water_sensitivity', 'moderate')
        }
    
    def generate_irrigation_recommendation(
        self, 
        crop_name: str, 
        current_weather: Optional[Dict[str, Any]] = None,
        soil_type: Optional[str] = None,
        crop_stage: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Genera recomendaciones de riego basadas en condiciones climáticas, 
        características del cultivo, tipo de suelo y etapa de desarrollo.
        
        :param crop_name: Nombre del cultivo
        :param current_weather: Datos meteorológicos actuales (opcional)
        :param soil_type: Tipo de suelo (opcional, por defecto 'general')
        :param crop_stage: Etapa de desarrollo del cultivo (opcional)
        :return: Recomendación de riego con justificación detallada
        """
        # Obtener datos meteorológicos si no se proporcionan
        if current_weather is None:
            current_weather = self.weather_client.get_weather_by_region(self.region)
        
        if not current_weather:
            self.logger.error("No se pudieron obtener datos meteorológicos")
            return {
                'recommendation': 'No determinado',
                'justification': 'Datos meteorológicos no disponibles',
                'confidence': 0
            }
        
        # Obtener etapa actual del cultivo si no se proporciona
        if crop_stage is None:
            try:
                crop_stage_info = self.crop_calendar.get_current_stage(crop_name)
                crop_stage = crop_stage_info['stage']
            except Exception as e:
                self.logger.warning(f"No se pudo obtener la etapa del cultivo: {e}")
                crop_stage = 'desconocida'
        
        # Obtener requerimientos específicos del cultivo
        crop_water_needs = self._get_crop_water_requirements(crop_name)
        
        # Determinar umbrales de humedad según el tipo de suelo
        soil_type = soil_type or 'general'
        moisture_threshold = self.IRRIGATION_THRESHOLDS['low_moisture'].get(soil_type, self.IRRIGATION_THRESHOLDS['low_moisture']['general'])
        
        # Análisis de condiciones para decisión de riego
        recommendation = {
            'crop': crop_name,
            'region': self.region,
            'current_conditions': current_weather,
            'crop_stage': crop_stage,
            'soil_type': soil_type
        }
        
        # Factores para la justificación detallada
        factors = []
        
        # Lógica de decisión de riego con consideraciones más complejas
        temperature = current_weather.get('temperature', 0)
        humidity = current_weather.get('humidity', 100)
        
        # Evaluar estrés por temperatura
        if temperature > self.IRRIGATION_THRESHOLDS['high_temperature']['high_stress']:
            factors.append(f"Temperatura extrema de {temperature}°C genera alto estrés hídrico")
        elif temperature > self.IRRIGATION_THRESHOLDS['high_temperature']['medium_stress']:
            factors.append(f"Temperatura de {temperature}°C indica estrés hídrico moderado")
        
        # Evaluar humedad del suelo
        if humidity < moisture_threshold:
            factors.append(f"Humedad del suelo ({humidity}%) por debajo del umbral para suelos {soil_type}")
        
        # Considerar etapa del cultivo
        stage_water_needs = {
            'dormancia': 'Bajo',
            'floracion': 'Alto',
            'cuaja': 'Medio',
            'desarrollo_fruto': 'Alto',
            'cosecha': 'Bajo'
        }
        
        stage_water_volume = stage_water_needs.get(crop_stage, 'Medio')
        factors.append(f"Etapa de {crop_stage} requiere riego {stage_water_volume}")
        
        # Generar recomendación basada en los factores
        if len(factors) > 2:  # Múltiples factores de estrés
            recommendation.update({
                'recommendation': 'Riego Intensivo',
                'justification': f"Múltiples factores de estrés detectados: {'; '.join(factors)}",
                'water_volume': 'Alto',
                'confidence': 0.9
            })
        elif len(factors) > 1:  # Algunos factores de estrés
            recommendation.update({
                'recommendation': 'Riego Moderado',
                'justification': f"Factores de estrés moderado: {'; '.join(factors)}",
                'water_volume': 'Medio',
                'confidence': 0.7
            })
        else:
            recommendation.update({
                'recommendation': 'Riego Mínimo',
                'justification': 'Condiciones climáticas y de cultivo estables',
                'water_volume': 'Bajo',
                'confidence': 0.5
            })
        
        return recommendation
    
    def log_irrigation_feedback(
        self, 
        crop_name: str, 
        recommendation: Dict[str, Any], 
        actual_outcome: Dict[str, Any]
    ):
        """
        Registra retroalimentación sobre la precisión de las recomendaciones.
        
        :param crop_name: Nombre del cultivo
        :param recommendation: Recomendación original
        :param actual_outcome: Resultado real después de la recomendación
        """
        # Registrar la retroalimentación en el historial
        feedback_entry = {
            'crop': crop_name,
            'recommendation': recommendation,
            'actual_outcome': actual_outcome,
            'timestamp': datetime.now()
        }
        self.feedback_history.append(feedback_entry)
        
        # Registro de retroalimentación
        self.logger.info(f"Feedback para {crop_name}:")
        self.logger.info(f"Recomendación original: {recommendation}")
        self.logger.info(f"Resultado real: {actual_outcome}")
    
    def validate_recommendation(self, recommendation: Dict[str, Any]) -> Dict[str, Any]:
        """
        Valida la recomendación de riego contra criterios predefinidos.
        
        :param recommendation: Recomendación de riego a validar
        :return: Diccionario con resultados de validación
        """
        # Criterios de validación básicos
        basic_criteria = [
            recommendation.get('confidence', 0) > 0.6,
            recommendation.get('recommendation') in ['Riego Intensivo', 'Riego Moderado', 'Riego Mínimo']
        ]
        
        # Validación basada en reglas
        validation_result = {
            'basic_criteria_met': all(basic_criteria),
            'overall_confidence': recommendation.get('confidence', 0),
            'is_valid': all(basic_criteria)
        }
        
        return validation_result

# Ejemplo de uso
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    irrigation_system = IrrigationDecisionSystem()
    
    # Ejemplo de recomendación para Avellano Europeo
    recommendation = irrigation_system.generate_irrigation_recommendation("Avellano Europeo")
    print("Recomendación de Riego:")
    for key, value in recommendation.items():
        print(f"{key}: {value}")
