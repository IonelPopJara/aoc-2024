'''
j
0        9 i
....#..... 0
.........#
..........
..#.......
.......#..
..........
.#..^..... start = (6, 4)
........#.
#.........
......#... 9
'''

DIRECTIONS = [
  # (i, j)
    (-1, 0),    # UP (i -= 1)
    (0, 1),     # RIGHT (j += 1)
    (1, 0),     # DOWN (i += 1)
    (0, -1),    # LEFT (j -= 1)
]

def print_grid(grid):
    print("---GRID---")
    for line in grid:
        for item in line:
            print(item, end="")
        print("")
    print("---GRID---")

def run_simulation(grid, ROWS, COLS, current_pos):
    is_guard_visible = True
    current_direction = 0 # Apparently it starts facing up all the time (for now)

    while is_guard_visible:
        # Set an X for our current position
        grid[current_pos[0]][current_pos[1]] = "X"
        # Calculate the next step
        facing = DIRECTIONS[current_direction]

        next_pos = [current_pos[0] + facing[0], current_pos[1] + facing[1]]
        # Check if the next step is outside of bounds
        if (next_pos[0] < 0 or next_pos[0] >= ROWS) or (next_pos[1] < 0 or next_pos[1] >= COLS):
            # The guard is outside of bounds so we finish the counting
            is_guard_visible = False
            break
        elif grid[next_pos[0]][next_pos[1]] == '#': # If we are facing an obstacle
            # Rotate 90 degrees to the right
            current_direction = (current_direction + 1) % len(DIRECTIONS)
        else:
            # Our next step is valid
            current_pos = next_pos

    x_counter = 0
    for row in grid:
        for col in row:
            if col == "X":
                x_counter += 1

    return x_counter

def run_simulation_2(grid, ROWS, COLS, current_pos):
    is_guard_visible = True
    current_direction = 0 # Apparently it starts facing up all the time (for now)

    max_steps = 100000
    step_counter = 0

    # Brutforce it
    while step_counter <= max_steps:
        # Set an X for our current position
        # grid[current_pos[0]][current_pos[1]] = "X"
        # Calculate the next step
        facing = DIRECTIONS[current_direction]

        next_pos = [current_pos[0] + facing[0], current_pos[1] + facing[1]]
        # Check if the next step is outside of bounds
        if (next_pos[0] < 0 or next_pos[0] >= ROWS) or (next_pos[1] < 0 or next_pos[1] >= COLS):
            # The guard is outside of bounds so we finish the counting
            is_guard_visible = False
            return False
        elif grid[next_pos[0]][next_pos[1]] == '#': # If we are facing an obstacle
            # Rotate 90 degrees to the right
            current_direction = (current_direction + 1) % len(DIRECTIONS)
        else:
            # Our next step is valid
            current_pos = next_pos
            step_counter += 1

    return True

def main(file_path):
    # Get the initial map
    input_file = file_path + "input-01.txt"
    with open(input_file, 'r') as file:
        lines = file.read().strip().split("\n")
        grid = [list(line) for line in lines]

    ROWS = len(grid)
    COLS = len(grid[0]) # I'll assume that the columns are all the same length

    # Do another pass to get the starting position
    # because I'm too lazy to change the previous loop
    for idx, row in enumerate(grid):
        for jdx, col in enumerate(row):
            if col == "^":
                current_pos = [idx, jdx]
                break

    original_starting_pos = current_pos
    original_grid = [row[:] for row in grid]

    # Print the map for fun
    print(f'Initial Map:')
    print(f'\tROWS: {ROWS} | COLS: {COLS}')
    print(f'\tStarting Pos: {current_pos}')
    print_grid(grid)

    is_guard_visible = True
    current_direction = 0 # Apparently it starts facing up all the time (for now)

    x_counter = run_simulation(grid, ROWS, COLS, current_pos)

    print(f'The guard has visited: {x_counter} unique positions')

    # Bruteforce part 2
    print("Part 2: Bruteforce")
    print_grid(original_grid)

    loop_counter = 0
    for i in range(len(original_grid)):
        for j in range(len(original_grid[0])):
            if original_grid[i][j] == '.':
                # Create a copy of the grid to put the obstacle
                temp_grid = [row[:] for row in original_grid]
                # Run the simulation on the temp_grid here
                temp_grid[i][j] = '#'
                starting_pos = original_starting_pos
                loop = run_simulation_2(temp_grid, ROWS, COLS, starting_pos)
                if loop:
                    loop_counter += 1

    print(f'Loops: {loop_counter}')


import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python day-06.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    main(file_path)
