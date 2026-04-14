import numpy as np

def solve_colley_system(wins, losses):
    """
    Solves the Colley Matrix ranking system.
    
    Parameters:
    wins - dictionary with team names and win counts
    losses - dictionary with team names and loss counts
    
    Returns:
    List of rankings for each team
    """
    
    # Get list of teams and number of teams
    teams = list(wins.keys())
    n = len(teams)
    
    # Initialize coefficient matrix A (Colley matrix)
    A = [[0.0] * n for _ in range(n)]
    
    # Initialize right-hand side vector b
    b = [0.0] * n
    
    # Build the Colley matrix
    for i in range(n):
        team_i = teams[i]
        games_i = wins[team_i] + losses[team_i]
        
        # Diagonal element
        A[i][i] = 2 + games_i
        
        # Right-hand side
        b[i] = 1 + (wins[team_i] - losses[team_i]) / 2
        
        # Off-diagonal elements
        for j in range(n):
            if i != j:
                A[i][j] = -1
    
    # Solve using Gaussian elimination
    rankings = gaussian_elimination(A, b)
    
    return rankings


def gaussian_elimination(A, b):
    """
    Solves Ax = b using Gaussian elimination with partial pivoting.
    """
    n = len(A)
    
    # Forward elimination
    for k in range(n):
        # Find pivot
        max_idx = k
        for i in range(k + 1, n):
            if abs(A[i][k]) > abs(A[max_idx][k]):
                max_idx = i
        
        # Swap rows
        A[k], A[max_idx] = A[max_idx], A[k]
        b[k], b[max_idx] = b[max_idx], b[k]
        
        # Eliminate column
        for i in range(k + 1, n):
            if A[k][k] != 0:
                factor = A[i][k] / A[k][k]
                for j in range(k, n):
                    A[i][j] -= factor * A[k][j]
                b[i] -= factor * b[k]
    
    # Back substitution
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = b[i]
        for j in range(i + 1, n):
            x[i] -= A[i][j] * x[j]
        if A[i][i] != 0:
            x[i] /= A[i][i]
    
    return x
