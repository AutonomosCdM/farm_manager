# Guía para Desarrolladores de Farm Manager

## Configuración del Entorno de Desarrollo

### Requisitos
- Python 3.9+
- Git
- Entorno virtual (venv o conda)

### Configuración Inicial

```bash
# Clonar el repositorio
git clone https://github.com/tu-organizacion/farm-manager.git
cd farm-manager

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias de desarrollo
pip install -r requirements.txt
pip install -e .[dev]
```

## Estructura del Proyecto

```
farm-manager/
│
├── farm_manager/
│   ├── core/
│   ├── workflows/
│   ├── irrigation/
│   ├── weather/
│   └── resources/
│
├── tests/
├── docs/
├── setup.py
└── requirements.txt
```

## Desarrollo de Nuevos Módulos

### Pasos para Agregar un Nuevo Módulo

1. Crear directorio en `farm_manager/`
2. Implementar clases base
3. Añadir pruebas unitarias
4. Actualizar documentación

### Ejemplo de Estructura de Módulo

```python
# farm_manager/nuevo_modulo/__init__.py
from .base import BaseClase
from .implementacion import ClaseEspecifica

__all__ = ['BaseClase', 'ClaseEspecifica']

# farm_manager/nuevo_modulo/base.py
from abc import ABC, abstractmethod

class BaseClase(ABC):
    @abstractmethod
    def metodo_principal(self):
        """Método abstracto a implementar"""
        pass

# farm_manager/nuevo_modulo/implementacion.py
from .base import BaseClase

class ClaseEspecifica(BaseClase):
    def metodo_principal(self):
        """Implementación concreta"""
        pass
```

## Pruebas

### Ejecución de Pruebas

```bash
# Ejecutar todas las pruebas
pytest tests/

# Ejecutar pruebas con cobertura
pytest --cov=farm_manager tests/

# Ejecutar pruebas para un módulo específico
pytest tests/test_nuevo_modulo.py
```

### Escribiendo Pruebas

- Usar `pytest`
- Crear archivos de prueba en el directorio `tests/`
- Usar fixtures para preparar datos de prueba
- Cubrir casos de éxito y error

## Estilo de Código

- Seguir PEP 8
- Usar type hints
- Documentar funciones y clases
- Usar docstrings descriptivos

### Ejemplo de Docstring

```python
def calcular_riego(cultivo: str, area: float) -> Dict[str, Any]:
    """
    Calcula el plan de riego para un cultivo específico.

    Args:
        cultivo (str): Tipo de cultivo
        area (float): Área en hectáreas

    Returns:
        Dict[str, Any]: Plan de riego detallado

    Raises:
        ValueError: Si el área es inválida
    """
    pass
```

## Integración Continua

- Configuración en `.github/workflows/ci.yml`
- Pruebas en múltiples versiones de Python
- Verificación de cobertura de código
- Linting con flake8 y black

## Publicación

```bash
# Construir paquete
python setup.py sdist bdist_wheel

# Publicar en PyPI
twine upload dist/*
```

## Contribuciones

### Proceso de Contribución

1. Fork del repositorio
2. Crear rama de características
3. Implementar cambios
4. Escribir pruebas
5. Ejecutar pruebas localmente
6. Crear Pull Request

### Guía de Estilo

- Código claro y legible
- Comentarios explicativos
- Pruebas exhaustivas
- Documentación actualizada

## Herramientas Recomendadas

- VSCode o PyCharm
- Black para formateo
- Mypy para type checking
- Pre-commit hooks

## Solución de Problemas

- Verificar versiones de dependencias
- Usar entorno virtual
- Consultar issues en GitHub
- Contactar mantenedores

## Recursos Adicionales

- Documentación de Python
- Documentación de librerías utilizadas
- Comunidad de desarrollo agrícola
