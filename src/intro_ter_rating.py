#!/usr/bin/env python3

from utils import save_json, read_json
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
from sacrebleu import sentence_ter, sentence_chrf
import fig_utils

data = read_json("data/parsed.json")
metric_scores = []
rating_scores = []
metric = sentence_ter

for doc in data:
    for line in doc["lines"]:
        for system_name, translation in line["translations"].items():
            # store sentence pairs
            if translation["orig"] is not None and translation["rating"]["overall"] is not None:
                metric_scores.append(
                    metric(translation["orig"], [translation["done"]]).score
                )
                rating_scores.append(translation["rating"]["overall"])


corr_coef = np.corrcoef(metric_scores, rating_scores)[1, 0]
plt.figure(figsize=(5, 3))

linear_model = np.polyfit(metric_scores, rating_scores, 1)
linear_model_fn = np.poly1d(linear_model)
x_s = np.arange(0, 125)
plt.plot(
    x_s, linear_model_fn(x_s),
    color=fig_utils.COLORS[1],
    label=f"Linear fit (pcorr={corr_coef:.1f})"
    )

plt.scatter(
    metric_scores,
    rating_scores,
    marker="o", s=10,
    alpha=0.7,
    color=fig_utils.COLORS[0]
)
plt.ylim(-0.5, 6.5)
plt.xlim(-5, 130)
plt.xlabel("TER")
plt.ylabel("Overall")
plt.legend()
plt.tight_layout()
plt.show()
