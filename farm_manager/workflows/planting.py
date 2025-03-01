from typing import Dict, Any, List
from .template import WorkflowTemplate


class PlantingTemplate(WorkflowTemplate):
    """Template for crop planting operations."""

    def __init__(self):
        super().__init__(
            name="Plantación de Cultivos",
            description="Plantilla para operaciones de siembra y plantación",
        )

    def generate_plan(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a planting workflow plan.

        Expected context keys:
        - crop_type: Type of crop to plant
        - area_hectares: Total area for planting
        - soil_type: Type of soil
        - planting_date: Recommended planting date
        """
        required_keys = ["crop_type", "area_hectares", "soil_type", "planting_date"]
        for key in required_keys:
            if key not in context:
                raise ValueError(f"Missing required context key: {key}")

        plan = {
            "operation": "Planting",
            "crop": context["crop_type"],
            "area": context["area_hectares"],
            "soil_preparation": self._recommend_soil_preparation(context["soil_type"]),
            "planting_steps": [
                f"Preparar terreno de {context['area_hectares']} hectáreas",
                f"Seleccionar semillas de {context['crop_type']}",
                "Calibrar maquinaria de siembra",
                f"Sembrar en fecha: {context['planting_date']}",
            ],
            "equipment_needed": self._get_equipment(context["crop_type"]),
            "estimated_labor": self._calculate_labor(context["area_hectares"]),
        }

        return plan

    def validate_plan(self, plan: Dict[str, Any]) -> bool:
        """
        Validate the planting plan for completeness.

        :param plan: The plan to validate
        :return: Boolean indicating if the plan is valid
        """
        required_keys = [
            "operation",
            "crop",
            "area",
            "soil_preparation",
            "planting_steps",
            "equipment_needed",
            "estimated_labor",
        ]

        return (
            all(key in plan for key in required_keys)
            and plan["operation"] == "Planting"
            and plan["area"] > 0
            and len(plan["planting_steps"]) > 0
        )

    def _recommend_soil_preparation(self, soil_type: str) -> str:
        """Recommend soil preparation based on soil type."""
        soil_prep_map = {
            "arcilloso": "Arado profundo y adición de materia orgánica",
            "arenoso": "Adición de compost y mejoradores de suelo",
            "franco": "Labranza mínima con fertilización balanceada",
        }
        return soil_prep_map.get(soil_type, "Preparación estándar de suelo")

    def _get_equipment(self, crop_type: str) -> List[str]:
        """Recommend equipment based on crop type."""
        equipment_map = {
            "avellano": ["Tractor", "Arado", "Sembradora especializada"],
            "trigo": ["Tractor", "Sembradora de granos", "Cultivador"],
            "maíz": ["Tractor", "Sembradora de precisión", "Cultivador"],
        }
        return equipment_map.get(crop_type, ["Tractor", "Herramientas básicas"])

    def _calculate_labor(self, area_hectares: float) -> Dict[str, Any]:
        """Estimate labor requirements based on area."""
        return {
            "workers_required": max(2, int(area_hectares * 0.5)),
            "estimated_hours": area_hectares * 4,
            "complexity": "media" if area_hectares < 10 else "alta",
        }
