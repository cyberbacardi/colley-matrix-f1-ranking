"""
Configuration settings for the Colley Matrix F1 Ranking System.
"""

# API settings
API_BASE_URL = 'https://api.openf1.com/'
REQUEST_TIMEOUT = 10  # seconds

# Default season for data fetching
DEFAULT_SEASON = 2023

# Logging settings
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'

# Output settings
RANKING_PRECISION = 4  # decimal places for ranking display

# Default factor weights for the enhanced rating system
DEFAULT_POINTS_WEIGHT = 0.5
DEFAULT_PENALTY_WEIGHT = 1.0
DEFAULT_DRIVER_WEIGHT = 0.3
DEFAULT_RELIABILITY_WEIGHT = 1.0