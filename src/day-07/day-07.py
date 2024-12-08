from itertools import product

def get_op_permutations(n_operators):
    # Even though we have to use ||,
    # I'll use | to make it simple
    operators = "+*|"

    p = list(product(operators, repeat=n_operators))

    p = [list(comb) for comb in p]

    return p

def is_equation_solvable(target, operation):
    target = int(target)

    total = 0
    current_operator = ''
    for item in operation:
        # If we see a number and we already have an operator
        if item != '+' and item != '*' and item != '|' and current_operator != '':
            # Calculate
            if current_operator == '+':
                total = total + int(item)
            elif current_operator == '*':
                total = total * int(item)
            elif current_operator == '|':
                total = int(str(total) + str(item))
        # If we see a number and we don't have any operator
        elif item != '+' and item != '*' and item != '|' and current_operator == '':
            # Add first number
            total += int(item)
        elif item == '+':
            current_operator = '+'
        elif item == '*':
            current_operator = '*'
        elif item == '|':
            current_operator = '|'

    if total == target:
        return True
    else:
        return False

def part_1(file_path):
    input_file = file_path + "input-01.txt"
    with open(input_file, 'r') as file:
        lines = file.read().strip().split("\n")
        equations = [line.split() for line in lines]

    solvable_test_values = []
    # Iterate through the equations
    for equation in equations:
        n_operators = len(equation) - 2 # 2 because the first element is the target
        # Get all the possible permutations of operators
        op_permutations = get_op_permutations(n_operators)

        # print(op_permutations)

        solvable = False

        # Test the operators
        for p in op_permutations:
            operation = []
            for idx, operand in enumerate(equation[1: len(equation) - 1]):
                operation.append(operand)
                operation.append(p[idx])
            operation.append(equation[-1])
            target = equation[0].split(':')[0]

            # print(f'{target} = {operation}')

            if is_equation_solvable(target, operation):
                # Add it to the test values to be sum
                # I can optimize the double checking
                # but I'm too lazy rn
                # solvable_test_values.add(int(target))
                solvable = True

        if solvable:
            solvable_test_values.append(int(target))
            continue

    # Sum the test values
    print(f'Solvable: {solvable_test_values}')
    print(f'\tSum: {sum(solvable_test_values)}')

import sys
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f'Usage: python day-07.py <file_path>')
        sys.exit(1)

    file_path = sys.argv[1]
    part_1(file_path)

