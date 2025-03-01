from typing import Dict, Any
from .base import KnowledgeBaseManager


class AgriculturalPracticesKnowledgeBase(KnowledgeBaseManager):
    """
    Specialized knowledge base for agricultural practices.
    """

    def __init__(self):
        """
        Initialize the agricultural practices knowledge base.
        """
        super().__init__(collection_name="agricultural_practices")

    def add_practice_knowledge(self, practice_data: Dict[str, Any]) -> str:
        """
        Add knowledge about an agricultural practice to the knowledge base.

        :param practice_data: Dictionary containing practice information
        :return: ID of the added entry
        """
        # Prepare document for semantic search
        document = f"""
        Practice: {practice_data.get('name', '')}
        Type: {practice_data.get('type', '')}
        Description: {practice_data.get('description', '')}
        Best Practices: {practice_data.get('best_practices', '')}
        Challenges: {practice_data.get('challenges', '')}
        """

        # Prepare metadata
        metadata = {
            "name": practice_data.get("name", ""),
            "type": practice_data.get("type", ""),
            "region": practice_data.get("region", "Los Ríos"),
        }

        # Add entry to knowledge base
        return self.add_entry(document, metadata)

    def query_practices(self, query: str, n_results: int = 5) -> Dict[str, Any]:
        """
        Query agricultural practices knowledge base with semantic search.

        :param query: Search query
        :param n_results: Number of results to return
        :return: Dictionary of query results
        """
        return self.query(query, n_results)
