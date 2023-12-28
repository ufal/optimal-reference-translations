#!/usr/bin/env python3

import collections
import sys
sys.path.append("src")
from utils import load_json
import numpy as np
import matplotlib.pyplot as plt
from sacrebleu import sentence_ter, sentence_chrf
import tqdm
import fig_utils

data = load_json("data/parsed.json")
metric_scores = []
rating_scores = []
post_edited = []
orig_word_counts = []
metric = sentence_chrf
rating_scores_all = collections.defaultdict(list)

for doc in tqdm.tqdm(data):
    for line in doc["lines"]:
        for system_name, translation in line["translations"].items():
            # store sentence pairs
            if translation["orig"] is not None and translation["rating"]["overall"] is not None:
                is_edited = translation["orig"].strip(
                ) != translation["done"].strip()
                post_edited.append(is_edited)
                metric_scores.append(
                    metric(translation["orig"], [translation["done"]]).score
                )
                rating_scores.append(translation["rating"]["overall"])
                for category, value in translation["rating"].items():
                    rating_scores_all[category].append(value)
                orig_word_counts.append(len(translation["orig"].split()))

corr_coef = np.corrcoef(metric_scores, rating_scores)[1, 0]
plt.figure(figsize=(5, 3))

print(
    sum(post_edited),
    f"post-edited in total ({np.average(post_edited):.2%})"
)
print(
    f"On average {np.average(orig_word_counts):.1f}",
    "source tokens per sentence"
)

for category, category_rating in rating_scores_all.items():
    assert len(category_rating) == len(post_edited)
    less_but_not_edited = np.average([
        (r is not None and r < 6) and not is_edited
        for r, is_edited in zip(category_rating, post_edited)
    ])
    print(f"{category}: {np.average(less_but_not_edited):.2%}")

less_but_not_edited = np.average([
    any((rating_scores_all[category][i] is not None and rating_scores_all[category][i] < 6) for category in rating_scores_all.keys()) 
    and not is_edited
    for i, is_edited in enumerate(post_edited)
])
print(f"any category: {np.average(less_but_not_edited):.2%}")

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
