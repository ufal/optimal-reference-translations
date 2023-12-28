#!/usr/bin/env python3

from utils import load_json
from collections import defaultdict

data = load_json("data/parsed.json")
sentlevel = defaultdict(lambda: defaultdict(list))
sentpairs = []
time = []

for doc in data:
    for line in doc["lines"]:
        for system_name, translation in line["translations"].items():
            for rating_name, rating_value in translation["rating"].items():
                # TODO: hotfix unfinished data
                if rating_value is None:
                    continue
                sentlevel[system_name][rating_name].append(rating_value)

            # store sentence pairs
            if translation["orig"] is not None:
                sentpairs.append((translation["orig"], translation["done"]))

    time.append(doc["time"])

sentlevel_flat = [
    r
    for rating in sentlevel.values()
    for rating_system in rating.values()
    for r in rating_system
]

# * Kolik procent hodnocení (vyjma těch maximálních=6) je neceločíselných?
print("\n")
print(f"Total ratings: {len(sentlevel_flat)}")
print(
    "Non-integer rating excluding 6 (perc.):",
    f"{sum([x!=int(x) for x in sentlevel_flat if x != 6])/len([x for x in sentlevel_flat if x != 6]):.0%}"
)
print(
    "Non-integer rating (perc.):"
    f"{sum([x!=int(x) for x in sentlevel_flat])/len(sentlevel_flat):.0%}"
)
print(
    "Rating 6 (perc.):",
    f"{sum([x==6 for x in sentlevel_flat])/len(sentlevel_flat):.0%}"
)

total_doc_rating = 0
for doc in data:
    for system_name, translation in doc["rating"].items():
        for rating_name, rating_value in translation.items():
            # TODO: hotfix unfinished data
            if rating_value is None:
                continue
            total_doc_rating += 1

print(f"Total doc ratings: {total_doc_rating}")
