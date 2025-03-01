"""
Knowledge management module for Farm Manager.

This module provides specialized knowledge bases for crops,
climate, agricultural practices, and other domain-specific information.
"""

from .base import KnowledgeBaseManager
from .crops import CropKnowledgeBase
from .climate import ClimateKnowledgeBase
from .practices import AgriculturalPracticesKnowledgeBase
from .regulations import RegulatoryKnowledgeBase

__all__ = [
    "KnowledgeBaseManager",
    "CropKnowledgeBase",
    "ClimateKnowledgeBase",
    "AgriculturalPracticesKnowledgeBase",
    "RegulatoryKnowledgeBase",
]
