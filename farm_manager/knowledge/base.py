import os
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings

from ..core.config import FarmManagerConfig
from ..core.exceptions import KnowledgeBaseError


class KnowledgeBaseManager:
    """
    Base class for managing specialized knowledge bases using ChromaDB.
    """

    def __init__(
        self,
        collection_name: str,
        config: Optional[FarmManagerConfig] = None,
        persist_directory: Optional[str] = None,
    ):
        """
        Initialize the knowledge base manager.

        :param collection_name: Name of the ChromaDB collection
        :param config: Optional configuration object
        :param persist_directory: Optional directory to persist the knowledge base
        """
        # Use provided config or create default
        self.config = config or FarmManagerConfig.get_config()

        # Determine persist directory
        if persist_directory is None:
            persist_directory = os.path.join(self.config.RESOURCE_DATA_PATH, "knowledge_base")

        # Ensure the persist directory exists
        os.makedirs(persist_directory, exist_ok=True)

        # Configure ChromaDB client
        self.chroma_client = chromadb.PersistentClient(path=persist_directory)

        # Create or get the collection
        self.collection = self._create_or_get_collection(collection_name)

    def _create_or_get_collection(self, collection_name: str):
        """
        Create or retrieve a ChromaDB collection.

        :param collection_name: Name of the collection
        :return: ChromaDB collection
        """
        return self.chroma_client.get_or_create_collection(name=collection_name)

    def add_entry(
        self, document: str, metadata: Dict[str, Any], entry_id: Optional[str] = None
    ) -> str:
        """
        Add an entry to the knowledge base.

        :param document: Text content of the entry
        :param metadata: Metadata associated with the entry
        :param entry_id: Optional custom ID, generated if not provided
        :return: ID of the added entry
        """
        try:
            # Generate ID if not provided
            if entry_id is None:
                entry_id = f"{metadata.get('name', 'unknown')}_{hash(frozenset(metadata.items()))}"

            # Add to ChromaDB collection
            self.collection.add(ids=[entry_id], documents=[document], metadatas=[metadata])

            return entry_id

        except Exception as e:
            raise KnowledgeBaseError(f"Error adding entry: {e}")

    def query(self, query_text: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """
        Perform a semantic search query on the knowledge base.

        :param query_text: Search query
        :param n_results: Number of results to return
        :return: List of matching knowledge base entries
        """
        try:
            results = self.collection.query(query_texts=[query_text], n_results=n_results)

            return [
                {
                    "id": results["ids"][0][i],
                    "document": results["documents"][0][i],
                    "metadata": results["metadatas"][0][i],
                    "distance": results["distances"][0][i],
                }
                for i in range(len(results["ids"][0]))
            ]

        except Exception as e:
            raise KnowledgeBaseError(f"Error performing query: {e}")

    def delete_entry(self, entry_id: str) -> bool:
        """
        Delete an entry from the knowledge base.

        :param entry_id: ID of the entry to delete
        :return: True if deletion was successful
        """
        try:
            self.collection.delete(ids=[entry_id])
            return True
        except Exception as e:
            raise KnowledgeBaseError(f"Error deleting entry: {e}")
