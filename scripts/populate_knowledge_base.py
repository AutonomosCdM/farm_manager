#!/usr/bin/env python3
import os
import sys
import json
from typing import Dict, Any

# Add project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from farm_manager.knowledge.base import KnowledgeBase
from farm_manager.knowledge import climate, crops, practices, regulations


def load_json_data(filepath: str) -> Dict[str, Any]:
    """Load JSON data from a file."""
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning: File {filepath} not found.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in {filepath}")
        return {}


def populate_knowledge_base():
    """Populate the knowledge base with initial data."""
    kb = KnowledgeBase()

    # Populate climate knowledge
    climate_data = load_json_data(os.path.join(project_root, "data", "climate_data.json"))
    for region, data in climate_data.items():
        kb.add_climate_data(region, data)

    # Populate crop knowledge
    crops_data = load_json_data(os.path.join(project_root, "data", "crops_data.json"))
    for crop_type, details in crops_data.items():
        kb.add_crop_knowledge(crop_type, details)

    # Populate agricultural practices
    practices_data = load_json_data(os.path.join(project_root, "data", "practices_data.json"))
    for practice, details in practices_data.items():
        kb.add_agricultural_practice(practice, details)

    # Populate agricultural regulations
    regulations_data = load_json_data(os.path.join(project_root, "data", "regulations_data.json"))
    for regulation, details in regulations_data.items():
        kb.add_regulation(regulation, details)

    print("Knowledge base populated successfully.")


def main():
    try:
        populate_knowledge_base()
    except Exception as e:
        print(f"Error populating knowledge base: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
