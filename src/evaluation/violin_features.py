#!/usr/bin/env python3

import sys
sys.path.append("src")
from utils import read_json
import fig_utils
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

data = read_json("data/parsed.json")
xs_doc = []
xs_seg = []
features = [
    'spelling', 'terminology',
    'grammar', 'meaning', 'style', 'pragmatics',
    "overall"
]

for doc in data:
    for system_name, rating in doc["rating"].items():
        # TODO: hotfix unfinished data
        if any([v is None for v in rating.values()]):
            continue
        xs_doc.append([rating[f] for f in features])

    for line in doc["lines"]:
        for system_name, translation in line["translations"].items():
            # TODO: hotfix unfinished data
            if any([v is None for v in translation["rating"].values()]):
                continue
            xs_seg.append([translation["rating"][f] for f in features])

xs_doc = np.array(xs_doc)
xs_seg = np.array(xs_seg)

COLORS = ["#9c2963", "#fb9e07"]


def draw_scatter(ax, xs, label):
    f_means = np.mean(xs, axis=0)
    # rotate so that each inside list is for a single array
    xs = xs.T
    # clip data
    xs = [[x for x in x_r if x >= 2] for x_r in xs]
    violin_parts = ax.violinplot(
        xs,
        showmeans=True,
        widths=1,
        showextrema=False,
    )
    for pc in violin_parts['bodies']:
        pc.set_facecolor(COLORS[0])
        pc.set_edgecolor('black')
        pc.set_linewidth(1.2)
        pc.set_alpha(0.75)
        pc.set_aa(True)
    violin_parts['cmeans'].set_linewidth(1.2)
    violin_parts['cmeans'].set_color("black")
    ax.set_yticks(
        [2,3,4,5,6],
        [2,3,4,5,6],
    )

    for f_i, f_mean in enumerate(f_means):
        # I have no idea why we have to divide by 7.7 and not 6
        # but this aligns the text labels good
        ax.text(
            (f_i)/7.7+0.05, 0.1,
            f"{f_mean:.1f}",
            ha="left",
            transform=ax.transAxes,
            # fontsize=8.5,
        )

    if label == "docs":
        ax.set_xticks([], [])
    else:
        ax.set_xticks(
            [x_i + 1 for x_i, x in enumerate(features)],
            [("\n" if x_i % 2 else "") + x.title()
             for x_i, x in enumerate(features)]
        )
    ax.set_ylabel("Rating " + r"$\bf{" + label + "}$")


plt.figure(figsize=(5, 4))
draw_scatter(
    plt.subplot(2, 1, 1),
    xs_doc,
    "docs",
)
draw_scatter(
    plt.subplot(2, 1, 2),
    xs_seg,
    "segments"
)

# address the last one
plt.tight_layout(pad=0)
plt.savefig("figures/violin_features.pdf")
plt.show()