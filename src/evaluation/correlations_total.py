#!/usr/bin/env python3

import sys
sys.path.append("src")
from utils import load_json
import numpy as np

data = load_json("data/parsed.json")
xs_doc = []
xs_seg = []
features = [
    'spelling', 'terminology',
    'grammar', 'meaning', 'style', 'pragmatics',
    "overall"
]

for doc in data:
    for system_name, rating in doc["rating"].items():
        # TODO: hotfix unfinished data
        if any([v is None for v in rating.values()]):
            continue
        xs_doc.append([rating[f] for f in features])

    for line in doc["lines"]:
        for system_name, translation in line["translations"].items():
            # TODO: hotfix unfinished data
            if any([v is None for v in translation["rating"].values()]):
                continue
            xs_seg.append([translation["rating"][f] for f in features])

xs_doc = np.array(xs_doc)
xs_seg = np.array(xs_seg)

print(len(xs_doc), "doc ratings in total")
print(len(xs_seg), "seg ratings in total")
print()

# rotate to index by features
xs_doc = xs_doc.T
xs_seg = xs_seg.T

print("DOC correlations")
for f_i, f in enumerate(features):
    print(f"{f:>12}-overall: {np.corrcoef(xs_doc[f_i], xs_doc[-1])[0,1]:.2f}")
print("\nSEG correlations")
for f_i, f in enumerate(features):
    print(f"{f:>12}-overall: {np.corrcoef(xs_seg[f_i], xs_seg[-1])[0,1]:.2f}")