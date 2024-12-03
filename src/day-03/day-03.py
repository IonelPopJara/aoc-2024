import sys
import re

# Read the input file,
# and process the information
def main(file_path):
    print('Part 1:')
    # Read input file
    txt = ""
    input_file = file_path + "input-01.txt"
    with open(input_file, 'r') as file:
        txt = file.read().rstrip()

    # Match all the elements that look like this
    # mul(digit 1-3 char, digi 1-3 char)
    match = r"mul\(\d{1,3},\d{1,3}\)"
    # Use regex to find the matches
    matches = re.findall(match, txt)
    total_mul = 0
    for res in matches:
        val = parse_mul(res)
        total_mul += val

    print(f'Total mult: {total_mul}')

def parse_mul(input_string):
    match = r"\d{1,3}"
    matches = re.findall(match, input_string)
    res = 1
    for i in matches:
        res *= int(i)

    return res

def part_2(file_path):
    print('Part 2')
    txt = ""
    # input_file = file_path + "input-02.txt"
    input_file = file_path + "input-01.txt"
    with open(input_file, 'r') as file:
        txt = file.read().rstrip()

    match = r"mul\(\d{1,3},\d{1,3}\)|do\(\)|don't\(\)"
    matches = re.findall(match,txt)
    print("Original matches")
    print(matches)

    valid_operations = []
    should_append = True
    for res in matches:
        if res == "don't()":
            should_append  = False
        elif res == "do()":
            should_append = True
        else:
            if should_append:
                valid_operations.append(res)

    print("New matches")
    print(valid_operations)

    total_shit = 0
    print("Numbers:")
    for i in valid_operations:
        wea = parse_mul(i)
        print(wea)
        total_shit += wea

    print(f'Total shit: {total_shit}')


# Setup to run the bash script
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python day-03.py <file_path>")
        sys.exit(1)
    file_path = sys.argv[1]
    main(file_path)
    part_2(file_path)

