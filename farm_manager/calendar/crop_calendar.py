import datetime
from typing import Dict, List, Optional

from .models import CropStage, CropCalendarModel
from ..core.exceptions import CropCalendarError


class CropCalendar:
    """
    Manages agricultural calendars for local crops in the Los Ríos region.
    """

    def __init__(self):
        """
        Initialize the agricultural calendar with predefined crop cycles.
        """
        self.crop_calendars: Dict[str, CropCalendarModel] = {
            "avellano_europeo": CropCalendarModel(
                name="Avellano Europeo",
                key_stages=[
                    CropStage(
                        name="dormancia",
                        start_month=6,  # June (winter in Southern Hemisphere)
                        end_month=8,  # August
                        description="Período de reposo vegetativo",
                        recommended_actions=[
                            "Realizar poda de formación",
                            "Aplicar tratamientos preventivos contra plagas",
                        ],
                    ),
                    CropStage(
                        name="floracion",
                        start_month=9,  # September
                        end_month=10,  # October
                        description="Período de floración",
                        recommended_actions=[
                            "Control de polinización",
                            "Monitoreo de condiciones climáticas",
                        ],
                    ),
                    CropStage(
                        name="cuaja",
                        start_month=11,  # November
                        end_month=12,  # December
                        description="Formación inicial de frutos",
                        recommended_actions=["Fertilización", "Control de riego"],
                    ),
                    CropStage(
                        name="desarrollo_fruto",
                        start_month=1,  # January
                        end_month=4,  # April
                        description="Desarrollo y maduración de frutos",
                        recommended_actions=[
                            "Monitoreo de crecimiento",
                            "Control de plagas y enfermedades",
                        ],
                    ),
                    CropStage(
                        name="cosecha",
                        start_month=4,  # April
                        end_month=5,  # May
                        description="Período de cosecha",
                        recommended_actions=[
                            "Preparar equipos de cosecha",
                            "Planificar almacenamiento",
                        ],
                    ),
                ],
            )
        }

    def get_current_stage(
        self, crop_name: str, current_date: Optional[datetime.date] = None
    ) -> Dict[str, Any]:
        """
        Determine the current stage of a crop based on the current date.

        :param crop_name: Name of the crop
        :param current_date: Date to check (defaults to current date)
        :return: Dictionary with current stage information
        """
        if current_date is None:
            current_date = datetime.date.today()

        # Normalize crop name
        normalized_name = crop_name.lower().replace(" ", "_")

        # Find crop calendar
        crop_calendar = self.crop_calendars.get(normalized_name)
        if not crop_calendar:
            raise CropCalendarError(f"No calendar found for crop: {crop_name}")

        current_month = current_date.month

        # Find current stage
        for stage in crop_calendar.key_stages:
            # Handle year-crossing stages
            if stage.start_month <= stage.end_month:
                if stage.start_month <= current_month <= stage.end_month:
                    return {
                        "crop": crop_calendar.name,
                        "stage": stage.name,
                        "description": stage.description,
                        "recommended_actions": stage.recommended_actions,
                    }
            else:
                # Handle stages that cross the year boundary
                if current_month >= stage.start_month or current_month <= stage.end_month:
                    return {
                        "crop": crop_calendar.name,
                        "stage": stage.name,
                        "description": stage.description,
                        "recommended_actions": stage.recommended_actions,
                    }

        raise CropCalendarError(f"Could not determine stage for {crop_name}")

    def get_crop_calendar(self, crop_name: str) -> CropCalendarModel:
        """
        Retrieve the full calendar for a specific crop.

        :param crop_name: Name of the crop
        :return: CropCalendarModel with complete crop calendar
        """
        # Normalize crop name
        normalized_name = crop_name.lower().replace(" ", "_")

        crop_calendar = self.crop_calendars.get(normalized_name)
        if not crop_calendar:
            raise CropCalendarError(f"No calendar found for crop: {crop_name}")

        return crop_calendar

    def get_recommended_actions(
        self, crop_name: str, current_date: Optional[datetime.date] = None
    ) -> List[str]:
        """
        Get recommended actions for a crop at its current stage.

        :param crop_name: Name of the crop
        :param current_date: Date to check (defaults to current date)
        :return: List of recommended actions
        """
        current_stage = self.get_current_stage(crop_name, current_date)
        return current_stage["recommended_actions"]
