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

def add_antinodes(grid, p1, p2, distance):

    # Get the direction
    dir = get_direction(p1, p2)
    new_pos = [p1[0], p1[1]]

    inside = True
    while inside:
        # Get the next antinode
        new_pos = [new_pos[0] + (dir[0] * distance[0]), new_pos[1] + (dir[1] * distance[1])]
        res = add_antinode(grid, new_pos)
        if res == False:
            inside = False

def add_antinode(grid, p):
    i, j = p

    if 0 <= i < len(grid) and 0 <= j < len(grid[0]):
        grid[i][j] = '#'
        return True

    return False


def main(file_path):
    # input_file = file_path + "input-00.txt"
    input_file = file_path + "input-01.txt"
    # input_file = file_path + "input-02.txt"

    # Get the grid data
    with open(input_file, 'r') as file:
        rows = file.read().strip().split('\n')
        grid = [list(col) for col in rows]

    ROWS = len(grid)
    COLS = len(grid[0])

    print_grid(grid)

    # Initialize the antinode map
    antinode_map = grid[:]

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

            # Get the antinodes next to p1
            add_antinodes(antinode_map, p1, p2, distance)
            # print(f'\tAntinode point: [{p1_antinode[0]}, {p1_antinode[1]}]')

            # Get the antinodes next to p2
            add_antinodes(antinode_map, p2, p1, distance)
            # print(f'\tAntinode point: [{p2_antinode[0]}, {p2_antinode[1]}]')

    print('\nANTINODES:')
    print_grid(antinode_map)

    antinode_count = sum(cell != '.' for row in antinode_map for cell in row)
    print(f'Total antinodes: {antinode_count}')

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python day-08.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    main(file_path)

