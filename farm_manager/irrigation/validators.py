from typing import Dict, Any, List


class IrrigationValidator:
    """
    Sistema de validación para recomendaciones de riego.
    """

    def validate_recommendation(self, recommendation: Dict[str, Any]) -> Dict[str, Any]:
        """
        Valida una recomendación de riego.

        :param recommendation: Recomendación de riego a validar
        :return: Resultado de la validación
        """
        # Criterios de validación básicos
        basic_criteria = [
            recommendation.get("confidence", 0) > 0.6,
            recommendation.get("recommendation")
            in ["Riego Intensivo", "Riego Moderado", "Riego Mínimo"],
        ]

        # Validación de condiciones meteorológicas
        weather_validation = self._validate_weather_conditions(recommendation)

        # Validación de etapa del cultivo
        crop_stage_validation = self._validate_crop_stage(recommendation)

        # Resultado final de validación
        validation_result = {
            "basic_criteria_met": all(basic_criteria),
            "weather_conditions_valid": weather_validation["valid"],
            "crop_stage_valid": crop_stage_validation["valid"],
            "overall_confidence": self._calculate_overall_confidence(
                recommendation,
                basic_criteria,
                weather_validation,
                crop_stage_validation,
            ),
            "warnings": self._generate_warnings(
                recommendation, weather_validation, crop_stage_validation
            ),
        }

        return validation_result

    def _validate_weather_conditions(self, recommendation: Dict[str, Any]) -> Dict[str, Any]:
        """
        Valida las condiciones meteorológicas de la recomendación.

        :param recommendation: Recomendación de riego
        :return: Resultado de la validación de condiciones meteorológicas
        """
        current_conditions = recommendation.get("current_conditions", {})

        # Umbrales de validación
        temperature_thresholds = {
            "min": -10,  # Temperatura mínima aceptable
            "max": 45,  # Temperatura máxima aceptable
        }
        humidity_thresholds = {
            "min": 10,  # Humedad mínima aceptable
            "max": 100,  # Humedad máxima aceptable
        }

        # Validaciones
        temperature_valid = (
            temperature_thresholds["min"]
            <= current_conditions.get("temperature", 0)
            <= temperature_thresholds["max"]
        )
        humidity_valid = (
            humidity_thresholds["min"]
            <= current_conditions.get("humidity", 0)
            <= humidity_thresholds["max"]
        )

        return {
            "valid": temperature_valid and humidity_valid,
            "temperature": {
                "value": current_conditions.get("temperature", 0),
                "valid": temperature_valid,
            },
            "humidity": {
                "value": current_conditions.get("humidity", 0),
                "valid": humidity_valid,
            },
        }

    def _validate_crop_stage(self, recommendation: Dict[str, Any]) -> Dict[str, Any]:
        """
        Valida la etapa del cultivo en la recomendación.

        :param recommendation: Recomendación de riego
        :return: Resultado de la validación de la etapa del cultivo
        """
        valid_stages = [
            "dormancia",
            "floracion",
            "cuaja",
            "desarrollo_fruto",
            "cosecha",
        ]

        crop_stage = recommendation.get("crop_stage", "desconocida")

        return {"valid": crop_stage in valid_stages, "stage": crop_stage}

    def _calculate_overall_confidence(
        self,
        recommendation: Dict[str, Any],
        basic_criteria: List[bool],
        weather_validation: Dict[str, Any],
        crop_stage_validation: Dict[str, Any],
    ) -> float:
        """
        Calcula la confianza general de la recomendación.

        :param recommendation: Recomendación de riego
        :param basic_criteria: Criterios básicos de validación
        :param weather_validation: Validación de condiciones meteorológicas
        :param crop_stage_validation: Validación de etapa del cultivo
        :return: Confianza general de la recomendación
        """
        # Confianza base de la recomendación
        base_confidence = recommendation.get("confidence", 0.5)

        # Ajustes de confianza
        basic_criteria_factor = 1.0 if all(basic_criteria) else 0.7
        weather_factor = 1.0 if weather_validation["valid"] else 0.6
        crop_stage_factor = 1.0 if crop_stage_validation["valid"] else 0.8

        # Calcular confianza general
        overall_confidence = (
            base_confidence * basic_criteria_factor * weather_factor * crop_stage_factor
        )

        return round(max(0, min(overall_confidence, 1)), 2)

    def _generate_warnings(
        self,
        recommendation: Dict[str, Any],
        weather_validation: Dict[str, Any],
        crop_stage_validation: Dict[str, Any],
    ) -> List[str]:
        """
        Genera advertencias para la recomendación de riego.

        :param recommendation: Recomendación de riego
        :param weather_validation: Validación de condiciones meteorológicas
        :param crop_stage_validation: Validación de etapa del cultivo
        :return: Lista de advertencias
        """
        warnings = []

        # Advertencias de condiciones meteorológicas
        if not weather_validation["temperature"]["valid"]:
            warnings.append(
                f"Temperatura fuera de rango: {weather_validation['temperature']['value']}°C"
            )

        if not weather_validation["humidity"]["valid"]:
            warnings.append(f"Humedad fuera de rango: {weather_validation['humidity']['value']}%")

        # Advertencias de etapa del cultivo
        if not crop_stage_validation["valid"]:
            warnings.append(f"Etapa del cultivo no reconocida: {crop_stage_validation['stage']}")

        return warnings
