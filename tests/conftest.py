
"""
Pytest configuration module.

Provides fixtures for tests.
"""

import pytest
from pathlib import Path
import sys
import os

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

@pytest.fixture
def test_data_dir():
    """
    Test data directory fixture.
    
    Returns:
        Path: Path to test data directory.
    """
    return Path(__file__).parent / 'test_data'

@pytest.fixture
def mock_config():
    """
    Mock configuration fixture.
    
    Returns:
        dict: Mock configuration.
    """
    return {
        'mock_data': True,
        'test_environment': 'test'
    }

@pytest.fixture
def sample_crop_data():
    """
    Sample crop data fixture.
    
    Returns:
        dict: Sample crop data.
    """
    return {
        'name': 'Test Crop',
        'water_needs': 10,
        'growth_days': 90
    }
