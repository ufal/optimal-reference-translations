#!/usr/bin/env python3

import sys

import numpy as np
sys.path.append("src")
from utils import read_json, UID_MAP
import tqdm
import collections
import scipy.stats as st
import matplotlib.pyplot as plt
import fig_utils

def get_conf_interval(data):
    interval = st.t.interval(
        alpha=0.90, df=len(data) - 1,
        loc=np.mean(data),
        scale=st.sem(data)
    )
    return interval


data = read_json("data/parsed.json")
SYSTEMS = ["1", "2", "3", "4"]

data_lines = collections.defaultdict(list)

for doc in tqdm.tqdm(data):
    data_local = []
    for system_name in SYSTEMS:
        for line in doc["lines"]:
            translation = line["translations"][system_name]
            # TODO: hotfix unfinished data
            if any([x is None for x in translation["rating"].values()]):
                continue

            data_local.append(translation["rating"])

    data_lines[doc["uid"]] += data_local

data_out = []

for uid, uid_lines in data_lines.items():
    print(f"{uid:>10}:", end="")
    val_avg = np.average([x["overall"] for x in uid_lines])
    val_var = np.var([x["overall"] for x in uid_lines])
    print(f"{val_avg:>7.2f} ({val_var:>.2f})")
    data_out.append((val_avg, val_var, uid))

plt.figure(figsize=(8, 3))
ax = plt.gca()

COLORS = {
    "translator": "#9c2963",
    "student": "#965173",
    "nontranslator": "#6b1c44",
}

x_offset = 0
prev_expertise = "translator"

expertise_all = collections.defaultdict(list)

for uid_i, uid  in enumerate(UID_MAP.keys()):
    uid_lines = data_lines[uid]
    expertise = UID_MAP[uid]
    data_local = [x["overall"] for x in uid_lines]
    data_local_crop = [x for x in data_local if x >= 1]
    expertise_all[expertise] += data_local

    if prev_expertise != expertise:
        prev_expertise = expertise
        x_offset += 0.5 

    violin_parts = ax.violinplot(
        data_local_crop,
        positions=[uid_i + x_offset],
        showmeans=True,
        widths=1.8,
        showextrema=False,
        bw_method=0.2
    )
    for pc in violin_parts['bodies']:
        pc.set_facecolor(COLORS[expertise])
        pc.set_edgecolor('black')
        pc.set_linewidth(1.2)
        pc.set_alpha(0.75)
        pc.set_aa(True)


        # get the center
        m = np.mean(pc.get_paths()[0].vertices[:, 0])
        # modify the paths to not go further left than the center
        pc.get_paths()[0].vertices[:, 0] = np.clip(
            pc.get_paths()[0].vertices[:, 0],
            m, np.inf
        )

    violin_parts['cmeans'].set_linewidth(1.2)
    violin_parts['cmeans'].set_color("black")
    for p in violin_parts['cmeans'].get_paths():
        p.vertices[0, 0] += 0.45

    ax.set_xlim(-0.7, 12)

for expertise, expertise_data in expertise_all.items():
    print(f"{expertise}: {np.average(expertise_data):.2f}")

plt.xticks(
    [1.5, 5.5, 9.5],
    ["Translators", "Students", "Non-translators"]
)
plt.ylim(1, 6.1)
plt.ylabel("Overall score")
plt.tight_layout()
plt.savefig("figures/annotator_dist.pdf")
plt.show()