import calendar
from typing import List, Dict, Any
from datetime import datetime
from .models import CropCalendarModel, CropStage


class CalendarVisualizer:
    """
    Provides visualization and formatting for agricultural calendars.
    """

    @staticmethod
    def generate_text_calendar(crop_calendar: CropCalendarModel, year: int = None) -> str:
        """
        Generate a text-based visualization of the crop calendar.

        :param crop_calendar: CropCalendarModel to visualize
        :param year: Year to use for visualization (defaults to current year)
        :return: Formatted text calendar
        """
        if year is None:
            year = datetime.now().year

        # Create calendar header
        calendar_text = f"Agricultural Calendar for {crop_calendar.name} ({year})\n"
        calendar_text += "=" * 50 + "\n\n"

        # Iterate through months
        for month in range(1, 13):
            month_name = calendar.month_name[month]
            calendar_text += f"{month_name.upper()} {year}\n"
            calendar_text += "-" * 20 + "\n"

            # Check if this month is part of any stage
            current_stages = [
                stage for stage in crop_calendar.key_stages if stage.is_current_stage(month)
            ]

            if current_stages:
                for stage in current_stages:
                    calendar_text += f"Stage: {stage.name.capitalize()}\n"
                    calendar_text += f"Description: {stage.description}\n"
                    calendar_text += "Recommended Actions:\n"
                    for action in stage.recommended_actions:
                        calendar_text += f"- {action}\n"
            else:
                calendar_text += "No specific crop stage this month\n"

            calendar_text += "\n"

        return calendar_text

    @staticmethod
    def generate_json_calendar(
        crop_calendar: CropCalendarModel, year: int = None
    ) -> Dict[str, Any]:
        """
        Generate a JSON representation of the crop calendar.

        :param crop_calendar: CropCalendarModel to visualize
        :param year: Year to use for visualization (defaults to current year)
        :return: JSON-compatible dictionary of the calendar
        """
        if year is None:
            year = datetime.now().year

        calendar_data = {"crop": crop_calendar.name, "year": year, "monthly_stages": {}}

        # Iterate through months
        for month in range(1, 13):
            month_name = calendar.month_name[month]

            # Check if this month is part of any stage
            current_stages = [
                stage for stage in crop_calendar.key_stages if stage.is_current_stage(month)
            ]

            calendar_data["monthly_stages"][month_name] = {
                "stages": (
                    [
                        {
                            "name": stage.name,
                            "description": stage.description,
                            "recommended_actions": stage.recommended_actions,
                        }
                        for stage in current_stages
                    ]
                    if current_stages
                    else []
                )
            }

        return calendar_data
