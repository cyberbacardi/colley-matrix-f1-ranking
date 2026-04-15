import pytest
from src.colley_solver import solve_colley_system

def test_solve_colley_system_basic():
    """Test basic functionality with sample data."""
    wins = {'Team A': 2, 'Team B': 1, 'Team C': 0}
    losses = {'Team A': 0, 'Team B': 1, 'Team C': 2}
    
    rankings = solve_colley_system(wins, losses)
    
    assert len(rankings) == 3
    assert rankings[0] > rankings[1] > rankings[2]  # Team A should rank highest
    assert all(isinstance(r, float) for r in rankings)

def test_solve_colley_system_mismatched_teams():
    """Test error handling for mismatched team dictionaries."""
    wins = {'Team A': 1, 'Team B': 1}
    losses = {'Team A': 1}  # Missing Team B
    
    with pytest.raises(ValueError, match="must have the same teams"):
        solve_colley_system(wins, losses)

def test_solve_colley_system_single_team():
    """Test with a single team."""
    wins = {'Team A': 5}
    losses = {'Team A': 0}
    
    rankings = solve_colley_system(wins, losses)
    
    assert len(rankings) == 1
    assert isinstance(rankings[0], float)


def test_solve_colley_system_with_enhancements():
    """Test points, penalty, reliability, and driver-rating enhancements."""
    wins = {'Team A': 2, 'Team B': 1}
    losses = {'Team A': 0, 'Team B': 1}
    points = {'Team A': 50.0, 'Team B': 30.0}
    penalty_points = {'Team A': 0.0, 'Team B': 10.0}
    reliability = {'Team A': 0.95, 'Team B': 0.80}
    driver_rating = {'Team A': 0.99, 'Team B': 0.85}

    rankings = solve_colley_system(
        wins,
        losses,
        points=points,
        penalty_points=penalty_points,
        reliability=reliability,
        driver_rating=driver_rating,
    )

    assert len(rankings) == 2
    assert rankings[0] > rankings[1]
    assert abs(sum(rankings) - 1.0) < 1e-9