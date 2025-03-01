from typing import Dict, Any
from .base import KnowledgeBaseManager


class ClimateKnowledgeBase(KnowledgeBaseManager):
    """
    Specialized knowledge base for climate-related information.
    """

    def __init__(self):
        """
        Initialize the climate knowledge base.
        """
        super().__init__(collection_name="climate")

    def add_climate_knowledge(self, climate_data: Dict[str, Any]) -> str:
        """
        Add climate-related knowledge to the knowledge base.

        :param climate_data: Dictionary containing climate information
        :return: ID of the added entry
        """
        # Prepare document for semantic search
        document = f"""
        Season: {climate_data.get('season', '')}
        Average Temperature: {climate_data.get('avg_temperature', '')}
        Precipitation: {climate_data.get('precipitation', '')}
        Wind Patterns: {climate_data.get('wind_patterns', '')}
        Frost Risk: {climate_data.get('frost_risk', '')}
        """

        # Prepare metadata
        metadata = {
            "season": climate_data.get("season", ""),
            "region": climate_data.get("region", "Los Ríos"),
        }

        # Add entry to knowledge base
        return self.add_entry(document, metadata)

    def query_climate(self, query: str, n_results: int = 5) -> Dict[str, Any]:
        """
        Query climate knowledge base with semantic search.

        :param query: Search query
        :param n_results: Number of results to return
        :return: Dictionary of query results
        """
        return self.query(query, n_results)
