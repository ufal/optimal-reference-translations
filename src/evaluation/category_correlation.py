#!/usr/bin/env python3

import sys
sys.path.append("src")
from utils import read_json
import numpy as np
import fig_utils
import utils
import matplotlib.pyplot as plt
import matplotlib as mpl


def get_color(val):
    if val > 0.6:
        return "black"
    else:
        return "white"

data = read_json("data/parsed.json")
hits_inconsistency = 0
hits_total = 0
xs = []
xs_doc = []

for doc in data:
    for line in doc["lines"]:
        for system_name, translation in line["translations"].items():
            # TODO: hotfix unfinished data
            if any([x is None for x in translation["rating"].values()]):
                continue
            if translation["rating"]["overall"] == 6 and any([x < 6 for x in translation["rating"].values()]):
                hits_inconsistency += 1
            hits_total += 1
            xs.append(
                [y for y in translation["rating"].values()]
            )
    for system_name, translation in doc["rating"].items():
            # TODO: hotfix unfinished data
            if any([x is None for x in translation.values()]):
                continue
            xs_doc.append(
                [y for y in translation.values()]
            )

print(
    "Rating = 6 but something else < 6:",
    f"{hits_inconsistency/hits_total:.1%}"
)

corrs = np.corrcoef(np.array(xs).T)
corrs[np.triu_indices(len(corrs))] = None
print(np.round(corrs, 2))
# crop correlations
corrs = corrs[1:,:-1]

corrs_doc = np.corrcoef(np.array(xs_doc).T)
corrs_doc[np.triu_indices(len(corrs_doc))] = None
print(np.round(corrs_doc, 2))
# crop correlations
corrs_doc = corrs_doc[1:,:-1]

VMIN = 0.4
VMAX = 0.9

# plotting
plt.figure(figsize=(5, 2.7))
ax = plt.gca()
cmap = mpl.cm.get_cmap("inferno").copy()
plt.imshow(corrs, cmap=cmap, vmin=VMIN, vmax=VMAX, aspect=0.7)


# add doc-level trinagles and texts
for s_i, s in enumerate(utils.CATEGORIES[1:]):
    for a_i, a in enumerate(utils.CATEGORIES[:-1]):
        result = corrs_doc[s_i, a_i]
        triangle = plt.Polygon(
            np.array([[a_i, s_i], [a_i + 1, s_i], [a_i, s_i + 1]]) - 0.5,
            # color input needs to be normalized
            color=cmap((result - VMIN) / (VMAX - VMIN))
        )
        ax.add_patch(triangle)
        plt.text(
            a_i - 0.2, s_i - 0.25, f"{result:.2f}".replace("0.", "."),
            ha="center", va="center", color=get_color(result),
        )


        result=  corrs[s_i,a_i]
        plt.text(
            a_i + 0.2, s_i + 0.25, f"{result:.2f}".replace("0.", "."),
            ha="center", va="center", color=get_color(result),
        )


plt.colorbar(
    cmap=cmap, shrink=0.65, aspect=10, anchor=(0, 0.0),
    ticks=np.round(np.linspace(VMIN, VMAX, num=5), 2),
)
plt.yticks(
    range(len(utils.CATEGORIES[1:])), 
    [x.title() for x in utils.CATEGORIES[1:]]
)
plt.xticks(
    list(range(len(utils.CATEGORIES[:-1]))),
    [("\n" if x_i % 2 else "") + x.title()
     for x_i, x in enumerate(utils.CATEGORIES[:-1])],
)

# add "legend"
triangle = plt.Polygon(
    np.array([[5.75, -0.5], [6 + 1, -0.5], [5.75, 0.75]]),
    # color input needs to be normalized
    facecolor=cmap((0.57 - VMIN) / (VMAX - VMIN)),
    edgecolor="black",
    clip_on=False,
    linewidth=1.5,
)
ax.add_patch(triangle)
triangle = plt.Polygon(
    np.array([[6 + 1, 0.75], [6 + 1, -0.5], [5.75, 0.75]]),
    # color input needs to be normalized
    facecolor=cmap((0.8 - VMIN) / (VMAX - VMIN)),
    edgecolor="black",
    clip_on=False,
    linewidth=1.5,
)
ax.add_patch(triangle)
plt.text(
    6.1, -0.2, "Doc.",
    ha="center", va="center", color="white",
)
plt.text(
    6.55, 0.47, "Sent.",
    ha="center", va="center", color="black",
)
plt.tight_layout(pad=0, rect=[0.05, -0.01, 0.98, 1])
plt.savefig("figures/category_correlation.pdf")
plt.show()