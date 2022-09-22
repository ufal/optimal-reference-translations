#!/usr/bin/env python3

import collections
import sys
sys.path.append("src")
from utils import read_json
import numpy as np
from scipy.stats import spearmanr

data = read_json("data/parsed.json")
d_seg = collections.defaultdict(list)
d_doc = collections.defaultdict(list)
d_seg_uid = collections.defaultdict(dict)
d_doc_uid = collections.defaultdict(lambda: collections.defaultdict(list))

for doc in data:
    for line in doc["lines"]:
        d_seg[line["source"]].append(line["translations"])
        d_seg_uid[line["source"]][doc["uid"]] = line["translations"]

    d_doc[doc["doc"]].append(doc["rating"])
    d_doc_uid[doc["doc"]][doc["uid"]].append(doc["rating"])

uids = list(list(d_seg_uid.values())[0].keys())

all_corrs = []
all_corrs_sys = collections.defaultdict(list)

for uid1_i, uid1 in enumerate(uids):
    data_flat_1 = []
    for seg_v in d_seg_uid.values():
        data_flat_1.append(seg_v[uid1])
    for uid2 in uids[uid1_i + 1:]:
        data_flat_2 = []
        for seg_v in d_seg_uid.values():
            data_flat_2.append(seg_v[uid2])

        print(uid1, uid2)
        for system in ["1", "2", "3", "4"]:
            data_system_1 = [x[system]["rating"]["overall"] for x in data_flat_1]
            data_system_2 = [x[system]["rating"]["overall"] for x in data_flat_2]
            data_system_all = np.array([
                (x, y) for x, y
                in zip(data_system_1, data_system_2)
                if x is not None and y is not None
            ])
            corr = np.corrcoef(data_system_all.T)[0, 1]

            print(f"{system}: {corr:4.2}")
            all_corrs.append(corr)
            all_corrs_sys[system].append(corr)
        

all_corrs = [x for x in all_corrs if not np.isnan(x)]
print(f"All corrs avg: {np.average(all_corrs):.2f}")
for system in ["1", "2", "3", "4"]:
    corrs_local = [x for x in all_corrs_sys[system] if not np.isnan(x)]
    print(f"{system} corrs avg: {np.average(corrs_local):.2f}")
