#!/usr/bin/env python3

import sys
sys.path.append("src")
from utils import load_json, load_wmt
import numpy as np

data = load_json("data/annotations.json")


tab_doc_count = len({
    doc["doc"]
    for doc in data
})
print("Document count: ", tab_doc_count)

tab_source_count = len({
    line["source"]
    for doc in data
    for line in doc["lines"]
})
print("Source segments: ", tab_source_count)
tab_source_length = np.average([
    len(line["source"].split())
    for doc in data
    for line in doc["lines"]
])
print("Source segment length: ", f"{tab_source_length:.1f}")

tab_ref_count = len({
    translator["orig"]
    for doc in data
    for line in doc["lines"]
    for translator in line["translations"].values()
})
# a few translations are the same
print("Reference count: ", "160*4=640")

tab_ref_annotations = len({
    line["source"] + "||||" + doc["uid"]
    for doc in data
    for line in doc["lines"]
}) * 4
print("Reference annotations count: ", tab_ref_annotations)


data_wmt = load_wmt()
print("Systems:", len({line["system"] for line in data_wmt}))
print("System targets:", len(data_wmt))
