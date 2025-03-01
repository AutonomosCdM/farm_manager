import os
from typing import List, Dict, Any
import chromadb
from chromadb.config import Settings
from pydantic import BaseModel, Field
import os
from typing import List, Dict, Any
import chromadb
from chromadb.config import Settings

class RegionalKnowledgeBase:
    """
    Manages a knowledge base for agricultural information in the Los Ríos region.
    Uses ChromaDB for vector storage and retrieval.
    """
    
    def __init__(self, persist_directory: str = 'knowledge_base'):
        """
        Initialize the knowledge base with ChromaDB.
        
        :param persist_directory: Directory to persist the knowledge base
        """
        # Ensure the persist directory exists
        os.makedirs(persist_directory, exist_ok=True)
        
        # Configure ChromaDB client
        self.chroma_client = chromadb.PersistentClient(path=persist_directory)
        
        # Create or get collections for different types of agricultural knowledge
        self.crops_collection = self._create_or_get_collection('crops')
        self.climate_collection = self._create_or_get_collection('climate')
        self.practices_collection = self._create_or_get_collection('agricultural_practices')
        self.regulations_collection = self._create_or_get_collection('agricultural_regulations')
    
    def _create_or_get_collection(self, collection_name: str):
        """
        Create or retrieve a ChromaDB collection.
        
        :param collection_name: Name of the collection
        :return: ChromaDB collection
        """
        return self.chroma_client.get_or_create_collection(name=collection_name)
    
    def add_crop_knowledge(self, crop_data: Dict[str, Any]):
        """
        Add knowledge about a specific crop to the knowledge base.
        
        :param crop_data: Dictionary containing crop information
        """
        # Generate a unique ID for the crop entry
        crop_id = f"{crop_data.get('name', 'unknown')}_{hash(frozenset(crop_data.items()))}"
        
        # Prepare metadata and embedding
        metadata = {
            'name': crop_data.get('name', ''),
            'type': crop_data.get('type', ''),
            'region': 'Los Ríos'
        }
        
        # Use a simple text representation for embedding
        document = f"""
        Crop: {crop_data.get('name', '')}
        Type: {crop_data.get('type', '')}
        Growing Conditions: {crop_data.get('growing_conditions', '')}
        Soil Requirements: {crop_data.get('soil_requirements', '')}
        Climate Adaptation: {crop_data.get('climate_adaptation', '')}
        """
        
        # Add to ChromaDB collection
        self.crops_collection.add(
            ids=[crop_id],
            documents=[document],
            metadatas=[metadata]
        )
    
    def add_climate_knowledge(self, climate_data: Dict[str, Any]):
        """
        Add climate-related knowledge for the region.
        
        :param climate_data: Dictionary containing climate information
        """
        climate_id = f"climate_{hash(frozenset(climate_data.items()))}"
        
        metadata = {
            'season': climate_data.get('season', ''),
            'region': 'Los Ríos'
        }
        
        document = f"""
        Season: {climate_data.get('season', '')}
        Average Temperature: {climate_data.get('avg_temperature', '')}
        Precipitation: {climate_data.get('precipitation', '')}
        Wind Patterns: {climate_data.get('wind_patterns', '')}
        Frost Risk: {climate_data.get('frost_risk', '')}
        """
        
        self.climate_collection.add(
            ids=[climate_id],
            documents=[document],
            metadatas=[metadata]
        )
    
    def add_agricultural_practice(self, practice_data: Dict[str, Any]):
        """
        Add knowledge about agricultural practices.
        
        :param practice_data: Dictionary containing practice information
        """
        practice_id = f"practice_{hash(frozenset(practice_data.items()))}"
        
        metadata = {
            'name': practice_data.get('name', ''),
            'type': practice_data.get('type', ''),
            'region': 'Los Ríos'
        }
        
        document = f"""
        Practice: {practice_data.get('name', '')}
        Type: {practice_data.get('type', '')}
        Description: {practice_data.get('description', '')}
        Best Practices: {practice_data.get('best_practices', '')}
        Challenges: {practice_data.get('challenges', '')}
        """
        
        self.practices_collection.add(
            ids=[practice_id],
            documents=[document],
            metadatas=[metadata]
        )
    
    def query_crops(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """
        Query crop knowledge base.
        
        :param query: Search query
        :param n_results: Number of results to return
        :return: List of matching crop knowledge entries
        """
        results = self.crops_collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        return [
            {
                'id': results['ids'][0][i],
                'document': results['documents'][0][i],
                'metadata': results['metadatas'][0][i],
                'distance': results['distances'][0][i]
            }
            for i in range(len(results['ids'][0]))
        ]
    
    def query_climate(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """
        Query climate knowledge base.
        
        :param query: Search query
        :param n_results: Number of results to return
        :return: List of matching climate knowledge entries
        """
        results = self.climate_collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        return [
            {
                'id': results['ids'][0][i],
                'document': results['documents'][0][i],
                'metadata': results['metadatas'][0][i],
                'distance': results['distances'][0][i]
            }
            for i in range(len(results['ids'][0]))
        ]
    
    def query_practices(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """
        Query agricultural practices knowledge base.
        
        :param query: Search query
        :param n_results: Number of results to return
        :return: List of matching agricultural practice entries
        """
        results = self.practices_collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        return [
            {
                'id': results['ids'][0][i],
                'document': results['documents'][0][i],
                'metadata': results['metadatas'][0][i],
                'distance': results['distances'][0][i]
            }
            for i in range(len(results['ids'][0]))
        ]
    
    def add_regulation(self, regulation_data: Dict[str, Any]):
        """
        Add agricultural regulatory information to the knowledge base.
        
        :param regulation_data: Dictionary containing regulatory information
        """
        regulation_id = f"regulation_{hash(frozenset(regulation_data.items()))}"
        
        metadata = {
            'authority': regulation_data.get('authority', ''),
            'type': regulation_data.get('type', ''),
            'year': regulation_data.get('year', '')
        }
        
        document = f"""
        Regulation: {regulation_data.get('name', '')}
        Authority: {regulation_data.get('authority', '')}
        Type: {regulation_data.get('type', '')}
        Description: {regulation_data.get('description', '')}
        Key Requirements: {regulation_data.get('key_requirements', '')}
        Compliance Criteria: {regulation_data.get('compliance_criteria', '')}
        """
        
        self.regulations_collection.add(
            ids=[regulation_id],
            documents=[document],
            metadatas=[metadata]
        )
    
    def query_regulations(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """
        Query agricultural regulations knowledge base.
        
        :param query: Search query
        :param n_results: Number of results to return
        :return: List of matching regulatory entries
        """
        results = self.regulations_collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        return [
            {
                'id': results['ids'][0][i],
                'document': results['documents'][0][i],
                'metadata': results['metadatas'][0][i],
                'distance': results['distances'][0][i]
            }
            for i in range(len(results['ids'][0]))
        ]

def populate_initial_knowledge_base():
    """
    Populate the knowledge base with initial information about Los Ríos region.
    """
    kb = RegionalKnowledgeBase()
    
    # Previous crop, climate, and practice population code remains the same
    
    # Add initial regulatory information
    regulations = [
        {
            'name': 'Ley de Protección Fitosanitaria',
            'authority': 'SAG (Servicio Agrícola y Ganadero)',
            'type': 'Fitosanidad',
            'year': 2020,
            'description': 'Regulaciones para prevenir la propagación de plagas y enfermedades en cultivos',
            'key_requirements': 'Registro de tratamientos fitosanitarios, control de movimiento de plantas',
            'compliance_criteria': 'Documentación de tratamientos, inspecciones periódicas'
        },
        {
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
        kb.add_regulation(regulation)

    """
    Populate the knowledge base with initial information about Los Ríos region.
    """
    kb = RegionalKnowledgeBase()
    
    # Add crop knowledge
    crops = [
        {
            'name': 'Avellano Europeo',
            'type': 'Frutal',
            'growing_conditions': 'Requiere suelos bien drenados, pH entre 5.5 y 6.5',
            'soil_requirements': 'Suelos francos, ricos en materia orgánica',
            'climate_adaptation': 'Adaptado a climas templados húmedos de la región de Los Ríos'
        },
        {
            'name': 'Ballica Perenne',
            'type': 'Pradera',
            'growing_conditions': 'Tolera diversos tipos de suelo, prefiere suelos húmedos',
            'soil_requirements': 'Adaptable a suelos francos y arcillosos',
            'climate_adaptation': 'Excelente adaptación a climas fríos y húmedos de la región'
        }
    ]
    
    for crop in crops:
        kb.add_crop_knowledge(crop)
    
    # Add climate knowledge
    climate_data = [
        {
            'season': 'Invierno',
            'avg_temperature': '6-10°C',
            'precipitation': 'Alta, entre 2000-3000 mm anuales',
            'wind_patterns': 'Vientos del oeste, frecuentes y moderados',
            'frost_risk': 'Alto, especialmente en zonas altas'
        },
        {
            'season': 'Verano',
            'avg_temperature': '12-18°C',
            'precipitation': 'Menor, pero aún significativa',
            'wind_patterns': 'Vientos más suaves, predominio de brisas',
            'frost_risk': 'Bajo'
        }
    ]
    
    for climate in climate_data:
        kb.add_climate_knowledge(climate)
    
    # Add agricultural practices
    practices = [
        {
            'name': 'Manejo de Praderas',
            'type': 'Producción Ganadera',
            'description': 'Técnicas para mantener y mejorar praderas en la región',
            'best_practices': 'Rotación de potreros, fertilización orgánica, control de malezas',
            'challenges': 'Alta humedad, riesgo de compactación de suelos'
        },
        {
            'name': 'Cultivo de Avellanos',
            'type': 'Fruticultura',
            'description': 'Técnicas específicas para el cultivo de avellanos en Los Ríos',
            'best_practices': 'Poda de formación, control de plagas, riego tecnificado',
            'challenges': 'Condiciones climáticas variables, riesgo de heladas'
        }
    ]
    
    for practice in practices:
        kb.add_agricultural_practice(practice)

if __name__ == "__main__":
    # Populate the knowledge base when the script is run
    populate_initial_knowledge_base()
    
    # Demonstrate querying capabilities
    kb = RegionalKnowledgeBase()
    
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
