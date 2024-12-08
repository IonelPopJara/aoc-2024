import sys
from itertools import combinations

def print_grid(grid):
    print("---GRID---")
    for line in grid:
        for freq in line:
            print(freq, end="")
        print("")
    print("---GRID---")

def get_distance(p1, p2):
    return (abs(p2[0] - p1[0]), abs(p2[1] - p1[1]))

def get_direction(p1, p2):
    return (
        (p1[0] - p2[0]) // max(abs(p1[0] - p2[0]), 1),
        (p1[1] - p2[1]) // max(abs(p1[1] - p2[1]), 1),
    )

def get_antinode(p1, p2, distance):

    # Get the antinode next to p1
    v1_direction = get_direction(p1, p2)
    # print(f'\tp1 antinode direction: {v1_direction}')
    antinode_pos = (p1[0] + (v1_direction[0] * distance[0]), p1[1] + (v1_direction[1] * distance[1]))

    return antinode_pos

def add_antinode(grid, p):
    i, j = p

    if 0 <= i < len(grid) and 0 <= j < len(grid[0]):
        grid[i][j] = '#'


def main(file_path):
    input_file = file_path + "input-00.txt"
    # input_file = file_path + "input-01.txt"

    # Get the grid data
    with open(input_file, 'r') as file:
        rows = file.read().strip().split('\n')
        grid = [list(col) for col in rows]

    ROWS = len(grid)
    COLS = len(grid[0])

    print_grid(grid)

    # Initialize the antinode map
    antinode_map = [['.' for _ in range(COLS)] for _ in range(ROWS)]

    points = {}
    # Iterate through the grid and store all the points in a dictionary
    for idx, row in enumerate(grid):
        for jdx, freq in enumerate(row):
            if freq != '.':
                points.setdefault(freq, []).append((idx, jdx))

    print(points)

    # Iterate through all the frequencies
    for freq, positions in points.items():
        # Get all the pair combinations for a given frequency
        # print(f'Freq: {freq} | Positions: {positions}')

        # Iterate through all the pairs and find antinodes
        for p1, p2 in combinations(positions, 2):
            distance = get_distance(p1, p2)

            # Get the antinode next to p1
            p1_antinode = get_antinode(p1, p2, distance)
            # print(f'\tAntinode point: [{p1_antinode[0]}, {p1_antinode[1]}]')

            # Get the antinode next to p2
            p2_antinode = get_antinode(p2, p1, distance)
            # print(f'\tAntinode point: [{p2_antinode[0]}, {p2_antinode[1]}]')

            # Add both antinodes to the antinode map
            add_antinode(antinode_map, p1_antinode)
            add_antinode(antinode_map, p2_antinode)

    print('\nANTINODES:')
    print_grid(antinode_map)

    antinode_count = sum(row.count('#') for row in antinode_map)
    print(f'Total antinodes: {antinode_count}')

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python day-08.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    main(file_path)

