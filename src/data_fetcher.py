import requests

API_URL = 'https://api.openf1.com/'


def fetch_f1_season(year):
    """Fetches the F1 season data for a given year."""
    response = requests.get(f'{API_URL}seasons/{year}')
    return response.json()


def fetch_race_results(season, round_number):
    """Fetches the race results for a given season and round number."""
    response = requests.get(f'{API_URL}seasons/{season}/races/{round_number}/results')
    return response.json()


def fetch_drivers():
    """Fetches the list of drivers in the current season."""
    response = requests.get(f'{API_URL}drivers/')
    return response.json()


def fetch_constructors():
    """Fetches the list of constructors in the current season."""
    response = requests.get(f'{API_URL}constructors/')
    return response.json()