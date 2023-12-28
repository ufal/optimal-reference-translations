#!/usr/bin/env python3

from utils import load_json
from collections import defaultdict

data = load_json("data/parsed.json")
sentlevel = defaultdict(lambda: defaultdict(list))
sent_targets = set()

for doc in data:
    for line in doc["lines"]:
        for system_name, translation in line["translations"].items():
            sent_targets.add(translation["orig"])
            for rating_name, rating_value in translation["rating"].items():
                # TODO: hotfix unfinished data
                if rating_value is None:
                    continue
                sentlevel[system_name][rating_name].append(rating_value)

sentlevel_flat = [
    r
    for rating in sentlevel.values()
    for rating_system in rating.values()
    for r in rating_system
]

# 50k evaluations
print(len(sentlevel_flat))
print(len(sent_targets))