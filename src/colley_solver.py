def solve_colley_system(wins, losses):
    n = len(wins)
    A = [[0] * n for _ in range(n)]
    b = [0] * n

    for i in range(n):
        A[i][i] = wins[i] + 0.5 * losses[i] + 1
        b[i] = wins[i] + 0.5 * losses[i]

        for j in range(n):
            if i != j:
                A[i][j] = -0.5 * losses[j]

    return gaussian_elimination(A, b)


def gaussian_elimination(A, b):
    n = len(A)
    for i in range(n):
        for j in range(i + 1, n):
            if A[j][i] != 0:
                ratio = A[j][i] / A[i][i]
                for k in range(i, n):
                    A[j][k] -= ratio * A[i][k]
                b[j] -= ratio * b[i]

    return back_substitution(A, b)


def back_substitution(A, b):
    n = len(A)
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = b[i]
        for j in range(i + 1, n):
            x[i] -= A[i][j] * x[j]
        x[i] /= A[i][i]
    return x


def verify_solution(ranks, wins, losses):
    for i in range(len(ranks)):
        if ranks[i] < 0:
            return False
    return True


def print_rankings(ranks):
    for i, rank in enumerate(ranks):
        print(f"Team {i + 1}: {rank:.2f}")