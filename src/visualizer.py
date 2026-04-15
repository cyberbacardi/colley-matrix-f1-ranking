import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, List, Optional


def plot_rankings(teams: List[str], rankings: List[float]) -> None:
    """Plots team rankings as a labeled horizontal bar chart."""
    plt.figure(figsize=(10, 6))
    y = np.arange(len(teams))
    plt.barh(y, rankings, color='skyblue')
    plt.yticks(y, teams)
    plt.xlabel('Normalized Rating')
    plt.title('Team Ranking Visualization')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()


def _normalize_series(series: List[float]) -> List[float]:
    if not series:
        return []
    minimum = min(series)
    maximum = max(series)
    if maximum == minimum:
        return [0.5 for _ in series]
    normalized = [(value - minimum) / (maximum - minimum) for value in series]
    # Keep minimum values visible instead of collapsing to zero
    return [0.1 + 0.9 * value for value in normalized]


def plot_factor_comparison(
    teams: List[str],
    points: Optional[Dict[str, float]] = None,
    penalty_points: Optional[Dict[str, float]] = None,
    reliability: Optional[Dict[str, float]] = None,
    driver_rating: Optional[Dict[str, float]] = None,
) -> None:
    """Plots a normalized comparison of rating factors across teams."""
    categories = []
    raw_values = []
    if points is not None:
        categories.append('Points')
        raw_values.append([points.get(team, 0.0) for team in teams])
    if penalty_points is not None:
        categories.append('Penalties')
        raw_values.append([penalty_points.get(team, 0.0) for team in teams])
    if reliability is not None:
        categories.append('Reliability')
        raw_values.append([reliability.get(team, 0.0) for team in teams])
    if driver_rating is not None:
        categories.append('Driver Rating')
        raw_values.append([driver_rating.get(team, 0.0) for team in teams])

    if not categories:
        return

    normalized_values = [_normalize_series(series) for series in raw_values]
    x = np.arange(len(teams))
    width = 0.8 / len(categories)
    plt.figure(figsize=(12, 6))

    for i, (label, series) in enumerate(zip(categories, normalized_values)):
        bars = plt.bar(x + i * width, series, width=width, label=f'{label} (normalized)')
        for bar, raw_value in zip(bars, raw_values[i]):
            plt.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.02,
                f'{raw_value:.2f}',
                ha='center',
                va='bottom',
                fontsize=8,
            )

    plt.xticks(x + width * (len(categories) - 1) / 2, teams)
    plt.xlabel('Teams')
    plt.ylabel('Normalized score')
    plt.title('Rating Factor Comparison (normalized across factors)')
    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_matrix_heatmap(matrix):
    """Plots a heatmap of the provided matrix."""
    plt.figure(figsize=(8, 6))
    plt.imshow(matrix, cmap='hot', interpolation='nearest')
    plt.colorbar()
    plt.title('Matrix Heatmap')
    plt.xlabel('Column index')
    plt.ylabel('Row index')
    plt.tight_layout()
    plt.show()


def plot_dashboard(
    teams: List[str],
    rankings: List[float],
    matrix,
    points: Optional[Dict[str, float]] = None,
    penalty_points: Optional[Dict[str, float]] = None,
    reliability: Optional[Dict[str, float]] = None,
    driver_rating: Optional[Dict[str, float]] = None,
) -> None:
    """Displays rankings, factor comparison, and matrix heatmap together."""
    categories = []
    raw_values = []
    if points is not None:
        categories.append('Points')
        raw_values.append([points.get(team, 0.0) for team in teams])
    if penalty_points is not None:
        categories.append('Penalties')
        raw_values.append([penalty_points.get(team, 0.0) for team in teams])
    if reliability is not None:
        categories.append('Reliability')
        raw_values.append([reliability.get(team, 0.0) for team in teams])
    if driver_rating is not None:
        categories.append('Driver Rating')
        raw_values.append([driver_rating.get(team, 0.0) for team in teams])

    normalized_values = [_normalize_series(series) for series in raw_values]
    x = np.arange(len(teams))
    width = 0.8 / max(1, len(categories))

    fig, axs = plt.subplots(1, 3, figsize=(20, 6))

    axs[0].barh(np.arange(len(teams)), rankings, color='skyblue')
    axs[0].set_yticks(np.arange(len(teams)))
    axs[0].set_yticklabels(teams)
    axs[0].invert_yaxis()
    axs[0].set_xlabel('Rating')
    axs[0].set_title('Team Rankings')

    if categories:
        for i, (label, series) in enumerate(zip(categories, normalized_values)):
            axs[1].bar(x + i * width, series, width=width, label=f'{label} (norm)')
        axs[1].set_xticks(x + width * (len(categories) - 1) / 2)
        axs[1].set_xticklabels(teams)
        axs[1].set_xlabel('Teams')
        axs[1].set_ylabel('Normalized score')
        axs[1].set_title('Factor Comparison')
        axs[1].legend(fontsize='small')
    else:
        axs[1].text(0.5, 0.5, 'No factor data', ha='center', va='center')
        axs[1].set_axis_off()

    heatmap = axs[2].imshow(matrix, cmap='hot', interpolation='nearest')
    axs[2].set_title('Colley Matrix Heatmap')
    axs[2].set_xlabel('Column index')
    axs[2].set_ylabel('Row index')
    fig.colorbar(heatmap, ax=axs[2], fraction=0.046, pad=0.04)

    plt.suptitle('Colley Rating Dashboard')
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()