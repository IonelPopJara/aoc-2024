import sys

DIRECTIONS = [
    (-1, 0),    # Up
    (1, 0),     # Down
    (0, -1),    # Left
    (0, 1),     # Right
    (-1, -1),   # Up Left
    (-1, 1),    # Up Right
    (1, -1),    # Down Left
    (1, 1),     # Down Right
]

def path_finding(i, j, ROWS, COLS, GRID, current_char, DIRECTION):
    target = "XMAS"
    if current_char == len(target):
        return 1

    if (i < 0 or i >= COLS or j < 0 or j >= ROWS or GRID[i][j] != target[current_char]):
        return 0

    di, dj = DIRECTION
    return path_finding(i + di, j + dj, ROWS, COLS, GRID, current_char + 1, DIRECTION)

def create_grid(file_path):
    grid = []

    input_file = file_path + "input-01.txt"
    with open(input_file) as file:
        for line in file:
            # Store the letters in a grid
            grid.append(list(line.strip()))

    ROWS = len(grid[0]) # Assume that all the rows are the same size
    COLS = len(grid)

    return (grid, ROWS, COLS)

def part_1(file_path):

    grid, ROWS, COLS = create_grid(file_path)

    print('Counting loop')
    total_paths = 0
    for i in range(COLS):
        for j in range(ROWS):
            for direction in DIRECTIONS:
                total_paths += path_finding(i, j, COLS, ROWS, grid, 0, direction)

    print(f'Total XMAS occurencies: {total_paths}')

def get_diag_indexes(i, j, ROWS, COLS):
    up = (i - 1 if i - 1 >= 0 else -1, j)
    down = (i + 1 if i + 1 < COLS else -1, j)
    left = (i, j - 1 if j - 1 >= 0 else -1)
    right = (i, j + 1 if j + 1 < ROWS else -1)

    left_up = (up[0], left[1])
    right_up = (up[0], right[1])
    left_down = (down[0], left[1])
    right_down = (down[0], right[1])

    return (left_up, right_up, left_down, right_down)

def check_x_mas(i, j, COLS, ROWS, grid):
    # Booleans to keep track of the answer
    left_top_down_diagonal_found = False
    right_top_down_diagonal_found = False

    left_up, right_up, left_down, right_down = get_diag_indexes(i, j, ROWS, COLS)

    # Get the indexes so we can check out of bounds
    # left-top-down
    left_up_i, left_up_j = left_up
    right_down_i, right_down_j = right_down

    # right-top-down
    right_up_i, right_up_j = right_up
    left_down_i, left_down_j = left_down

    # Check left up
    if (left_up_i < 0 or left_up_i >= COLS or left_up_j < 0 or left_up_j >= ROWS):
        return False
    # Check right down
    if (right_down_i < 0 or right_down_i >= COLS or right_down_j < 0 or right_down_j >= ROWS):
        return False
    # Check right up
    if (right_up_i < 0 or right_up_i >= COLS or right_up_j < 0 or right_up_j >= ROWS):
        return False
    # Check left down
    if (left_down_i < 0 or left_down_i >= COLS or left_down_j < 0 or left_down_j >= ROWS):
        return False

    # Check the left top down diagonal first
    # This could be either in order or reversed
    # So we have to check twice

    # Check in one order
    if (grid[left_up_i][left_up_j] == 'M' and grid[right_down_i][right_down_j] == 'S'):
        left_top_down_diagonal_found = True

    # Check in reverse order
    if (grid[left_up_i][left_up_j] == 'S' and grid[right_down_i][right_down_j] == 'M'):
        left_top_down_diagonal_found = True

    # Check in one order
    if (grid[right_up_i][right_up_j] == 'M' and grid[left_down_i][left_down_j] == 'S'):
        right_top_down_diagonal_found = True

    # Check in reverse order
    if (grid[right_up_i][right_up_j] == 'S' and grid[left_down_i][left_down_j] == 'M'):
        right_top_down_diagonal_found = True

    return (left_top_down_diagonal_found and right_top_down_diagonal_found)

def part_2(file_path):
    grid, ROWS, COLS = create_grid(file_path)

    print('X-MASes loop')
    total_x_mases = 0
    for i in range(COLS):
        for j in range(ROWS):
            # Only check the center of the X-MAS
            if grid[i][j] == 'A':
                # Check if we have an X-MAS
                if check_x_mas(i, j, COLS, ROWS, grid):
                    print(grid[i][j], end=" ")
                    total_x_mases += 1
                else:
                    print(".", end=" ")
            else:
                print(".", end=" ")
        print("")

    print(f'Total X_MASes: {total_x_mases}')

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python day-04.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]

    part_1(file_path)
    part_2(file_path)
