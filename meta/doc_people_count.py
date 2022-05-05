#!/usr/bin/env python3
from math import ceil

BUDGET_MAX = 60000
BUDGET_MIN = 40000

print(f"{'People':<10}", f"{'Docs':<10}", f"{'Cost (k)':<10}", sep="")

for group_size in range(3, 7):
    for docs in range(15, 30):
        single_annotation_avg = docs * 45/60 * 200
        cost = single_annotation_avg * group_size * 3
        if cost <= BUDGET_MAX and cost >= BUDGET_MIN:
            print(f"{group_size*3:<10}{docs:<10}{ceil(cost/1000):<10}")