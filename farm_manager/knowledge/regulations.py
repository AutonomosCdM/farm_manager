from typing import Dict, Any
from .base import KnowledgeBaseManager


class RegulatoryKnowledgeBase(KnowledgeBaseManager):
    """
    Specialized knowledge base for agricultural regulations.
    """

    def __init__(self):
        """
        Initialize the regulatory knowledge base.
        """
        super().__init__(collection_name="agricultural_regulations")

    def add_regulation_knowledge(self, regulation_data: Dict[str, Any]) -> str:
        """
        Add knowledge about an agricultural regulation to the knowledge base.

        :param regulation_data: Dictionary containing regulatory information
        :return: ID of the added entry
        """
        # Prepare document for semantic search
        document = f"""
        Regulation: {regulation_data.get('name', '')}
        Authority: {regulation_data.get('authority', '')}
        Type: {regulation_data.get('type', '')}
        Description: {regulation_data.get('description', '')}
        Key Requirements: {regulation_data.get('key_requirements', '')}
        Compliance Criteria: {regulation_data.get('compliance_criteria', '')}
        """

        # Prepare metadata
        metadata = {
            "name": regulation_data.get("name", ""),
            "authority": regulation_data.get("authority", ""),
            "type": regulation_data.get("type", ""),
            "year": regulation_data.get("year", ""),
            "region": regulation_data.get("region", "Chile"),
        }

        # Add entry to knowledge base
        return self.add_entry(document, metadata)

    def query_regulations(self, query: str, n_results: int = 5) -> Dict[str, Any]:
        """
        Query agricultural regulations knowledge base with semantic search.

        :param query: Search query
        :param n_results: Number of results to return
        :return: Dictionary of query results
        """
        return self.query(query, n_results)
