#!/usr/bin/env python3

import collections
import sys
sys.path.append("src")
from utils import load_json
import numpy as np
from scipy.stats import spearmanr

data = load_json("data/parsed.json")
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
total_order = 0
same_order = 0
p1_order = 0

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

        for l1, l2 in zip(data_flat_1, data_flat_2):
            l1 = [(s, v["rating"]["overall"]) for s,v in l1.items()]
            l2 = [(s, v["rating"]["overall"]) for s,v in l2.items()]
            if any([x[1] is None for x in l1]):
                continue
            if any([x[1] is None for x in l2]):
                continue
            # sort with stabilizer
            sorted1 = sorted(l1, key=lambda x: x[1] + int(x[0])/10)
            sorted2 = sorted(l2, key=lambda x: x[1] + int(x[0])/10)
            total_order += 1
            if all([x[0] == y[0] for x,y in zip(sorted1, sorted2)]):
                same_order += 1
            else:
                sorted1 = [x[0] for x in sorted1]
                sorted2 = [x[0] for x in sorted2]
                for (s1_i, s1), (s2_i, s2) in zip(enumerate(sorted1), enumerate(sorted2)):
                    if s1 != s2:
                        index_s2 = sorted1.index(s2)
                        sorted1[s1_i] = s2
                        # perform one swap
                        sorted1[index_s2] = s1
                        break
                if all([x == y for x,y in zip(sorted1, sorted2)]):
                    p1_order += 1


all_corrs = [x for x in all_corrs if not np.isnan(x)]
print(f"All corrs avg: {np.average(all_corrs):.2f}")
for system in ["1", "2", "3", "4"]:
    corrs_local = [x for x in all_corrs_sys[system] if not np.isnan(x)]
    print(f"{system} corrs avg: {np.average(corrs_local):.2f}")

print(f"Same order: {same_order}/{total_order}")
print(f"P1 order: {p1_order}/{total_order}")