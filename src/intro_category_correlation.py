#!/usr/bin/env python3

from utils import save_json, read_json
import json
from collections import defaultdict
import numpy as np

data = read_json("data/parsed.json")
hits_inconsistency = 0
hits_total = 0
xs = []
# hack, assume that all ratings have the same order
features = None

for doc in data:
    for line in doc["lines"]:
        for system_name, translation in line["translations"].items():
            # TODO: hotfix unfinished dataa
            if translation["rating"]["overall"] is None or translation["rating"]["pragmatics"] is None:
                continue
            if translation["rating"]["overall"] == 6 and any([x < 6 for x in translation["rating"].values()]):
                hits_inconsistency += 1
            hits_total += 1
            xs.append(
                [y for y in translation["rating"].values()]
            )
            if features is None:
                features = [x for x in translation["rating"].keys()]

print(
    "Rating = 6 but something else < 6:",
    f"{hits_inconsistency/hits_total:.1%}"
)

print(", ".join(features))
print(np.round(np.corrcoef(np.array(xs).T),1))