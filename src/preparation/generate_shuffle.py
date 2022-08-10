#!/usr/bin/env python3

raise Exception("This script is deprecated. Use `generate_xlsx.py` instead.")

from utils import load_data, load_data_structure, save_json
import random
import csv

data = load_data_structure()

UIDs = [
    "harare", "lusaka", "sahara", "cardiff", "hanoi",
    "caracas", "montevideo", "washington", "kampala", "funafuti",
    "ashgabat", "ankara", "tiraspol", "lome", "bangkok",
    "dodoma", "dushanbe", "damascus", "bern", "stockholm",
    "paramaribo", "khartoum", "madrid", "juba", "seoul",
    "pretoria", "hargeisa", "mogadishu", "honiara", "ljubljana",
    "bratislava", "philipsburg", "singapore", "freetown", "belgrade",
]

for uid_i, uid in enumerate(UIDs[:3]):
    random.seed(uid_i)
    new_data = []

    keys = list(data.keys())
    random.shuffle(keys)
    data_shuffled = [l for k in keys for l in data[k]]

    mapping = {"systems": [], "docs": keys, "doc_len": [len(data[k]) for k in keys]}

    for sent in data_shuffled:
        order = [1,2,3,4]
        random.shuffle(order)
        
        mapping["systems"].append(order)
        new_sent = []
        for i in order:
            new_sent.append(sent[i])

        # source is always first
        new_data.append([sent[0]] + new_sent)

    with open(f"data/translations_{uid}.csv", "w") as f:
        csv.writer(f, quoting=csv.QUOTE_ALL).writerows(new_data)

    save_json(f"data/mapping_{uid}.json", mapping)