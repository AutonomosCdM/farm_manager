from typing import Dict, Any, List
from .template import WorkflowTemplate


class MaintenanceTemplate(WorkflowTemplate):
    """Template for crop and farm maintenance operations."""

    def __init__(self):
        super().__init__(
            name="Mantenimiento de Cultivos y Infraestructura",
            description="Plantilla para operaciones de mantenimiento agrícola",
        )

    def generate_plan(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a maintenance workflow plan.

        Expected context keys:
        - crop_type: Type of crop being maintained
        - area_hectares: Total area for maintenance
        - maintenance_type: Specific type of maintenance (irrigation, fertilization, pest control)
        - maintenance_date: Recommended maintenance date
        """
        required_keys = [
            "crop_type",
            "area_hectares",
            "maintenance_type",
            "maintenance_date",
        ]
        for key in required_keys:
            if key not in context:
                raise ValueError(f"Missing required context key: {key}")

        plan = {
            "operation": "Maintenance",
            "crop": context["crop_type"],
            "area": context["area_hectares"],
            "maintenance_type": context["maintenance_type"],
            "maintenance_steps": self._generate_maintenance_steps(context),
            "equipment_needed": self._get_equipment(context["maintenance_type"]),
            "estimated_labor": self._calculate_labor(
                context["area_hectares"], context["maintenance_type"]
            ),
        }

        return plan

    def validate_plan(self, plan: Dict[str, Any]) -> bool:
        """
        Validate the maintenance plan for completeness.

        :param plan: The plan to validate
        :return: Boolean indicating if the plan is valid
        """
        required_keys = [
            "operation",
            "crop",
            "area",
            "maintenance_type",
            "maintenance_steps",
            "equipment_needed",
            "estimated_labor",
        ]

        return (
            all(key in plan for key in required_keys)
            and plan["operation"] == "Maintenance"
            and plan["area"] > 0
            and len(plan["maintenance_steps"]) > 0
        )

    def _generate_maintenance_steps(self, context: Dict[str, Any]) -> List[str]:
        """
        Generate specific maintenance steps based on maintenance type.

        :param context: Context dictionary with maintenance details
        :return: List of maintenance steps
        """
        maintenance_type = context["maintenance_type"]
        crop_type = context["crop_type"]
        area = context["area_hectares"]
        maintenance_date = context["maintenance_date"]

        steps_map = {
            "irrigation": [
                f"Evaluar estado de riego para {crop_type} en {area} hectáreas",
                f"Verificar sistemas de riego y tuberías",
                f"Programar riego en fecha: {maintenance_date}",
                "Ajustar volumen de agua según condiciones del cultivo",
            ],
            "fertilization": [
                f"Analizar composición del suelo para {crop_type}",
                f"Seleccionar fertilizantes apropiados para {area} hectáreas",
                f"Aplicar fertilizantes en fecha: {maintenance_date}",
                "Monitorear absorción de nutrientes",
            ],
            "pest_control": [
                f"Inspeccionar presencia de plagas en {crop_type}",
                "Identificar tipos de plagas y nivel de infestación",
                f"Seleccionar métodos de control para {area} hectáreas",
                f"Aplicar tratamiento en fecha: {maintenance_date}",
                "Evaluar efectividad del tratamiento",
            ],
        }

        return steps_map.get(
            maintenance_type,
            [
                f"Realizar mantenimiento general para {crop_type}",
                f"Cubrir {area} hectáreas",
                f"Fecha de mantenimiento: {maintenance_date}",
            ],
        )

    def _get_equipment(self, maintenance_type: str) -> List[str]:
        """Recommend equipment based on maintenance type."""
        equipment_map = {
            "irrigation": [
                "Sistema de riego",
                "Bombas de agua",
                "Mangueras",
                "Aspersores",
            ],
            "fertilization": [
                "Esparcidor de fertilizantes",
                "Tractor",
                "Tanque de fertilizantes",
            ],
            "pest_control": ["Fumigadora", "Equipo de protección", "Pulverizador"],
        }
        return equipment_map.get(maintenance_type, ["Herramientas básicas de mantenimiento"])

    def _calculate_labor(self, area_hectares: float, maintenance_type: str) -> Dict[str, Any]:
        """Estimate labor requirements based on area and maintenance type."""
        labor_multipliers = {
            "irrigation": 0.4,
            "fertilization": 0.6,
            "pest_control": 0.8,
        }

        multiplier = labor_multipliers.get(maintenance_type, 0.5)

        return {
            "workers_required": max(2, int(area_hectares * multiplier)),
            "estimated_hours": area_hectares * 3,
            "complexity": "media" if area_hectares < 15 else "alta",
        }
