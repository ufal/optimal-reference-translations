#!/usr/bin/env python3

from utils import read_json
from collections import defaultdict
import numpy as np

data = read_json("data/parsed.json")
doclevel = defaultdict(lambda: defaultdict(list))
sentlevel = defaultdict(lambda: defaultdict(list))
sentpairs = []
time = []

for doc in data:
    for system_name, rating in doc["rating"].items():
        for rating_name, rating_value in rating.items():
            # TODO: hotfix unfinished dataa
            if rating_value is None:
                continue
            doclevel[system_name][rating_name].append(rating_value)
    for line in doc["lines"]:
        for system_name, translation in line["translations"].items():
            for rating_name, rating_value in translation["rating"].items():
                # TODO: hotfix unfinished dataa
                if rating_value is None:
                    continue
                sentlevel[system_name][rating_name].append(rating_value)

            # store sentence pairs
            if translation["orig"] is not None:
                sentpairs.append((translation["orig"], translation["done"]))

    time.append(doc["time"])

doclevel = {
    system_name: {
        attribute: np.average(rating_values)
        for attribute, rating_values in rating.items()
    }
    for system_name, rating in doclevel.items()
}
sentlevel_flat = [
    r
    for rating in sentlevel.values()
    for rating_system in rating.values()
    for r in rating_system
]

sentlevel = {
    system_name: {
        attribute: np.average(rating_values)
        for attribute, rating_values in rating.items()
    }
    for system_name, rating in sentlevel.items()
}


def print_table(data):
    data = [data[str(i)] for i in [1, 2, 3, 4]]
    attributes = list(data[0].keys())
    print("            P1   P2   P3   N1")
    for k in attributes:
        print(f"{k:<12}", *[f"{data[i][k]:<.1f}  " for i in range(4)], sep="")


print("DOC-LEVEL")
print_table(doclevel)
print()
print("SENT-LEVEL")
print_table(sentlevel)

print(f"Average time: {np.average(time):.0f} min")

# * Dodržují anotátoři pravidlo, že při overall<6 vyplní posteditaci?
print("\n")
print(f"Sentence pairs total: {len(sentpairs)}")
print(
    "Post-edited (perc.):",
    f"{sum([x!=y for x,y in sentpairs])/len(sentpairs):.0%}"
)