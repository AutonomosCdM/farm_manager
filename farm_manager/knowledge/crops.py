from typing import Dict, Any
from .base import KnowledgeBaseManager


class CropKnowledgeBase(KnowledgeBaseManager):
    """
    Specialized knowledge base for crop-related information.
    """

    def __init__(self):
        """
        Initialize the crop knowledge base.
        """
        super().__init__(collection_name="crops")

    def add_crop_knowledge(self, crop_data: Dict[str, Any]) -> str:
        """
        Add knowledge about a specific crop to the knowledge base.

        :param crop_data: Dictionary containing crop information
        :return: ID of the added entry
        """
        # Prepare document for semantic search
        document = f"""
        Crop: {crop_data.get('name', '')}
        Type: {crop_data.get('type', '')}
        Growing Conditions: {crop_data.get('growing_conditions', '')}
        Soil Requirements: {crop_data.get('soil_requirements', '')}
        Climate Adaptation: {crop_data.get('climate_adaptation', '')}
        """

        # Prepare metadata
        metadata = {
            "name": crop_data.get("name", ""),
            "type": crop_data.get("type", ""),
            "region": crop_data.get("region", "Los Ríos"),
        }

        # Add entry to knowledge base
        return self.add_entry(document, metadata)

    def query_crops(self, query: str, n_results: int = 5) -> Dict[str, Any]:
        """
        Query crop knowledge base with semantic search.

        :param query: Search query
        :param n_results: Number of results to return
        :return: Dictionary of query results
        """
        return self.query(query, n_results)
