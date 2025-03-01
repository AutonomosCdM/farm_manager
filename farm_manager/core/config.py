from dataclasses import dataclass, field
from typing import Dict, Any
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@dataclass
class FarmManagerConfig:
    """
    Centralized configuration for Farm Manager application.
    Loads settings from environment variables with sensible defaults.
    """

    # Database Configuration
    DATABASE_URL: str = field(
        default_factory=lambda: os.getenv("DATABASE_URL", "sqlite:///farm_manager.db")
    )

    # API Configuration
    API_HOST: str = field(default_factory=lambda: os.getenv("API_HOST", "localhost"))
    API_PORT: int = field(default_factory=lambda: int(os.getenv("API_PORT", 8000)))

    # Logging Configuration
    LOG_LEVEL: str = field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))

    # Resource Management
    RESOURCE_DATA_PATH: str = field(
        default_factory=lambda: os.getenv("RESOURCE_DATA_PATH", "resource_data/")
    )

    @classmethod
    def get_config(cls) -> "FarmManagerConfig":
        """
        Factory method to create a configuration instance.

        Returns:
            FarmManagerConfig: Configured instance with environment-specific settings
        """
        return cls()
