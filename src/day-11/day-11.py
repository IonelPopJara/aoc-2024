from collections import defaultdict
import sys

def print_layout(input_layout):
    formatted_layout = " ".join(input_layout)
    print(formatted_layout)

# 125 17
def blink(stones_dict):
    new_stones_dict = defaultdict(int)

    for stone, count in stones_dict.items():
        if stone == 0: # 1st Rule
            new_stones_dict[1] += count
        elif (len(str(stone)) % 2 == 0): # 2nd Rule
            str_stone = str(stone)
            first_half = int(str_stone[:len(str_stone) // 2])
            second_half = int(str_stone[len(str_stone) // 2:])

            new_stones_dict[first_half] += count
            new_stones_dict[second_half] += count
        else:
            new_stones_dict[int(stone) * 2024] += count

    return new_stones_dict

def main(file_path):
    input_file = file_path + "input-01.txt"

    with open(input_file, 'r') as file:
        stones = file.read().strip().split()

    stones_dict = defaultdict(int)
    for stone in stones:
        stones_dict[int(stone)] = 1

    print(f'Stones: {stones_dict}')

    p_25 = stones_dict.copy()
    for i in range(75):
        p_25 = blink(p_25)

    print(f'After blinking {i + 1} times: {sum(p_25.values())}')

import sys
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python day-11.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    main(file_path)

