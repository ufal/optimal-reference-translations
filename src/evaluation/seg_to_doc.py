#!/usr/bin/env python3

import sys

import numpy as np
sys.path.append("src")
from utils import CATEGORIES, read_json
import tqdm

data = read_json("data/parsed.json")
ys = []
xs = []

SYSTEMS = ["1", "2", "3", "4"]

for doc in tqdm.tqdm(data):
    for system_name in SYSTEMS:
        # TODO: hotfix unfinished data
        if any([doc["rating"][system_name][c] is None for c in CATEGORIES]):
            continue
        ys.append([doc["rating"][system_name][c] for c in CATEGORIES])

        data_lines = []
        for line in doc["lines"]:
            translation = line["translations"][system_name]
            # TODO: hotfix unfinished data
            if any([x is None for x in translation["rating"].values()]):
                continue

            data_lines.append([float(translation["rating"][c]) for c in CATEGORIES])

        ratings = np.array(data_lines)
        xs_min = ratings.min(axis=1)
        xs_max = ratings.max(axis=1)
        xs_avg = np.average(ratings, axis=1)
        xs_med = np.median(ratings, axis=1)
        xs.append(np.array([xs_min, xs_max, xs_avg, xs_med]))

print(" "*16 + "".join([f"{x:>6} " for x in ["MIN", "MAX", "AVG", "MED"]]))

for category_i, category in enumerate(CATEGORIES):
    print(f"{category.title():>15}:", end="")
    # select overall
    ys_local = [y[category_i] for y in ys]
    xs_local = [x[:,category_i] for x in xs]
    corr_min = np.corrcoef(ys_local, [x[0] for x in xs_local])[0,1]
    corr_max = np.corrcoef(ys_local, [x[1] for x in xs_local])[0,1]
    corr_avg = np.corrcoef(ys_local, [x[2] for x in xs_local])[0,1]
    corr_med = np.corrcoef(ys_local, [x[3] for x in xs_local])[0,1]
    print(f"{corr_min:>6.2f} {corr_max:>6.2f} {corr_avg:>6.2f} {corr_med:>6.2f}")


# LaTeX output

print("\\toprule")
print("\\textbf{Category} & " + " & ".join(["\\textbf{" + x + "}" for x in ["min", "max", "avg", "med"]]) + "\\\\")
print("\\midrule")

for category_i, category in enumerate(CATEGORIES):
    # category_head = "\\textbf{" + category.title() + "} &"
    category_head = "{" + category.title() + "} &"
    print(f"{category_head:<25}", end="")
    # select overall
    ys_local = [y[category_i] for y in ys]
    xs_local = [x[:,category_i] for x in xs]
    corr_min = np.corrcoef(ys_local, [x[0] for x in xs_local])[0,1]
    corr_max = np.corrcoef(ys_local, [x[1] for x in xs_local])[0,1]
    corr_avg = np.corrcoef(ys_local, [x[2] for x in xs_local])[0,1]
    corr_med = np.corrcoef(ys_local, [x[3] for x in xs_local])[0,1]
    print(f"{corr_min:>6.2f} & {corr_max:>6.2f} & {corr_avg:>6.2f} & {corr_med:>6.2f} \\\\")
print("\\bottomrule")