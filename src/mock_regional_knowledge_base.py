import os
from typing import List, Dict, Any

class MockRegionalKnowledgeBase:
    """
    A mock implementation of the RegionalKnowledgeBase that doesn't rely on ChromaDB.
    This is used to demonstrate the functionality without the compatibility issues.
    """
    
    def __init__(self, persist_directory: str = 'knowledge_base'):
        """
        Initialize the mock knowledge base.
        
        :param persist_directory: Directory to persist the knowledge base (not used in mock)
        """
        # Initialize empty collections
        self.crops = []
        self.climate = []
        self.practices = []
        self.regulations = []
        
        # Populate with initial data
        self._populate_initial_data()
    
    def _populate_initial_data(self):
        """Populate the mock knowledge base with initial data."""
        # Add crop knowledge
        crops = [
            {
                'id': 'avellano_europeo_1',
                'name': 'Avellano Europeo',
                'type': 'Frutal',
                'growing_conditions': 'Requiere suelos bien drenados, pH entre 5.5 y 6.5',
                'soil_requirements': 'Suelos francos, ricos en materia orgánica',
                'climate_adaptation': 'Adaptado a climas templados húmedos de la región de Los Ríos'
            },
            {
                'id': 'ballica_perenne_1',
                'name': 'Ballica Perenne',
                'type': 'Pradera',
                'growing_conditions': 'Tolera diversos tipos de suelo, prefiere suelos húmedos',
                'soil_requirements': 'Adaptable a suelos francos y arcillosos',
                'climate_adaptation': 'Excelente adaptación a climas fríos y húmedos de la región'
            }
        ]
        
        for crop in crops:
            self.add_crop_knowledge(crop)
        
        # Add climate knowledge
        climate_data = [
            {
                'id': 'invierno_1',
                'season': 'Invierno',
                'avg_temperature': '6-10°C',
                'precipitation': 'Alta, entre 2000-3000 mm anuales',
                'wind_patterns': 'Vientos del oeste, frecuentes y moderados',
                'frost_risk': 'Alto, especialmente en zonas altas'
            },
            {
                'id': 'verano_1',
                'season': 'Verano',
                'avg_temperature': '12-18°C',
                'precipitation': 'Menor, pero aún significativa',
                'wind_patterns': 'Vientos más suaves, predominio de brisas',
                'frost_risk': 'Bajo'
            }
        ]
        
        for climate in climate_data:
            self.add_climate_knowledge(climate)
        
        # Add agricultural practices
        practices = [
            {
                'id': 'manejo_praderas_1',
                'name': 'Manejo de Praderas',
                'type': 'Producción Ganadera',
                'description': 'Técnicas para mantener y mejorar praderas en la región',
                'best_practices': 'Rotación de potreros, fertilización orgánica, control de malezas',
                'challenges': 'Alta humedad, riesgo de compactación de suelos'
            },
            {
                'id': 'cultivo_avellanos_1',
                'name': 'Cultivo de Avellanos',
                'type': 'Fruticultura',
                'description': 'Técnicas específicas para el cultivo de avellanos en Los Ríos',
                'best_practices': 'Poda de formación, control de plagas, riego tecnificado',
                'challenges': 'Condiciones climáticas variables, riesgo de heladas'
            }
        ]
        
        for practice in practices:
            self.add_agricultural_practice(practice)
        
        # Add regulations
        regulations = [
            {
                'id': 'ley_fitosanitaria_1',
                'name': 'Ley de Protección Fitosanitaria',
                'authority': 'SAG (Servicio Agrícola y Ganadero)',
                'type': 'Fitosanidad',
                'year': 2020,
                'description': 'Regulaciones para prevenir la propagación de plagas y enfermedades en cultivos',
                'key_requirements': 'Registro de tratamientos fitosanitarios, control de movimiento de plantas',
                'compliance_criteria': 'Documentación de tratamientos, inspecciones periódicas'
            },
            {
                'id': 'normativa_agroquimicos_1',
                'name': 'Normativa de Uso de Agroquímicos',
                'authority': 'MINAGRI (Ministerio de Agricultura)',
                'type': 'Regulación Ambiental',
                'year': 2018,
                'description': 'Regulaciones para el uso responsable de productos químicos en agricultura',
                'key_requirements': 'Certificación de aplicadores, límites de residuos en cultivos',
                'compliance_criteria': 'Registro de aplicaciones, capacitación en manejo de agroquímicos'
            }
        ]
        
        for regulation in regulations:
            self.add_regulation(regulation)
    
    def add_crop_knowledge(self, crop_data: Dict[str, Any]):
        """
        Add knowledge about a specific crop to the knowledge base.
        
        :param crop_data: Dictionary containing crop information
        """
        # Create a document representation for display
        crop_data['document'] = f"""
        Crop: {crop_data.get('name', '')}
        Type: {crop_data.get('type', '')}
        Growing Conditions: {crop_data.get('growing_conditions', '')}
        Soil Requirements: {crop_data.get('soil_requirements', '')}
        Climate Adaptation: {crop_data.get('climate_adaptation', '')}
        """
        
        # Add metadata for querying
        crop_data['metadata'] = {
            'name': crop_data.get('name', ''),
            'type': crop_data.get('type', ''),
            'region': 'Los Ríos'
        }
        
        self.crops.append(crop_data)
    
    def add_climate_knowledge(self, climate_data: Dict[str, Any]):
        """
        Add climate-related knowledge for the region.
        
        :param climate_data: Dictionary containing climate information
        """
        # Create a document representation for display
        climate_data['document'] = f"""
        Season: {climate_data.get('season', '')}
        Average Temperature: {climate_data.get('avg_temperature', '')}
        Precipitation: {climate_data.get('precipitation', '')}
        Wind Patterns: {climate_data.get('wind_patterns', '')}
        Frost Risk: {climate_data.get('frost_risk', '')}
        """
        
        # Add metadata for querying
        climate_data['metadata'] = {
            'season': climate_data.get('season', ''),
            'region': 'Los Ríos'
        }
        
        self.climate.append(climate_data)
    
    def add_agricultural_practice(self, practice_data: Dict[str, Any]):
        """
        Add knowledge about agricultural practices.
        
        :param practice_data: Dictionary containing practice information
        """
        # Create a document representation for display
        practice_data['document'] = f"""
        Practice: {practice_data.get('name', '')}
        Type: {practice_data.get('type', '')}
        Description: {practice_data.get('description', '')}
        Best Practices: {practice_data.get('best_practices', '')}
        Challenges: {practice_data.get('challenges', '')}
        """
        
        # Add metadata for querying
        practice_data['metadata'] = {
            'name': practice_data.get('name', ''),
            'type': practice_data.get('type', ''),
            'region': 'Los Ríos'
        }
        
        self.practices.append(practice_data)
    
    def add_regulation(self, regulation_data: Dict[str, Any]):
        """
        Add agricultural regulatory information to the knowledge base.
        
        :param regulation_data: Dictionary containing regulatory information
        """
        # Create a document representation for display
        regulation_data['document'] = f"""
        Regulation: {regulation_data.get('name', '')}
        Authority: {regulation_data.get('authority', '')}
        Type: {regulation_data.get('type', '')}
        Description: {regulation_data.get('description', '')}
        Key Requirements: {regulation_data.get('key_requirements', '')}
        Compliance Criteria: {regulation_data.get('compliance_criteria', '')}
        """
        
        # Add metadata for querying
        regulation_data['metadata'] = {
            'authority': regulation_data.get('authority', ''),
            'type': regulation_data.get('type', ''),
            'year': regulation_data.get('year', '')
        }
        
        self.regulations.append(regulation_data)
    
    def _simple_search(self, collection, query, n_results=5):
        """
        Simple search function that checks if the query is in the document.
        
        :param collection: Collection to search in
        :param query: Search query
        :param n_results: Number of results to return
        :return: List of matching entries
        """
        results = []
        
        for item in collection:
            # Simple check if query is in document
            if query.lower() in item['document'].lower():
                # Add a mock distance score (lower is better)
                item['distance'] = 0.1
                results.append(item)
        
        # Sort by "relevance" and limit to n_results
        return results[:n_results]
    
    def query_crops(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """
        Query crop knowledge base.
        
        :param query: Search query
        :param n_results: Number of results to return
        :return: List of matching crop knowledge entries
        """
        return self._simple_search(self.crops, query, n_results)
    
    def query_climate(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """
        Query climate knowledge base.
        
        :param query: Search query
        :param n_results: Number of results to return
        :return: List of matching climate knowledge entries
        """
        return self._simple_search(self.climate, query, n_results)
    
    def query_practices(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """
        Query agricultural practices knowledge base.
        
        :param query: Search query
        :param n_results: Number of results to return
        :return: List of matching agricultural practice entries
        """
        return self._simple_search(self.practices, query, n_results)
    
    def query_regulations(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """
        Query agricultural regulations knowledge base.
        
        :param query: Search query
        :param n_results: Number of results to return
        :return: List of matching regulatory entries
        """
        return self._simple_search(self.regulations, query, n_results)


if __name__ == "__main__":
    # Create a mock knowledge base
    kb = MockRegionalKnowledgeBase()
    
    # Demonstrate querying capabilities
    print("Querying Crops:")
    crop_results = kb.query_crops("avellano")
    for result in crop_results:
        print(f"Crop Result: {result['metadata']['name']}")
        print(f"Document: {result['document']}\n")
    
    print("\nQuerying Climate:")
    climate_results = kb.query_climate("invierno")
    for result in climate_results:
        print(f"Climate Result: {result['metadata']['season']}")
        print(f"Document: {result['document']}\n")
    
    print("\nQuerying Practices:")
    practice_results = kb.query_practices("praderas")
    for result in practice_results:
        print(f"Practice Result: {result['metadata']['name']}")
        print(f"Document: {result['document']}\n")
    
    print("\nQuerying Regulations:")
    regulation_results = kb.query_regulations("fitosanitaria")
    for result in regulation_results:
        print(f"Regulation Result: {result['metadata']['authority']}")
        print(f"Document: {result['document']}\n")
