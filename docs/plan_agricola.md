z# Plan de Desarrollo: Asistente de Gestión Agrícola

Este documento detalla el plan de desarrollo para un asistente de gestión agrícola, organizado en tareas secuenciales de menor a mayor complejidad. Cada tarea incluye criterios de prueba para verificar su correcta implementación.

## Instrucciones de Uso

- Utiliza las cajas de verificación `[ ]` para marcar el progreso de cada tarea
- Cuando una tarea esté completada, marca la caja con una X: `[X]`
- Sigue las instrucciones específicas para completar cada tarea exitosamente

## FASE 1: AGENTE ÚNICO DE PLANIFICACIÓN CENTRAL

### 1.1 Configuración del Entorno de Desarrollo

- [X] **Tarea**: Configurar entorno Python con venv y dependencias iniciales
- **Complejidad**: Baja
- **Prueba**: Verificar activación automática del entorno al entrar al directorio y persistencia entre sesiones
- **Instrucciones para LLM**:
  1. Crear directorio del proyecto y entrar en él
  2. Ejecutar `python -m venv venv` para crear el entorno virtual
  3. Configurar activación automática mediante hooks en `.bashrc` o `.zshrc`
  4. Crear `requirements.txt` con dependencias iniciales (langchain, langgraph, chromadb)
  5. Instalar dependencias con `pip install -r requirements.txt`
  6. Verificar que el entorno se active automáticamente al entrar al directorio

### 1.2 Modelo de Datos Básico

- [X] **Tarea**: Diseñar e implementar esquema de datos para personal, maquinaria y terrenos
- **Complejidad**: Baja
- **Prueba**: Validar operaciones CRUD básicas sobre cada entidad del modelo
- **Instrucciones para LLM**:
  1. Diseñar esquemas para entidades principales (personal, maquinaria, terrenos)
  2. Implementar clases con Pydantic para validación de datos
  3. Crear funciones para operaciones CRUD básicas
  4. Implementar sistema de persistencia (inicialmente con archivos JSON)
  5. Escribir pruebas unitarias para validar operaciones CRUD
  6. Documentar el modelo de datos y sus relaciones

### 1.3 Implementación de LangGraph Base

- [X] **Tarea**: Configurar estructura básica de LangGraph para flujos de trabajo
- **Complejidad**: Media
- **Prueba**: Ejecutar un flujo de trabajo simple que complete un ciclo completo
- **Instrucciones para LLM**:
  1. Definir nodos básicos para el grafo (planificación, asignación, verificación)
  2. Implementar estados y transiciones entre nodos
  3. Configurar LLM para cada nodo (usando OpenAI o modelo local)
  4. Crear un flujo de trabajo simple para prueba de concepto
  5. Implementar mecanismos de persistencia de estado
  6. Documentar la estructura del grafo y sus componentes

### 1.4 Flujos de Trabajo Predefinidos

- [x] **Tarea**: Implementar plantillas para operaciones agrícolas comunes (En Progreso)
  - Implementado sistema base de plantillas de flujo de trabajo
  - Creada plantilla inicial para operaciones de plantación
  - Desarrollado sistema de generación y validación de planes
  - Documentación detallada en README.md y NOTES.md
- **Complejidad**: Media
- **Prueba**: Verificar que cada plantilla genera un plan coherente y completo
- **Instrucciones para LLM**:
  1. Identificar operaciones agrícolas comunes para la región
  2. Diseñar plantillas parametrizables para cada operación
  3. Implementar sistema de selección de plantilla según contexto
  4. Crear mecanismo para personalizar plantillas según necesidades específicas
  5. Desarrollar sistema de validación para planes generados
  6. Probar cada plantilla con diferentes parámetros y verificar coherencia

### 1.5 Base de Conocimiento Regional

- [x] **Tarea**: Recopilar y estructurar información técnica para región de Los Ríos (En Progreso)
  - Implementado sistema de base de conocimiento con ChromaDB
  - Creadas colecciones para cultivos, clima y prácticas agrícolas
  - Añadida información inicial para Avellano Europeo y Ballica Perenne
  - Desarrolladas funciones de consulta semántica
  - Documentación detallada en NOTES.md
- **Complejidad**: Media
- **Prueba**: Consultar información específica y validar precisión con expertos locales
- **Instrucciones para LLM**:
  1. Recopilar información sobre cultivos locales (Avellano Europeo, Praderas de Ballicas, Praderas naturales mejoradas, Paja, Heno, fardos), condiciones climáticas y prácticas agrícolas
  2. Estructurar datos en formato adecuado para vectorización
  3. Implementar base de conocimiento con ChromaDB
  4. Crear funciones de consulta para recuperar información relevante
  5. Desarrollar sistema de actualización de la base de conocimiento
  6. Validar precisión de la información con expertos agrícolas locales

### 1.6 Calendarios Agrícolas Locales

- [x] **Tarea**: Implementar sistema de calendarios para cultivos locales (En Progreso)
  - Desarrollado sistema de calendarios agrícolas
  - Implementada clase CropCalendar para Avellano Europeo
  - Creadas funciones para:
    * Determinar etapa actual del cultivo
    * Obtener calendario completo
    * Recuperar acciones recomendadas
  - Documentación detallada en NOTES.md
- **Complejidad**: Media
- **Prueba**: Verificar recomendaciones temporales para avellana europea
- **Instrucciones para LLM**:
  1. Recopilar información sobre ciclos de cultivo para especies locales
  2. Diseñar estructura de datos para calendarios agrícolas
  3. Implementar sistema de consulta por cultivo y fecha
  4. Crear visualizaciones de calendarios para facilitar comprensión
  5. Desarrollar sistema de alertas basado en fechas clave
  6. Validar recomendaciones temporales con casos de prueba específicos

### 1.7 Integración de Normativa Chilena

- [x] **Tarea**: Incorporar normativa agrícola relevante en la base de conocimiento (Completada)
  - Implementado sistema de almacenamiento de normativas
  - Añadidas normativas iniciales:
    * Ley de Protección Fitosanitaria (SAG)
    * Normativa de Uso de Agroquímicos (MINAGRI)
  - Creadas funciones para:
    * Agregar normativas a la base de conocimiento
    * Consultar normativas por palabras clave
  - Implementada versión alternativa (mock_regional_knowledge_base.py) para compatibilidad con Python 3.13
  - Documentación de funcionalidades en código fuente
- **Complejidad**: Alta
- **Prueba**: Validar que las recomendaciones cumplen con la normativa vigente
- **Instrucciones para LLM**:
  1. Recopilar normativa agrícola chilena relevante (SAG, INDAP, etc.)
  2. Estructurar información normativa en formato consultable
  3. Integrar normativa en la base de conocimiento
  4. Implementar sistema de verificación de cumplimiento normativo
  5. Crear mecanismo de actualización ante cambios normativos
  6. Validar que las recomendaciones del sistema cumplen con la normativa

## FASE 2: MÓDULOS FUNCIONALES ESPECÍFICOS

### 2.1 Conexión Básica a APIs Meteorológicas

- [x] **Tarea**: Implementar cliente para consumir datos de APIs meteorológicas chilenas (Completada)
  - Implementado cliente ChileanWeatherClient para consumir datos de AgroMonitoring API
  - Añadido soporte para las 16 regiones de Chile con coordenadas específicas
  - Creadas funciones para normalizar datos meteorológicos (temperatura en °C, humedad, viento)
  - Implementado sistema de caché local con TTLCache para optimizar consultas
  - Desarrollado estructura para sistema de alertas meteorológicas
  - Validado con pruebas exitosas para múltiples regiones
- **Complejidad**: Baja
- **Prueba**: Obtener y mostrar datos meteorológicos actuales para la región
- **Instrucciones para LLM**:
  1. Identificar APIs meteorológicas disponibles para Chile
  2. Implementar cliente HTTP para consumir datos
  3. Crear funciones para parsear y normalizar datos meteorológicos
  4. Implementar caché local para optimizar consultas
  5. Desarrollar sistema de alertas basado en condiciones meteorológicas
  6. Validar precisión de datos comparando con fuentes oficiales

### 2.2 Sistema de Seguimiento de Recursos

- [x] **Tarea**: Desarrollar interfaz básica para registro de maquinaria y personal
- **Complejidad**: Baja
- **Estado**: Completado
- **Detalles de Implementación**:
  - Implementado sistema completo en `src/resource_management.py`
  - Creadas clases `Machinery` y `Personnel` para modelado de recursos
  - Desarrollada clase `ResourceManager` para gestión centralizada
  - Implementado CLI completo con subcomandos para todas las operaciones
  - Añadido sistema de persistencia en JSON para datos de recursos
  - Implementado registro de actividad (usage_log) para seguimiento
- **Funcionalidades Principales**:
  - Registro y actualización de maquinaria y personal
  - Consultas por tipo, habilidad y departamento
  - Asignación de recursos a tareas
  - Seguimiento de estado y mantenimiento
  - Generación de reportes de utilización
- **Pruebas Realizadas**:
  - Verificación de registro y actualización de recursos
  - Validación de consultas y filtros
  - Comprobación de generación de reportes

### 2.3 Algoritmos de Decisión para Riego

- [x] **Tarea**: Implementar lógica para recomendaciones de riego basadas en condiciones actuales
- **Complejidad**: Media
- **Estado**: Completado
- **Detalles de Implementación**:
  - Desarrollado sistema de decisión de riego en `src/irrigation_decision_system.py`
  - Implementado modelo de machine learning con RandomForestRegressor
  - Integrado con ChileanWeatherClient y RegionalKnowledgeBase
  - Creado sistema de recomendaciones con múltiples niveles de detalle
  - Añadido mecanismo de retroalimentación y aprendizaje
- **Funcionalidades Principales**:
  - Análisis de condiciones climáticas
  - Consideración de tipo de suelo y etapa del cultivo
  - Generación de recomendaciones con justificación detallada
  - Niveles de riego: Mínimo, Moderado e Intensivo
  - Cálculo de confianza de recomendaciones
- **Pruebas Realizadas**:
  - Validación de recomendaciones para diferentes cultivos
  - Verificación de integración con fuentes de datos externas
  - Pruebas de mecanismo de retroalimentación y aprendizaje

### 2.4 Optimización de Uso de Maquinaria

- [x] **Tarea**: Desarrollar algoritmo para asignación eficiente de maquinaria
- **Complejidad**: Media
- **Estado**: Completado
- **Detalles de Implementación**:
  - Creado sistema de optimización de maquinaria en `src/resource_management.py`
  - Implementado `ResourceOptimizer` con métodos de cálculo de eficiencia de maquinaria
  - Desarrollado algoritmo de asignación basado en:
    * Prioridad de tareas
    * Eficiencia de maquinaria
    * Disponibilidad de recursos
  - Creados métodos para resolución de conflictos de asignación
  - Implementadas pruebas unitarias en `test_machinery_optimization.py`
  - Añadida documentación en README.md
- **Funcionalidades Principales**:
  - Cálculo de eficiencia de maquinaria considerando:
    * Tipo de máquina
    * Historial de mantenimiento
    * Estado actual
    * Edad de la máquina
  - Asignación de maquinaria basada en prioridades
  - Sistema de resolución de conflictos de asignación
- **Pruebas Realizadas**:
  - Verificación de cálculo de eficiencia de maquinaria
  - Validación de asignación óptima de recursos
  - Pruebas de resolución de conflictos en escenarios complejos

### 2.5 Sistema de Mantenimiento Predictivo

- [ ] **Tarea**: Implementar seguimiento y predicción de mantenimiento para maquinaria
- **Complejidad**: Media
- **Prueba**: Validar alertas anticipadas para mantenimiento basadas en uso
- **Instrucciones para LLM**:
  1. Diseñar modelo de datos para registro de mantenimiento
  2. Implementar sistema de seguimiento de horas/uso de maquinaria
  3. Desarrollar algoritmo predictivo basado en patrones de uso
  4. Crear sistema de alertas para mantenimiento preventivo
  5. Implementar registro de mantenimientos realizados
  6. Validar precisión de predicciones con datos históricos

### 2.6 Asignación de Personal por Competencias

- [ ] **Tarea**: Desarrollar sistema que asigne personal según habilidades requeridas
- **Complejidad**: Alta
- **Prueba**: Verificar asignaciones óptimas en diferentes escenarios de trabajo
- **Instrucciones para LLM**:
  1. Diseñar modelo de competencias para personal agrícola
  2. Implementar sistema de registro y validación de habilidades
  3. Desarrollar algoritmo de matching entre tareas y competencias
  4. Crear mecanismo de priorización basado en experiencia y eficiencia
  5. Implementar sistema de retroalimentación sobre desempeño
  6. Validar asignaciones en escenarios complejos con múltiples restricciones

### 2.7 Verificación de Seguridad y Cumplimiento

- [ ] **Tarea**: Implementar sistema de verificación de EPP y requisitos de seguridad
- **Complejidad**: Alta
- **Prueba**: Validar detección de incumplimientos y generación de alertas apropiadas
- **Instrucciones para LLM**:
  1. Recopilar normativa de seguridad agrícola aplicable
  2. Diseñar sistema de verificación de equipos de protección personal
  3. Implementar listas de verificación por tipo de tarea
  4. Desarrollar sistema de alertas ante incumplimientos
  5. Crear registro de incidentes y medidas correctivas
  6. Validar efectividad del sistema con simulaciones de incumplimiento

## FASE 3: SISTEMA DE COMUNICACIÓN

### 3.1 Notificaciones Básicas

- [ ] **Tarea**: Implementar sistema de generación de mensajes para diferentes eventos
- **Complejidad**: Baja
- **Prueba**: Verificar formato y contenido de mensajes para diferentes tipos de alertas
- **Instrucciones para LLM**:
  1. Diseñar estructura de mensajes para diferentes tipos de eventos
  2. Implementar sistema de plantillas de mensajes personalizables
  3. Crear mecanismo de priorización de notificaciones
  4. Desarrollar sistema de registro de mensajes enviados
  5. Implementar canales de notificación (consola, archivo, etc.)
  6. Validar claridad y utilidad de los mensajes generados

### 3.2 Integración con WhatsApp (API Básica)

- [ ] **Tarea**: Configurar conexión con API de WhatsApp Business
- **Complejidad**: Media
- **Prueba**: Enviar y recibir mensajes de prueba a través de la plataforma
- **Instrucciones para LLM**:
  1. Registrar cuenta en WhatsApp Business API
  2. Configurar credenciales y permisos necesarios
  3. Implementar cliente para envío de mensajes
  4. Desarrollar webhook para recepción de mensajes
  5. Crear sistema de manejo de errores y reintentos
  6. Validar comunicación bidireccional con mensajes de prueba

### 3.3 Notificaciones Diarias de Tareas

- [ ] **Tarea**: Implementar sistema automatizado de envío de tareas diarias
- **Complejidad**: Media
- **Prueba**: Verificar envío puntual y contenido correcto de las notificaciones
- **Instrucciones para LLM**:
  1. Diseñar formato de notificación diaria de tareas
  2. Implementar sistema de programación de envíos
  3. Desarrollar mecanismo de generación de contenido personalizado
  4. Crear sistema de confirmación de recepción
  5. Implementar registro de notificaciones enviadas
  6. Validar puntualidad y contenido de las notificaciones

### 3.4 Sistema de Consultas vía Mensajería

- [ ] **Tarea**: Desarrollar parser para interpretar consultas simples por WhatsApp
- **Complejidad**: Alta
- **Prueba**: Procesar correctamente diferentes tipos de consultas y generar respuestas apropiadas
- **Instrucciones para LLM**:
  1. Diseñar gramática para consultas vía mensajería
  2. Implementar parser para interpretar mensajes entrantes
  3. Desarrollar sistema de resolución de ambigüedades
  4. Crear mecanismo de generación de respuestas contextuales
  5. Implementar sistema de ayuda y ejemplos de uso
  6. Validar precisión de interpretación con diversos tipos de consultas

### 3.5 Integración con Google Calendar

- [ ] **Tarea**: Implementar sincronización bidireccional con Google Calendar
- **Complejidad**: Alta
- **Prueba**: Verificar que eventos creados en ambos sistemas se sincronizan correctamente
- **Instrucciones para LLM**:
  1. Configurar proyecto en Google Cloud y habilitar API de Calendar
  2. Implementar autenticación OAuth para acceso a calendarios
  3. Desarrollar sistema de creación de eventos desde la aplicación
  4. Crear mecanismo de sincronización de eventos modificados
  5. Implementar manejo de conflictos entre sistemas
  6. Validar sincronización bidireccional con diversos escenarios

## FASE 4: ANÁLISIS Y APRENDIZAJE

### 4.1 Almacenamiento de Decisiones

- [ ] **Tarea**: Implementar sistema para registrar decisiones tomadas
- **Complejidad**: Baja
- **Prueba**: Verificar que las decisiones se almacenan con metadatos relevantes
- **Instrucciones para LLM**:
  1. Diseñar esquema de datos para registro de decisiones
  2. Implementar sistema de captura automática de decisiones
  3. Desarrollar mecanismo de etiquetado y categorización
  4. Crear sistema de consulta de decisiones históricas
  5. Implementar exportación de decisiones para análisis
  6. Validar completitud de metadatos en decisiones registradas

### 4.2 Reportes Operativos Básicos

- [ ] **Tarea**: Desarrollar generación de informes simples sobre operaciones
- **Complejidad**: Media
- **Prueba**: Validar que los informes contienen información precisa y relevante
- **Instrucciones para LLM**:
  1. Diseñar estructura de reportes operativos
  2. Implementar generación automática de informes diarios/semanales
  3. Desarrollar visualizaciones para datos clave
  4. Crear sistema de distribución de reportes
  5. Implementar personalización de contenido según destinatario
  6. Validar precisión y relevancia de la información presentada

### 4.3 Seguimiento de KPIs Agrícolas

- [ ] **Tarea**: Implementar sistema de métricas para operaciones agrícolas
- **Complejidad**: Media
- **Prueba**: Verificar cálculo correcto de indicadores clave en diferentes escenarios
- **Instrucciones para LLM**:
  1. Identificar KPIs relevantes para operaciones agrícolas locales
  2. Diseñar sistema de recolección de datos para métricas
  3. Implementar cálculo automático de indicadores
  4. Desarrollar visualizaciones de evolución temporal
  5. Crear sistema de alertas basado en umbrales de KPIs
  6. Validar precisión de cálculos con datos de prueba

### 4.4 Sistema de Retroalimentación

- [ ] **Tarea**: Desarrollar mecanismo para capturar feedback del supervisor
- **Complejidad**: Media
- **Prueba**: Validar que el feedback se registra y asocia correctamente a las recomendaciones
- **Instrucciones para LLM**:
  1. Diseñar interfaz para captura de retroalimentación
  2. Implementar sistema de calificación de recomendaciones
  3. Desarrollar mecanismo para comentarios detallados
  4. Crear sistema de asociación entre feedback y decisiones
  5. Implementar análisis de sentimiento en comentarios
  6. Validar correcta asociación entre feedback y recomendaciones

### 4.5 Ajuste de Recomendaciones por Historial

- [ ] **Tarea**: Implementar algoritmo de aprendizaje basado en decisiones pasadas
- **Complejidad**: Alta
- **Prueba**: Demostrar mejora en recomendaciones basadas en historial de decisiones
- **Instrucciones para LLM**:
  1. Diseñar modelo de aprendizaje basado en retroalimentación
  2. Implementar sistema de ponderación de decisiones históricas
  3. Desarrollar mecanismo de ajuste de parámetros según feedback
  4. Crear sistema de evaluación de mejora continua
  5. Implementar pruebas A/B para validar ajustes
  6. Demostrar mejora cuantificable en precisión de recomendaciones

### 4.6 Análisis Comparativo de Temporadas

- [ ] **Tarea**: Desarrollar sistema de comparación entre diferentes temporadas agrícolas
- **Complejidad**: Alta
- **Prueba**: Verificar identificación correcta de patrones y anomalías entre temporadas
- **Instrucciones para LLM**:
  1. Diseñar modelo de datos para comparación interanual
  2. Implementar normalización de datos entre temporadas
  3. Desarrollar algoritmos de detección de patrones y anomalías
  4. Crear visualizaciones comparativas entre temporadas
  5. Implementar sistema de recomendaciones basado en análisis histórico
  6. Validar precisión en identificación de patrones con datos reales

## IMPLEMENTACIÓN TÉCNICA

### Infraestructura Base

- [ ] **Tarea**: Configurar PostgreSQL y Chroma para almacenamiento
- **Complejidad**: Media
- **Prueba**: Verificar operaciones de lectura/escritura y rendimiento con volumen de datos realista
- **Instrucciones para LLM**:
  1. Instalar y configurar PostgreSQL para datos estructurados
  2. Configurar ChromaDB para almacenamiento vectorial
  3. Implementar esquemas de base de datos relacional
  4. Desarrollar capa de abstracción para acceso a datos
  5. Crear scripts de migración y respaldo
  6. Realizar pruebas de rendimiento con volúmenes realistas

### Despliegue Local

- [ ] **Tarea**: Configurar entorno de ejecución local para desarrollo y pruebas
- **Complejidad**: Media
- **Prueba**: Validar funcionamiento completo en entorno local controlado
- **Instrucciones para LLM**:
  1. Configurar entorno de desarrollo con dependencias completas
  2. Implementar scripts de inicialización de servicios
  3. Desarrollar documentación de instalación paso a paso
  4. Crear conjunto de datos de prueba representativos
  5. Implementar scripts de verificación de instalación
  6. Validar funcionamiento en diferentes entornos locales

### Containerización

- [ ] **Tarea**: Preparar sistema para despliegue containerizado
- **Complejidad**: Alta
- **Prueba**: Verificar funcionamiento correcto en entorno containerizado con persistencia de datos
  6. Validar funcionamiento completo en entorno Docker
