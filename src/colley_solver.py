import numpy as np
from typing import Dict, List, Optional


def _normalize_scores(values: Optional[Dict[str, float]]) -> Dict[str, float]:
    if not values:
        return {}
    max_value = max(values.values())
    if max_value <= 0:
        return {team: 0.0 for team in values}
    return {team: value / max_value for team, value in values.items()}


def solve_colley_system(
    wins: Dict[str, int],
    losses: Dict[str, int],
    points: Optional[Dict[str, float]] = None,
    penalty_points: Optional[Dict[str, float]] = None,
    reliability: Optional[Dict[str, float]] = None,
    driver_rating: Optional[Dict[str, float]] = None,
    points_weight: float = 0.5,
    penalty_weight: float = 1.0,
    driver_weight: float = 0.3,
    reliability_weight: float = 1.0,
) -> List[float]:
    """
    Solves the Colley Matrix ranking system with optional rating enhancements.

    Parameters:
    wins - dictionary with team names and win counts
    losses - dictionary with team names and loss counts
    points - optional team points values for a points-based rating system
    penalty_points - optional penalty totals to subtract from rating
    reliability - optional reliability score per team (0.0 to 1.0)
    driver_rating - optional driver rating score per team

    Returns:
    List of rankings for each team in the same order as wins.keys()

    Raises:
    ValueError: If wins and losses have different teams or invalid data
    """
    if set(wins.keys()) != set(losses.keys()):
        raise ValueError("Wins and losses dictionaries must have the same teams")

    teams = list(wins.keys())
    for extra in (points, penalty_points, reliability, driver_rating):
        if extra is not None and set(extra.keys()) != set(teams):
            raise ValueError("All rating inputs must use the same team set")

    points_norm = _normalize_scores(points)
    penalties_norm = _normalize_scores(penalty_points)
    driver_norm = _normalize_scores(driver_rating)

    n = len(teams)
    A = np.zeros((n, n))
    b = np.zeros(n)

    for i in range(n):
        team_i = teams[i]
        games_i = wins[team_i] + losses[team_i]
        reliability_value = 1.0 if reliability is None else reliability.get(team_i, 1.0)
        if not 0.0 <= reliability_value <= 1.0:
            raise ValueError("Reliability values must be between 0.0 and 1.0")

        reliability_adjustment = reliability_weight * (1.0 - reliability_value) * games_i
        A[i, i] = 2 + games_i + reliability_adjustment

        points_adjustment = points_weight * (points_norm.get(team_i, 0.0) - 0.5)
        penalty_adjustment = penalty_weight * penalties_norm.get(team_i, 0.0)
        driver_adjustment = driver_weight * driver_norm.get(team_i, 0.0)

        b[i] = (
            1
            + (wins[team_i] - losses[team_i]) / 2
            + points_adjustment
            + driver_adjustment
            - penalty_adjustment
        )

        for j in range(n):
            if i != j:
                A[i, j] = -1

    try:
        rankings = np.linalg.solve(A, b)
        total = np.sum(rankings)
        if total != 0:
            rankings = rankings / total
        return rankings.tolist()
    except np.linalg.LinAlgError as e:
        raise ValueError(f"Failed to solve the linear system: {e}")


def build_colley_system_matrix(
    wins: Dict[str, int],
    losses: Dict[str, int],
    reliability: Optional[Dict[str, float]] = None,
    reliability_weight: float = 1.0,
) -> tuple[List[str], np.ndarray, np.ndarray]:
    """Builds and returns the Colley matrix and rhs vector."""
    if set(wins.keys()) != set(losses.keys()):
        raise ValueError("Wins and losses dictionaries must have the same teams")

    teams = list(wins.keys())
    n = len(teams)
    A = np.zeros((n, n))
    b = np.zeros(n)

    for i in range(n):
        team_i = teams[i]
        games_i = wins[team_i] + losses[team_i]
        reliability_value = 1.0 if reliability is None else reliability.get(team_i, 1.0)
        if not 0.0 <= reliability_value <= 1.0:
            raise ValueError("Reliability values must be between 0.0 and 1.0")

        reliability_adjustment = reliability_weight * (1.0 - reliability_value) * games_i
        A[i, i] = 2 + games_i + reliability_adjustment
        b[i] = 1 + (wins[team_i] - losses[team_i]) / 2

        for j in range(n):
            if i != j:
                A[i, j] = -1

    return teams, A, b
