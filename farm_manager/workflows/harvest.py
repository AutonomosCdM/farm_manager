from typing import Dict, Any, List
from .template import WorkflowTemplate


class HarvestTemplate(WorkflowTemplate):
    """Template for crop harvesting operations."""

    def __init__(self):
        super().__init__(
            name="Cosecha de Cultivos",
            description="Plantilla para operaciones de recolección y cosecha",
        )

    def generate_plan(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a harvest workflow plan.

        Expected context keys:
        - crop_type: Type of crop to harvest
        - area_hectares: Total area for harvesting
        - expected_yield: Expected yield per hectare
        - harvest_date: Recommended harvest date
        """
        required_keys = ["crop_type", "area_hectares", "expected_yield", "harvest_date"]
        for key in required_keys:
            if key not in context:
                raise ValueError(f"Missing required context key: {key}")

        plan = {
            "operation": "Harvest",
            "crop": context["crop_type"],
            "area": context["area_hectares"],
            "expected_total_yield": context["expected_yield"] * context["area_hectares"],
            "harvest_steps": [
                f"Evaluar madurez de {context['crop_type']} en {context['area_hectares']} hectáreas",
                "Preparar maquinaria de cosecha",
                f"Realizar cosecha en fecha: {context['harvest_date']}",
                "Inspeccionar calidad de los productos cosechados",
                "Preparar almacenamiento y transporte",
            ],
            "equipment_needed": self._get_equipment(context["crop_type"]),
            "estimated_labor": self._calculate_labor(context["area_hectares"]),
        }

        return plan

    def validate_plan(self, plan: Dict[str, Any]) -> bool:
        """
        Validate the harvest plan for completeness.

        :param plan: The plan to validate
        :return: Boolean indicating if the plan is valid
        """
        required_keys = [
            "operation",
            "crop",
            "area",
            "expected_total_yield",
            "harvest_steps",
            "equipment_needed",
            "estimated_labor",
        ]

        return (
            all(key in plan for key in required_keys)
            and plan["operation"] == "Harvest"
            and plan["area"] > 0
            and plan["expected_total_yield"] > 0
            and len(plan["harvest_steps"]) > 0
        )

    def _get_equipment(self, crop_type: str) -> List[str]:
        """Recommend harvesting equipment based on crop type."""
        equipment_map = {
            "avellano": ["Cosechadora de avellanos", "Tractor", "Remolque"],
            "trigo": ["Cosechadora de granos", "Tractor", "Remolque de granos"],
            "maíz": ["Cosechadora de maíz", "Tractor", "Remolque de granos"],
        }
        return equipment_map.get(crop_type, ["Cosechadora", "Tractor", "Herramientas básicas"])

    def _calculate_labor(self, area_hectares: float) -> Dict[str, Any]:
        """Estimate labor requirements based on area."""
        return {
            "workers_required": max(3, int(area_hectares * 0.7)),
            "estimated_hours": area_hectares * 6,
            "complexity": "alta" if area_hectares > 10 else "media",
        }
