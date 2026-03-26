import matplotlib.pyplot as plt
import numpy as np


def plot_rankings(rankings):
    """Plots the rankings as a bar chart."""
    plt.figure(figsize=(10, 6))
    plt.barh(range(len(rankings)), rankings, color='skyblue')
    plt.xlabel('Rank')
    plt.ylabel('Participants')
    plt.title('Rankings Visualization')
    plt.gca().invert_yaxis()  # Invert y axis to have the first rank on top
    plt.show()


def plot_matrix_heatmap(matrix):
    """Plots a heatmap of the provided matrix."""
    plt.figure(figsize=(8, 6))
    plt.imshow(matrix, cmap='hot', interpolation='nearest')
    plt.colorbar()  # Show color scale
    plt.title('Matrix Heatmap')
    plt.xlabel('X-axis Label')
    plt.ylabel('Y-axis Label')
    plt.show()