from src.colley_solver import solve_colley_system

# Sample F1 team data
wins = {
    'Red Bull': 12,
    'Mercedes': 10,
    'Ferrari': 8,
    'McLaren': 6
}

losses = {
    'Red Bull': 2,
    'Mercedes': 4,
    'Ferrari': 6,
    'McLaren': 8
}

print("=" * 50)
print("Colley Matrix F1 Ranking System")
print("=" * 50)

# Run the solver
rankings = solve_colley_system(wins, losses)

# Display results
print("\nTeam Rankings:")
print("-" * 50)

for i, (team, rank) in enumerate(zip(wins.keys(), rankings), 1):
    print(f"{i}. {team}: {rank:.4f}")

print("-" * 50)
print("\n✅ Ranking complete!")