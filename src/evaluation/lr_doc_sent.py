#!/usr/bin/env python3

import sys
sys.path.append("src")
from utils import read_json
import fig_utils
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

data = read_json("data/parsed.json")
xs_doc = []
ys_doc = []
xs_sent = []
ys_sent = []
features = [
    'spelling', 'terminology',
    'grammar', 'meaning', 'style', 'pragmatics'
]

for doc in data:
    for system_name, rating in doc["rating"].items():
        # TODO: hotfix unfinished data
        if any([v is None for v in rating.values()]):
            continue
        ys_doc.append(rating["overall"])
        xs_doc.append([rating[f] for f in features])

    for line in doc["lines"]:
        for system_name, translation in line["translations"].items():
            # TODO: hotfix unfinished data
            if any([v is None for v in translation["rating"].values()]):
                continue
            ys_sent.append(translation["rating"]["overall"])
            xs_sent.append([translation["rating"][f] for f in features])


xs_doc_train, xs_doc_test, ys_doc_train, ys_doc_test = train_test_split(
    xs_doc, ys_doc,
    test_size=100,
    random_state=0
)
xs_sent_train, xs_sent_test, ys_sent_train, ys_sent_test = train_test_split(
    xs_sent, ys_sent,
    test_size=100,
    random_state=0
)


def draw_scatter(ax, xs_train, ys_train, xs_test, ys_test, label):
    model = LinearRegression()
    model.fit(xs_train, ys_train)
    ys_pred = model.predict(xs_test)
    corrcoef = np.corrcoef((ys_pred, ys_test))[0, 1]
    lr_explanation = "$"
    lr_explanation += " + ".join([
        f"{c:.1f}\\cdot {n}"
        for c, n in zip(model.coef_, features[:3])
    ])
    lr_explanation += "$ \n $ + \,"
    lr_explanation += " + ".join([
        f"{c:.1f}\\cdot {n}"
        for c, n in zip(model.coef_, features[3:])
    ])
    if model.intercept_ >= 0:
        lr_explanation += " + "
    lr_explanation += f"{model.intercept_:.1f}$"
    
    ax.text(
        0.95, 0.55,
        "$\\rho_\mathregular{pred, true}^\mathregular{" + label + "} = " + f"{corrcoef:.2f}$",
        transform=ax.transAxes,
        ha="right"
    )
    ax.text(
        0.95, 0.25 if label == "segments" else 0.20,
        "$rating_{" + label + "} = $" + lr_explanation,
        transform=ax.transAxes,
        ha="right",
        fontsize=8.5,
    )

    ys = list(zip(ys_pred, ys_test))
    ys.sort(key=lambda x: x[1])
    ax.scatter(
        list(range(len(ys))),
        [y[0] for y in ys],
        label="Predicted",
        alpha=0.5,
    )
    ax.scatter(
        list(range(len(ys))),
        [y[1] for y in ys],
        label="True",
        alpha=0.25,
    )
    ax.set_xticks([], [])
    ax.set_ylabel("Rating " + r"$\bf{" + label + "}$")
    if label == "segments":
        ax.set_yticks(
            [-1, 0, 1, 2, 3, 4, 5, 6],
            ["", 0, 1, 2, 3, 4, 5, 6],
        )

plt.figure(figsize=(5,4))
draw_scatter(
    plt.subplot(2, 1, 1),
    xs_doc_train, ys_doc_train,
    xs_doc_test, ys_doc_test,
    "docs",
)
draw_scatter(
    plt.subplot(2, 1, 2),
    xs_sent_train, ys_sent_train,
    xs_sent_test, ys_sent_test,
    "segments"
)

# address the last one
plt.xlabel("Test items (docs or segments)")
plt.legend(ncol=2)
plt.tight_layout(pad=0)
plt.savefig("figures/lr_doc_sent.pdf")
plt.show()
