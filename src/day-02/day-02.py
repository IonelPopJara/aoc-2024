def is_report_valid(input_report):
    is_safe = True

    # Manage order
    is_increasing = False
    if (input_report[0] <= input_report[1]):
        is_increasing = True

    i = 0
    while i < len(input_report) - 1:
        # Check if the input_report is in order (either ascending or descending)
        is_sorted = (is_increasing and input_report[i] <= input_report[i + 1]) or (not is_increasing and input_report[i] >= input_report[i + 1])

        # Check adj diff condition
        adj_diff = abs(input_report[i] - input_report[i + 1])
        if (not (1 <= adj_diff <= 3)) or (not is_sorted):
            is_safe = False
            break

        i+=1

    if is_safe:
        return True
    else:
        return False

def main(file_path):

    file_src = file_path + "input-01.txt"
    reports = []

    with open(file_src) as file:
        for line in file:
            reports.append([int (x) for x in line.strip().split()])

    total_safe_reports = 0

    # NOTE: A report is safe if it's either increasing or decreasing
    # and the levels differ by at least 1 and are most 3.

    # Processing
    for report in reports:
        if is_report_valid(report):
            total_safe_reports += 1
        else:
            # print(f'Report {report} is not safe')
            for i, lvl in enumerate(report):
                # Since the Problem Dampener was implemented
                # we can tolerate 1 mistake
                new_report = report[:i] + report[i + 1:]
                is_new_valid = is_report_valid(new_report)
                # print(f'{new_report} -> {is_new_valid}')
                if is_new_valid:
                    total_safe_reports += 1
                    break

    print(f'Total safe reports: {total_safe_reports}')

import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python day-02.py <file_path>")
        sys.exit(1)
    file_path = sys.argv[1]
    main(file_path)
