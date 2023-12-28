#!/usr/bin/env python3

import sys
sys.path.append("src")
from utils import load_json
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import sacrebleu

metric_bleu = sacrebleu.metrics.BLEU(effective_order=True)

data = load_json("data/parsed.json")
xs_seg = []
ys_seg = []
features = [
    'spelling', 'terminology',
    'grammar', 'meaning', 'style', 'pragmatics'
]

for doc in data:
    for line in doc["lines"]:
        for system_name, translation in line["translations"].items():
            # TODO: hotfix unfinished data
            if any([v is None for v in translation["rating"].values()]):
                continue
            ys_seg.append(translation["rating"]["overall"])
            score_bleu = metric_bleu.sentence_score(
                translation["orig"], [translation["done"]]
            ).score / 100
            xs_seg.append(
                [translation["rating"][f] for f in features] + [score_bleu]
            )

xs_seg = np.array(xs_seg)
xs_seg = xs_seg - np.mean(xs_seg, axis=0)
xs_seg_train, xs_seg_test, ys_seg_train, ys_seg_test = train_test_split(
    xs_seg, ys_seg,
    test_size=100,
    random_state=0
)

def draw_scatter(xs_train, ys_train, xs_test, ys_test, label):
    print(f"{label} train/test {len(xs_train)}/{len(xs_test)}")

    model = LinearRegression()
    model.fit(xs_train, ys_train)
    ys_pred = model.predict(xs_test)
    corrcoef = np.corrcoef((ys_pred, ys_test))[0, 1]

    lr_explanation = ""
    lr_explanation += " + ".join([
        f"{c:.1f} * {n}"
        for c, n in zip(model.coef_, features + ["bleu"])
    ])
    if model.intercept_ >= 0:
        lr_explanation += " + "
    lr_explanation += f"{model.intercept_:.1f}"
    print(lr_explanation)
    print(f"Corr: {corrcoef:.2f}")


draw_scatter(
    xs_seg_train, ys_seg_train,
    xs_seg_test, ys_seg_test,
    "segments"
)
