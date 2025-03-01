import logging
from src.irrigation_decision_system import IrrigationDecisionSystem

def test_irrigation_recommendations():
    """
    Prueba del Sistema de Decisión de Riego para diferentes escenarios climáticos
    """
    logging.basicConfig(level=logging.INFO)
    
    # Instanciar el sistema de decisión de riego
    irrigation_system = IrrigationDecisionSystem()
    
    # Escenarios de prueba
    test_scenarios = [
        {
            'name': 'Escenario 1: Condiciones de Estrés Alto',
            'crop': 'Avellano Europeo',
            'weather': {
                'temperature': 35,  # Temperatura muy alta
                'humidity': 20,     # Humedad muy baja
            },
            'soil_type': 'sandy',   # Suelo arenoso (retiene menos agua)
            'crop_stage': 'desarrollo_fruto'  # Etapa crítica de desarrollo
        },
        {
            'name': 'Escenario 2: Condiciones de Estrés Moderado',
            'crop': 'Avellano Europeo',
            'weather': {
                'temperature': 28,  # Temperatura moderadamente alta
                'humidity': 35,     # Humedad baja
            },
            'soil_type': 'loam',    # Suelo franco
            'crop_stage': 'floracion'  # Etapa de floración
        },
        {
            'name': 'Escenario 3: Condiciones Favorables',
            'crop': 'Avellano Europeo',
            'weather': {
                'temperature': 22,  # Temperatura moderada
                'humidity': 55,     # Humedad adecuada
            },
            'soil_type': 'clay',    # Suelo arcilloso (retiene más agua)
            'crop_stage': 'dormancia'  # Etapa de reposo
        },
        {
            'name': 'Escenario 4: Condiciones Extremas',
            'crop': 'Avellano Europeo',
            'weather': {
                'temperature': 38,  # Temperatura extrema
                'humidity': 15,     # Humedad muy baja
            },
            'soil_type': 'sandy',   # Suelo arenoso
            'crop_stage': 'cuaja'   # Etapa de formación de frutos
        }
    ]
    
    # Realizar pruebas para cada escenario
    print("PRUEBA DE SISTEMA DE DECISIÓN DE RIEGO\n")
    for scenario in test_scenarios:
        print(f"{scenario['name']}")
        print("-" * 50)
        
        # Generar recomendación de riego
        recommendation = irrigation_system.generate_irrigation_recommendation(
            crop_name=scenario['crop'],
            current_weather=scenario['weather'],
            soil_type=scenario['soil_type'],
            crop_stage=scenario['crop_stage']
        )
        
        # Imprimir detalles de la recomendación
        for key, value in recommendation.items():
            print(f"{key.capitalize()}: {value}")
        
        # Validar la recomendación
        validation = irrigation_system.validate_recommendation(recommendation)
        print("\nValidación de la Recomendación:")
        for key, value in validation.items():
            print(f"{key.capitalize()}: {value}")
        
        print("\n")

def simulate_feedback():
    """
    Simula retroalimentación para los escenarios de prueba
    """
    irrigation_system = IrrigationDecisionSystem()
    
    # Escenarios de prueba con resultados simulados
    test_scenarios = [
        {
            'crop': 'Avellano Europeo',
            'recommendation': {
                'recommendation': 'Riego Intensivo',
                'water_volume': 'Alto',
                'confidence': 0.9
            },
            'actual_outcome': {
                'success': True,
                'crop_health': 'Excelente',
                'water_saved': 0.2  # 20% de agua ahorrada
            }
        },
        {
            'crop': 'Avellano Europeo',
            'recommendation': {
                'recommendation': 'Riego Moderado',
                'water_volume': 'Medio',
                'confidence': 0.7
            },
            'actual_outcome': {
                'success': False,
                'crop_health': 'Regular',
                'water_saved': -0.1  # 10% más de agua usada
            }
        }
    ]
    
    print("PRUEBA DE RETROALIMENTACIÓN\n")
    for scenario in test_scenarios:
        print(f"Registro de Retroalimentación para {scenario['crop']}")
        print("-" * 50)
        
        # Registrar retroalimentación
        irrigation_system.log_irrigation_feedback(
            crop_name=scenario['crop'],
            recommendation=scenario['recommendation'],
            actual_outcome=scenario['actual_outcome']
        )
        
        print("\n")

if __name__ == "__main__":
    test_irrigation_recommendations()
    simulate_feedback()
