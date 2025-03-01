from typing import Dict, Any
from farm_manager.workflows import (
    WorkflowTemplate, 
    PlantingTemplate, 
    HarvestTemplate, 
    MaintenanceTemplate
)

class WorkflowTemplateManager:
    """
    Manages and selects workflow templates based on context.
    """
    
    def __init__(self):
        self.templates = {
            'planting': PlantingTemplate(),
            'harvest': HarvestTemplate(),
            'maintenance': MaintenanceTemplate()
        }
    
    def get_template(self, operation_type: str) -> WorkflowTemplate:
        """
        Select a template based on operation type.
        
        :param operation_type: Type of agricultural operation
        :return: Appropriate workflow template
        """
        template = self.templates.get(operation_type.lower())
        if not template:
            raise ValueError(f"No template found for operation type: {operation_type}")
        return template
    
    def generate_workflow(self, operation_type: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a workflow plan using the appropriate template.
        
        :param operation_type: Type of agricultural operation
        :param context: Context parameters for the operation
        :return: Generated workflow plan
        """
        template = self.get_template(operation_type)
        plan = template.generate_plan(context)
        
        if not template.validate_plan(plan):
            raise ValueError("Generated plan failed validation")
        
        return plan

# Example usage and testing
if __name__ == "__main__":
    manager = WorkflowTemplateManager()
    
    # Example context for planting avellanos
    avellano_context = {
        'crop_type': 'avellano',
        'area_hectares': 5.5,
        'soil_type': 'franco',
        'planting_date': '2025-07-15'
    }
    
    # Example context for harvest
    harvest_context = {
        'crop_type': 'trigo',
        'area_hectares': 10.0,
        'expected_yield': 3.5,  # tons per hectare
        'harvest_date': '2025-12-10'
    }
    
    # Example context for maintenance
    maintenance_context = {
        'crop_type': 'maíz',
        'area_hectares': 8.0,
        'maintenance_type': 'pest_control',
        'maintenance_date': '2025-09-20'
    }
    
    try:
        print("Planting Workflow:")
        planting_plan = manager.generate_workflow('planting', avellano_context)
        print(planting_plan)
        
        print("\nHarvest Workflow:")
        harvest_plan = manager.generate_workflow('harvest', harvest_context)
        print(harvest_plan)
        
        print("\nMaintenance Workflow:")
        maintenance_plan = manager.generate_workflow('maintenance', maintenance_context)
        print(maintenance_plan)
    except Exception as e:
        print(f"Error generating workflow: {e}")
