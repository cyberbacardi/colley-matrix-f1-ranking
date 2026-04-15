from src.colley_solver import solve_colley_system

def display_rankings(wins, losses, rankings, title):
    print(f"\n{title}")
    print("-" * 60)
    print(f"{'Rank':<5} {'Team':<15} {'Rating':<10} {'Matches':<8}")
    print("-" * 60)

    for i, (team, rank) in enumerate(zip(wins.keys(), rankings), 1):
        total_matches = wins[team] + losses[team]
        print(f"{i:<5} {team:<15} {rank:.4f} {total_matches:<8}")

    print("-" * 60)
    print(f"Total Rating Sum: {sum(rankings):.6f}")

# Scenario 1:  2023 F1 Season
print("=" * 60)
print("SCENARIO 1: Current F1 Season")
print("=" * 60)

wins = {
    'Red Bull': 12,
    'Mercedes': 10,
    'Ferrari': 8,
    'McLaren': 6,
    'Aston Martin': 4
}

losses = {
    'Red Bull': 2,
    'Mercedes': 4,
    'Ferrari': 6,
    'McLaren': 8,
    'Aston Martin': 10
}

rankings = solve_colley_system(wins, losses)
display_rankings(wins, losses, rankings, "Team Rankings:")

# Scenario 2: Custom example
print("\n" + "=" * 60)
print("SCENARIO 2: Simple 3-Team Example")
print("=" * 60)

wins2 = {'Team A': 2, 'Team B': 1, 'Team C': 0}
losses2 = {'Team A': 0, 'Team B': 1, 'Team C': 2}

rankings2 = solve_colley_system(wins2, losses2)
display_rankings(wins2, losses2, rankings2, "Team Rankings:")

print("\n✅ All demonstrations complete!")