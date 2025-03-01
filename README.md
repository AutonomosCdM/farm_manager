# Farm Manager

## Descripción
Farm Manager es una herramienta integral de gestión agrícola que proporciona funcionalidades avanzadas para la planificación y optimización de operaciones agrícolas.

## Estructura del Proyecto

### Directorios de Datos
- `data/resources/`: Almacena archivos JSON de recursos de la granja
- `data/knowledge_base/`: Contiene la configuración y base de datos de gestión de conocimiento
- `data/backups/`: Copias de seguridad automatizadas de recursos y base de conocimientos

### Sistema de Respaldo
Un script de respaldo automatizado se ejecuta diariamente a medianoche, creando:
- Copias de seguridad con marca de tiempo de la base de datos SQLite de conocimientos
- Copias de seguridad completas de datos de recursos
- Rotación de respaldos para mantener un máximo de 7 copias recientes

### Control de Acceso
Control de acceso basado en roles implementado con los siguientes roles:
- `admin`: Permisos completos de lectura, escritura, eliminación y respaldo
- `researcher`: Acceso de solo lectura
- `viewer`: Acceso de solo lectura con permisos mínimos

## Instalación

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/farm-manager.git
cd farm-manager

# Crear y activar entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
pip install -e .
```

## Versionado

Este proyecto sigue el [Versionado Semántico 2.0.0](https://semver.org/lang/es/).

### Actualización de Versiones

Utilizamos un script de gestión de versiones para actualizar la versión del proyecto. Puedes incrementar la versión usando:

```bash
python scripts/version_manager.py [major|minor|patch]
```

- `major`: Para cambios incompatibles en la API
- `minor`: Para nuevas funcionalidades compatibles
- `patch`: Para correcciones de errores

Cada actualización de versión automáticamente:
- Actualiza la versión en `setup.py`
- Actualiza el `CHANGELOG.md`

### Historial de Cambios

Consulta el archivo `CHANGELOG.md` para ver el historial detallado de cambios en cada versión.

## Uso de la CLI

### Flujos de Trabajo
Generar planes de trabajo para diferentes operaciones agrícolas:

```bash
# Plan de plantación
farm-manager workflow --operation planting --crop-type avellano --area 5.5 --date 2025-07-15

# Plan de cosecha
farm-manager workflow --operation harvest --crop-type trigo --area 10.0 --date 2025-12-10

# Plan de mantenimiento
farm-manager workflow --operation maintenance --crop-type maíz --area 8.0 --date 2025-09-20
```

### Riego
Generar planes de riego para cultivos específicos:

```bash
# Plan de riego para trigo
farm-manager irrigate --crop trigo --area 10.0
```

### Clima
Obtener pronósticos meteorológicos:

```bash
# Pronóstico para Santiago por 3 días
farm-manager weather --location Santiago --days 3
```

### Recursos
Gestionar y optimizar recursos agrícolas:

```bash
# Listar recursos de maquinaria
farm-manager resources --action list --resource-type machinery

# Optimizar recursos de personal
farm-manager resources --action optimize --resource-type personnel
```

## Características Principales
- Generación de planes de trabajo para plantación, cosecha y mantenimiento
- Sistema de decisiones de riego
- Consulta de pronósticos meteorológicos
- Gestión y optimización de recursos
- Sistema de respaldo y persistencia de datos
- Control de acceso basado en roles

## Contribuciones
Las contribuciones son bienvenidas. Por favor, lee las pautas de contribución antes de enviar un pull request.

## Licencia
[Especificar la licencia del proyecto]
