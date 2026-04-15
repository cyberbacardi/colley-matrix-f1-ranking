import requests
import logging
from typing import Dict, List, Any
from .config import API_BASE_URL, REQUEST_TIMEOUT

logger = logging.getLogger(__name__)

def fetch_f1_season(year: int) -> Dict[str, Any]:
    """Fetches the F1 season data for a given year."""
    try:
        response = requests.get(f'{API_BASE_URL}seasons/{year}', timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        logger.info(f"Successfully fetched season data for {year}")
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Failed to fetch season data for {year}: {e}")
        raise

def fetch_race_results(season: int, round_number: int) -> List[Dict[str, Any]]:
    """Fetches the race results for a given season and round number."""
    try:
        response = requests.get(f'{API_BASE_URL}seasons/{season}/races/{round_number}/results', timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        logger.info(f"Successfully fetched race results for season {season}, round {round_number}")
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Failed to fetch race results for season {season}, round {round_number}: {e}")
        raise

def fetch_drivers() -> List[Dict[str, Any]]:
    """Fetches the list of drivers in the current season."""
    try:
        response = requests.get(f'{API_BASE_URL}drivers/', timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        logger.info("Successfully fetched drivers list")
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Failed to fetch drivers: {e}")
        raise

def fetch_constructors() -> List[Dict[str, Any]]:
    """Fetches the list of constructors in the current season."""
    try:
        response = requests.get(f'{API_BASE_URL}constructors/', timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        logger.info("Successfully fetched constructors list")
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Failed to fetch constructors: {e}")
        raise