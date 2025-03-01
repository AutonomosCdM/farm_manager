# Referencia de API de Farm Manager

## Módulo de Workflows

### `farm_manager.workflows.WorkflowTemplate`

Clase base abstracta para plantillas de flujo de trabajo.

#### Métodos

- `generate_plan(context: Dict[str, Any]) -> Dict[str, Any]`
  - Genera un plan de trabajo basado en el contexto proporcionado
  - Parámetros:
    * `context`: Diccionario con detalles de la operación
  - Retorna: Plan de trabajo detallado

- `validate_plan(plan: Dict[str, Any]) -> bool`
  - Valida la coherencia de un plan de trabajo
  - Parámetros:
    * `plan`: Plan de trabajo a validar
  - Retorna: Booleano indicando validez del plan

### Plantillas Específicas

#### `PlantingTemplate`
Plantilla especializada para planes de plantación.

##### Métodos Adicionales
- `_recommend_soil_preparation(soil_type: str) -> str`
- `_get_equipment(crop_type: str) -> List[str]`
- `_calculate_labor(area_hectares: float) -> Dict[str, Any]`

#### `HarvestTemplate`
Plantilla especializada para planes de cosecha.

##### Métodos Adicionales
- `_get_equipment(crop_type: str) -> List[str]`
- `_calculate_labor(area_hectares: float) -> Dict[str, Any]`

#### `MaintenanceTemplate`
Plantilla especializada para planes de mantenimiento.

##### Métodos Adicionales
- `_generate_maintenance_steps(context: Dict[str, Any]) -> List[str]`
- `_get_equipment(maintenance_type: str) -> List[str]`
- `_calculate_labor(area_hectares: float, maintenance_type: str) -> Dict[str, Any]`

## Módulo de Irrigación

### `farm_manager.irrigation.IrrigationDecisionSystem`

Sistema de toma de decisiones para planes de riego.

#### Métodos

- `generate_irrigation_plan(crop: str, area: float) -> Dict[str, Any]`
  - Genera un plan de riego para un cultivo específico
  - Parámetros:
    * `crop`: Tipo de cultivo
    * `area`: Área en hectáreas
  - Retorna: Plan de riego detallado
  - Lanza: `IrrigationDecisionError` si hay problemas

## Módulo de Clima

### `farm_manager.weather.WeatherClient`

Cliente para obtener información meteorológica.

#### Métodos

- `get_forecast(location: str, days: int = 3) -> List[Dict[str, Any]]`
  - Obtiene pronóstico meteorológico para una ubicación
  - Parámetros:
    * `location`: Ubicación geográfica
    * `days`: Número de días de pronóstico (defecto: 3)
  - Retorna: Lista de pronósticos diarios
  - Lanza: `WeatherClientError` en caso de error

### `farm_manager.weather.ChileanWeatherClient`

Cliente especializado para pronósticos en Chile.

## Módulo de Recursos

### `farm_manager.resources.ResourceManager`

Gestión y optimización de recursos agrícolas.

#### Métodos

- `list_resources(resource_type: Optional[str] = None) -> List[Dict[str, Any]]`
  - Lista recursos disponibles
  - Parámetros:
    * `resource_type`: Tipo de recurso (opcional)
  - Retorna: Lista de recursos
  - Lanza: `ResourceManagementError` en caso de error

- `optimize_resources(resource_type: Optional[str] = None) -> Dict[str, Any]`
  - Optimiza recursos agrícolas
  - Parámetros:
    * `resource_type`: Tipo de recurso (opcional)
  - Retorna: Resultados de optimización
  - Lanza: `ResourceManagementError` en caso de error

## Módulo Core (Excepciones)

### Excepciones Personalizadas

- `FarmManagerBaseError`: Excepción base para errores del sistema
- `WeatherClientError`: Errores en cliente meteorológico
- `IrrigationDecisionError`: Errores en decisiones de riego
- `ResourceManagementError`: Errores en gestión de recursos
- `WorkflowTemplateError`: Errores en plantillas de workflow

## Ejemplos de Uso

### Generación de Workflow

```python
from farm_manager.workflows import WorkflowTemplateManager

manager = WorkflowTemplateManager()
context = {
    'crop_type': 'avellano',
    'area_hectares': 5.5,
    'soil_type': 'franco',
    'planting_date': '2025-07-15'
}
workflow_plan = manager.generate_workflow('planting', context)
```

### Plan de Riego

```python
from farm_manager.irrigation import IrrigationDecisionSystem

irrigation_system = IrrigationDecisionSystem()
irrigation_plan = irrigation_system.generate_irrigation_plan('trigo', 10.0)
```

### Pronóstico Meteorológico

```python
from farm_manager.weather import WeatherClient

client = WeatherClient()
forecast = client.get_forecast('Santiago', days=3)
```

### Gestión de Recursos

```python
from farm_manager.resources import ResourceManager

manager = ResourceManager()
resources = manager.list_resources('machinery')
optimization = manager.optimize_resources()
