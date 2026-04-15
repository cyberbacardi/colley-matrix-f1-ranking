import argparse
import logging
from typing import Dict, List, Optional, Tuple

from src.colley_solver import build_colley_system_matrix, solve_colley_system
from src.config import (
    DEFAULT_DRIVER_WEIGHT,
    DEFAULT_PENALTY_WEIGHT,
    DEFAULT_POINTS_WEIGHT,
    DEFAULT_RELIABILITY_WEIGHT,
    DEFAULT_SEASON,
    LOG_FORMAT,
    LOG_LEVEL,
    RANKING_PRECISION,
)
from src.visualizer import plot_dashboard, plot_factor_comparison, plot_matrix_heatmap, plot_rankings

# Configure logging
logging.basicConfig(level=getattr(logging, LOG_LEVEL), format=LOG_FORMAT)
logger = logging.getLogger(__name__)


def get_default_team_data() -> Tuple[
    Dict[str, int],
    Dict[str, int],
    Dict[str, float],
    Dict[str, float],
    Dict[str, float],
    Dict[str, float],
]:
    wins = {
        'Red Bull': 12,
        'Mercedes': 10,
        'Ferrari': 8,
        'McLaren': 6,
    }

    losses = {
        'Red Bull': 2,
        'Mercedes': 4,
        'Ferrari': 6,
        'McLaren': 8,
    }

    points = {
        'Red Bull': 450,
        'Mercedes': 392,
        'Ferrari': 312,
        'McLaren': 250,
    }

    penalty_points = {
        'Red Bull': 2,
        'Mercedes': 0,
        'Ferrari': 1,
        'McLaren': 3,
    }

    reliability = {
        'Red Bull': 0.95,
        'Mercedes': 0.92,
        'Ferrari': 0.88,
        'McLaren': 0.80,
    }

    driver_rating = {
        'Red Bull': 0.98,
        'Mercedes': 0.96,
        'Ferrari': 0.90,
        'McLaren': 0.85,
    }

    return wins, losses, points, penalty_points, reliability, driver_rating


def filter_team_data(
    teams: List[str],
    wins: Dict[str, int],
    losses: Dict[str, int],
    points: Dict[str, float],
    penalty_points: Dict[str, float],
    reliability: Dict[str, float],
    driver_rating: Dict[str, float],
) -> Tuple[
    Dict[str, int],
    Dict[str, int],
    Dict[str, float],
    Dict[str, float],
    Dict[str, float],
    Dict[str, float],
]:
    selected = [team for team in teams if team in wins]
    if not selected:
        raise ValueError("No matching teams found for the provided filter")

    def _pick(data):
        return {team: data[team] for team in selected}

    return (
        _pick(wins),
        _pick(losses),
        _pick(points),
        _pick(penalty_points),
        _pick(reliability),
        _pick(driver_rating),
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Colley Matrix F1 Ranking System with enhanced CLI options'
    )
    parser.add_argument('--season', type=int, default=DEFAULT_SEASON, help='Season year label')
    parser.add_argument(
        '--teams', nargs='+', help='Filter output to one or more team names'
    )
    parser.add_argument(
        '--points-weight', type=float, default=DEFAULT_POINTS_WEIGHT, help='Weight applied to points input'
    )
    parser.add_argument(
        '--penalty-weight', type=float, default=DEFAULT_PENALTY_WEIGHT, help='Weight applied to penalty points'
    )
    parser.add_argument(
        '--driver-weight', type=float, default=DEFAULT_DRIVER_WEIGHT, help='Weight applied to driver rating'
    )
    parser.add_argument(
        '--reliability-weight', type=float, default=DEFAULT_RELIABILITY_WEIGHT, help='Weight applied to reliability factor'
    )
    parser.add_argument(
        '--no-plot', action='store_true', help='Disable plotting of charts'
    )
    parser.add_argument(
        '--no-heatmap', action='store_true', help='Disable the matrix heatmap plot'
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    wins, losses, points, penalty_points, reliability, driver_rating = get_default_team_data()

    if args.teams:
        wins, losses, points, penalty_points, reliability, driver_rating = filter_team_data(
            args.teams,
            wins,
            losses,
            points,
            penalty_points,
            reliability,
            driver_rating,
        )

    logger.info('Starting Colley Matrix F1 Ranking System')
    print('=' * 50)
    print(f'Colley Matrix F1 Ranking System — Season {args.season}')
    print('=' * 50)
    print(f'Points weight: {args.points_weight}, penalty weight: {args.penalty_weight}, driver weight: {args.driver_weight}, reliability weight: {args.reliability_weight}')
    print(f'Plots enabled: {not args.no_plot}, heatmap enabled: {not args.no_heatmap}')

    try:
        rankings = solve_colley_system(
            wins,
            losses,
            points=points,
            penalty_points=penalty_points,
            reliability=reliability,
            driver_rating=driver_rating,
            points_weight=args.points_weight,
            penalty_weight=args.penalty_weight,
            driver_weight=args.driver_weight,
            reliability_weight=args.reliability_weight,
        )
        logger.info('Ranking computation completed successfully')

        print('\nTeam Rankings:')
        print('-' * 60)
        print(f"{'Rank':<5} {'Team':<15} {'Rating':<10} {'Matches':<8}")
        print('-' * 60)

        teams = list(wins.keys())
        for i, (team, rank) in enumerate(zip(teams, rankings), 1):
            total_matches = wins[team] + losses[team]
            print(f"{i:<5} {team:<15} {rank:.{RANKING_PRECISION}f} {total_matches:<8}")

        print('-' * 60)
        print(f'Total Rating Sum: {sum(rankings):.6f}')
        print('\n✅ Ranking complete!')
        logger.info('Results displayed successfully')

        if not args.no_plot:
            teams, matrix, _ = build_colley_system_matrix(
                wins,
                losses,
                reliability=reliability,
                reliability_weight=args.reliability_weight,
            )
            if not args.no_heatmap:
                plot_dashboard(
                    teams,
                    rankings,
                    matrix,
                    points=points,
                    penalty_points=penalty_points,
                    reliability=reliability,
                    driver_rating=driver_rating,
                )
            else:
                plot_rankings(teams, rankings)
                plot_factor_comparison(
                    teams,
                    points=points,
                    penalty_points=penalty_points,
                    reliability=reliability,
                    driver_rating=driver_rating,
                )

    except Exception as e:
        logger.error(f'An error occurred during ranking: {e}')
        print(f'Error: {e}')


if __name__ == '__main__':
    main()