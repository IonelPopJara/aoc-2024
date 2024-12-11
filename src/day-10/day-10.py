def main(file_path):
    input_file = file_path + "input-00.txt"

    # Get the grid data
    with open(input_file, 'r') as file:
        rows = file.read().strip().split('\n')
        grid = [list(col) for col in rows]

    ROWS = len(grid)
    COLS = len(grid[0])


    counter = {'count': 0}

    visited = set()

    def find_paths(grid, i, j, previous_height, counter):

        if (i, j) in visited:
            return

        current_height = int(grid[i][j])
        print(f'Current: {current_height}[{i}, {j}]', end="")

        if (current_height - previous_height != 1):
            print(f'Invalid trail')
            return
        elif current_height == 9:
            print(f'Valid trail')
            counter['count'] += 1
            return
        else:
            print("")

        visited.add((i, j))

        # Find paths up, down, left, and right
        if i - 1 >= 0:
            find_paths(grid, i - 1, j, current_height, counter) # Up

        if i + 1 < ROWS:
            find_paths(grid, i + 1, j, current_height, counter) # Down

        if j - 1 >= 0:
            find_paths(grid, i, j - 1, current_height, counter) # Left

        if j + 1 < COLS:
            find_paths(grid, i, j + 1, current_height, counter) # Right

    for idx, row in enumerate(grid):
        for jdx, pos in enumerate(row):
            if pos == '0':
                find_paths(grid, idx, jdx, -1, counter)

    print(f'Counter: {counter}')

import sys
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python day-08.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    main(file_path)

