#!/usr/bin/env python3
import sys

current_district = None
current_sum = 0.0
current_count = 0

for line in sys.stdin:
    line = line.strip()

    # Parse the input from mapper
    try:
        district, income = line.split('\t')
        income = float(income)
    except ValueError:
        # If line is malformed, skip it
        continue

    # this IF-switch only works because Hadoop sorts map output
    # by key (here: district) before it is passed to the reducer
    if current_district == district:
        current_sum += income
        current_count += 1
    else:
        if current_district:
            # write result to STDOUT
            print("{}\t{:.2f}".format(current_district, current_sum / current_count))
        current_district = district
        current_sum = income
        current_count = 1

# do not forget to output the last district if needed!
if current_district == district:
    print("{}\t{:.2f}".format(current_district, current_sum / current_count))
