def build_colley_matrix(race_results):
    # Build the Colley Matrix from race results
    # Initialize matrix and calculations here...
    pass


def extract_teams_from_races(race_results):
    # Extract teams from the list of race results
    teams = set()
    for race in race_results:
        for result in race['results']:
            teams.add(result['team'])
    return list(teams)


def print_matrix_stats(matrix):
    # Print statistics about the Colley Matrix
    print("Colley Matrix:")
    for row in matrix:
        print(row)  
    # Further stats can be calculated and printed here...
    pass