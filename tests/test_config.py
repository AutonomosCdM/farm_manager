
"""
Test configuration module.

Provides configuration for tests.
"""

import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Test configuration
TEST_CONFIG = {
    'mock_data': True,
    'skip_slow_tests': True,
    'test_environment': 'development'
}

def get_test_config():
    """
    Get test configuration.
    
    Returns:
        dict: Test configuration.
    """
    return TEST_CONFIG
