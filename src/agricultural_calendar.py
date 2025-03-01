import datetime
from typing import Dict, List, Optional

class CropCalendar:
    """
    Manages agricultural calendars for local crops in the Los Ríos region.
    """
    
    def __init__(self):
        """
        Initialize the agricultural calendar with predefined crop cycles.
        """
        self.crop_cycles = {
            'avellano_europeo': {
                'name': 'Avellano Europeo',
                'key_stages': {
                    'dormancia': {
                        'start_month': 6,  # June (winter in Southern Hemisphere)
                        'end_month': 8,    # August
                        'description': 'Período de reposo vegetativo'
                    },
                    'floracion': {
                        'start_month': 9,  # September
                        'end_month': 10,   # October
                        'description': 'Período de floración'
                    },
                    'cuaja': {
                        'start_month': 11,  # November
                        'end_month': 12,    # December
                        'description': 'Formación inicial de frutos'
                    },
                    'desarrollo_fruto': {
                        'start_month': 1,  # January
                        'end_month': 4,    # April
                        'description': 'Desarrollo y maduración de frutos'
                    },
                    'cosecha': {
                        'start_month': 4,  # April
                        'end_month': 5,    # May
                        'description': 'Período de cosecha'
                    }
                },
                'recommended_actions': {
                    'dormancia': [
                        'Realizar poda de formación',
                        'Aplicar tratamientos preventivos contra plagas'
                    ],
                    'floracion': [
                        'Control de polinización',
                        'Monitoreo de condiciones climáticas'
                    ],
                    'cuaja': [
                        'Fertilización',
                        'Control de riego'
                    ],
                    'desarrollo_fruto': [
                        'Monitoreo de crecimiento',
                        'Control de plagas y enfermedades'
                    ],
                    'cosecha': [
                        'Preparar equipos de cosecha',
                        'Planificar almacenamiento'
                    ]
                }
            }
        }
    
    def get_current_stage(self, crop_name: str, current_date: Optional[datetime.date] = None) -> Dict:
        """
        Determine the current stage of a crop based on the current date.
        
        :param crop_name: Name of the crop
        :param current_date: Date to check (defaults to current date)
        :return: Dictionary with current stage information
        """
        if current_date is None:
            current_date = datetime.date.today()
        
        crop = self.crop_cycles.get(crop_name.lower().replace(' ', '_'))
        if not crop:
            raise ValueError(f"No calendar found for crop: {crop_name}")
        
        current_month = current_date.month
        
        for stage_name, stage_info in crop['key_stages'].items():
            # Handle year-crossing stages (e.g., from December to January)
            if stage_info['start_month'] <= stage_info['end_month']:
                if stage_info['start_month'] <= current_month <= stage_info['end_month']:
                    return {
                        'crop': crop['name'],
                        'stage': stage_name,
                        'description': stage_info['description'],
                        'recommended_actions': crop['recommended_actions'][stage_name]
                    }
            else:
                # Handle stages that cross the year boundary
                if current_month >= stage_info['start_month'] or current_month <= stage_info['end_month']:
                    return {
                        'crop': crop['name'],
                        'stage': stage_name,
                        'description': stage_info['description'],
                        'recommended_actions': crop['recommended_actions'][stage_name]
                    }
        
        raise ValueError(f"Could not determine stage for {crop_name}")
    
    def get_crop_calendar(self, crop_name: str) -> Dict:
        """
        Retrieve the full calendar for a specific crop.
        
        :param crop_name: Name of the crop
        :return: Dictionary with complete crop calendar
        """
        crop = self.crop_cycles.get(crop_name.lower().replace(' ', '_'))
        if not crop:
            raise ValueError(f"No calendar found for crop: {crop_name}")
        
        return crop
    
    def get_recommended_actions(self, crop_name: str, current_date: Optional[datetime.date] = None) -> List[str]:
        """
        Get recommended actions for a crop at its current stage.
        
        :param crop_name: Name of the crop
        :param current_date: Date to check (defaults to current date)
        :return: List of recommended actions
        """
        current_stage = self.get_current_stage(crop_name, current_date)
        return current_stage['recommended_actions']

def main():
    """
    Demonstrate the usage of the agricultural calendar.
    """
    calendar = CropCalendar()
    
    # Example usage for Avellano Europeo
    try:
        # Check current stage for Avellano Europeo
        current_stage = calendar.get_current_stage('avellano_europeo')
        print(f"Current Stage: {current_stage['stage']}")
        print(f"Description: {current_stage['description']}")
        print("Recommended Actions:")
        for action in current_stage['recommended_actions']:
            print(f"- {action}")
        
        # Get full calendar
        full_calendar = calendar.get_crop_calendar('avellano_europeo')
        print("\nFull Crop Calendar:")
        for stage, details in full_calendar['key_stages'].items():
            print(f"{stage.capitalize()}: {details['description']}")
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
