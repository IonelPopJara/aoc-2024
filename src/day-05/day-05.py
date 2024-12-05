def get_file_data(file_path, file_name):
    print('\tProcessing input data...')

    rule_index = {} # Here we will store the counter for the rules
    manuals = []
    manual_started = False

    input_file = file_path + file_name
    with open(input_file, 'r') as file:
        # print('\nRules:')
        for line in file:
            if line == "\n":
                manual_started = True
            elif not manual_started: # If we are checking a rule
                key, new_val = line.strip().split('|')

                current = []
                if key in rule_index:
                    current = rule_index[key]

                current.append(new_val)
                rule_index[key] = current
            else:
                manuals.append(line.strip().split(','))

    return rule_index, manuals

# Returns true if the manual checks the rules
def check_manual(manual, rules):
    for i, val in enumerate(manual):
        nums_before_val = manual[:i]
        val_rules = rules[val] if val in rules else []

        # To check the rules, the numbers in the rules, should always be after
        # If any of them is in the before list. It is wrong.
        # So we can check the intersection of the sets.
        common_elements = set(nums_before_val).intersection(val_rules)

        if common_elements:
            return False
            is_manual_valid = False

    return True

def middle_sum(manuals):
    total_middle_sum = 0
    # Check the middle number of each manual and sum them
    for manual in manuals:
        middle_idx = len(manual) // 2
        middle = manual[middle_idx]
        total_middle_sum += int(middle)

    return total_middle_sum

# `process_manuals` returns all the valid manuals
# and also the fixed invalid manuals.
def process_manuals(file_path, file_name):
    # At first I thought of using a dictionary and iterating over it
    # But what if I just count the rules. The number with the most
    # amount of rules should go first and the one with the least
    # amount will go last. If a number has no rules, we don't care.
    #
    # Update: that didn't work so I guess I'll try the first approach...
    # :)

    valid_manuals = []
    invalid_manuals = []
    rules, manuals = get_file_data(file_path, file_name)

    print('\tChecking manuals...')
    for manual in manuals:
        if check_manual(manual, rules):
            valid_manuals.append(manual)
        else:
            invalid_manuals.append(manual)

    # Fix the invalid manuals

    print(f'\tProcesing invalid manuals...')
    # This is essentially a stupid not so stupid bogosort
    for manual in invalid_manuals:
        i = 0
        while i < len(manual):
            val = manual[i]
            nums_before = manual[:i]
            rules_after = rules[val] if val in rules else []


            # If we found an intersection, i.e., the number in the wrong place
            common_elements = set(nums_before).intersection(rules_after)
            if common_elements:
                # Find the index of the problematic element
                element = next(iter(common_elements))
                index = manual.index(element)
                # Swap it and restart the loop
                manual[i], manual[index] = manual[index], manual[i]
                i = 0

            i+=1

    return valid_manuals, invalid_manuals

def main(file_path = ".", file_name = "input-00.txt"):
    valid_manuals, invalid_manuals = process_manuals(file_path, file_name)

    valid_middle_sum = middle_sum(valid_manuals)
    print(f'\tValid Middle Sum: {valid_middle_sum}')

    invalid_middle_sum = middle_sum(invalid_manuals)
    print(f'\tInvalid Middle Sum: {invalid_middle_sum}')

import sys
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python day-05.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]

    print("Checking Part 1:")
    print("input-00.txt")
    main(file_path, "input-00.txt")

    print("input-01.txt")
    main(file_path, "input-01.txt")

