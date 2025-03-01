from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


@dataclass
class CropStage:
    """
    Represents a specific stage in a crop's growth cycle.
    """

    name: str
    start_month: int
    end_month: int
    description: str
    recommended_actions: List[str] = field(default_factory=list)

    def is_current_stage(self, current_month: int) -> bool:
        """
        Check if the given month falls within this stage.

        :param current_month: Month to check
        :return: True if the month is in this stage, False otherwise
        """
        if self.start_month <= self.end_month:
            return self.start_month <= current_month <= self.end_month
        else:
            # Handle year-crossing stages
            return current_month >= self.start_month or current_month <= self.end_month


@dataclass
class CropCalendarModel:
    """
    Represents the complete agricultural calendar for a specific crop.
    """

    name: str
    key_stages: List[CropStage]

    def get_stage_by_name(self, stage_name: str) -> Optional[CropStage]:
        """
        Retrieve a specific stage by its name.

        :param stage_name: Name of the stage to retrieve
        :return: CropStage if found, None otherwise
        """
        for stage in self.key_stages:
            if stage.name == stage_name:
                return stage
        return None

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the crop calendar to a dictionary representation.

        :return: Dictionary representation of the crop calendar
        """
        return {
            "name": self.name,
            "key_stages": [
                {
                    "name": stage.name,
                    "start_month": stage.start_month,
                    "end_month": stage.end_month,
                    "description": stage.description,
                    "recommended_actions": stage.recommended_actions,
                }
                for stage in self.key_stages
            ],
        }
