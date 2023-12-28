#!/usr/bin/env python3

import collections
import sys
sys.path.append("src")
from utils import load_json, load_wmt, save_json

data_ort = load_json("data/annotations.json")
data_wmt = load_wmt()

FIRST_ROUND_TO_NAME = {
    # worst to best
    "3": "R1",
    "2": "R2",
    "1": "R3",
    "4": "R4",
}

src_to_ref = collections.defaultdict(list)
for doc in data_ort:
    for line in doc["lines"]:
        for translation_v, translation_k in line["translations"].items():
            translation_v = FIRST_ROUND_TO_NAME[translation_v]
            src_to_ref[line["source"]].append((translation_k["orig"], translation_v))
            src_to_ref[line["source"]].append((translation_k["done"], f"PE {doc['expertise']} {translation_v}"))

for line in data_wmt:
    line["ref"] = src_to_ref[line["src"]]


save_json("computed/metric_scores_none.json", data_wmt)