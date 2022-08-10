#!/usr/bin/env python3

from utils import read_json
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

data = read_json("data/parsed.json")
doclevel = defaultdict(lambda: defaultdict(list))
sentlevel = defaultdict(lambda: defaultdict(list))
sentpairs = []
time = []

for doc in data:
    for system_name, rating in doc["rating"].items():
        for rating_name, rating_value in rating.items():
            # TODO: hotfix unfinished dataa
            try:
                rating_value = float(rating_value)
                doclevel[system_name][rating_name].append(rating_value)
            except:
                print(rating_value)

    for line in doc["lines"]:
        for system_name, translation in line["translations"].items():
            for rating_name, rating_value in translation["rating"].items():
                # TODO: hotfix unfinished dataa
                try:
                    float(rating_value)
                    sentlevel[system_name][rating_name].append(rating_value)
                except:
                    print(rating_value)

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

# TODO: move these misc. things somewhere else
print(f"Average time: {np.average(time):.0f} min")

# * Dodržují anotátoři pravidlo, že při overall<6 vyplní posteditaci?
print("\n")
print(f"Sentence pairs total: {len(sentpairs)}")
print(
    "Post-edited (perc.):",
    f"{sum([x!=y for x,y in sentpairs])/len(sentpairs):.0%}"
)

attributes = list(sentlevel["1"].keys())

plt.figure(figsize=(5, 2.7))
ax = plt.gca()
img = np.full((4, len(attributes)), fill_value=np.nan)

cmap = mpl.cm.get_cmap("inferno").copy()

plt.xticks(
    list(range(len(attributes))),
    [("\n" if x_i % 2 else "") + x.title()
     for x_i, x in enumerate(attributes)],
)
plt.yticks(list(range(4)), ["P1", "P2", "P3", "N1"])
VMIN = 4.8
VMAX = 6

def get_color(val):
    if val > 5.4:
        return "black"
    else:
        return "white"

for s_i, s in enumerate(["1", "2", "3", "4"]):
    for a_i, a in enumerate(attributes):
        result = doclevel[s][a]
        img[s_i, a_i] = result
        plt.text(
            a_i+0.2, s_i +0.25, f"{result:.1f}",
            ha="center", va="center", color=get_color(result),
        )

        result = sentlevel[s][a]
        
        triangle = plt.Polygon(
            np.array([[a_i, s_i], [a_i + 1, s_i], [a_i, s_i+1]]) - 0.5,
            # color input needs to be normalized
            color=cmap((result - VMIN) / (VMAX - VMIN))
        )
        ax.add_patch(triangle)

        plt.text(
            a_i-0.2, s_i -0.25, f"{result:.1f}",
            ha="center", va="center", color=get_color(result),
        )

# add "legend"
triangle = plt.Polygon(
    np.array([[6.75, -0.5], [7+1, -0.5], [6.75, 0.5]]),
    # color input needs to be normalized
    facecolor=cmap((5.4 - VMIN) / (VMAX - VMIN)),
    edgecolor="black",
    clip_on=False
)
ax.add_patch(triangle)
triangle = plt.Polygon(
    np.array([[7+1, 0.5], [7+1, -0.5], [6.75, 0.5]]),
    # color input needs to be normalized
    facecolor=cmap((5.8 - VMIN) / (VMAX - VMIN)),
    edgecolor="black",
    clip_on=False
)
ax.add_patch(triangle)
plt.text(
    7.2, -0.25, "Doc.",
    ha="center", va="center", color="black",
)
plt.text(
    7.55, 0.35, "Sent.",
    ha="center", va="center", color="black",
)

plt.imshow(img, cmap=cmap, vmin=VMIN, vmax=VMAX)
plt.colorbar(cmap=cmap, shrink=0.65, aspect=10, anchor=(0, 0.0))
plt.tight_layout(pad=0, rect=[0,0,1,1.1])
plt.savefig("figures/sent_doc_level.pdf")
plt.show()
