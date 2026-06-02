#!/usr/bin/env python3
import sys

# Input format: person_id, district_id, personal_income
# Example: 10021,2,120000

for line in sys.stdin:
    line = line.strip()
    # Skip empty lines
    if not line:
        continue

    parts = line.split(',')

    if len(parts) == 3:
        person_id = parts[0]
        district_id = parts[1]
        income = parts[2]
        # Emit key-value pair: district_id \t income
        # We print to stdout, which Hadoop captures
        print("{}\t{}".format(district_id, income))
