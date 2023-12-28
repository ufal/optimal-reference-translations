#!/usr/bin/env python3

import sys
sys.path.append("src")
from utils import CATEGORIES, load_json
import numpy as np
import fig_utils
import matplotlib.pyplot as plt
import matplotlib as mpl
import sacrebleu
import evaluate
import tqdm

metric_bleu = sacrebleu.metrics.BLEU(effective_order=True)
metric_chrf = sacrebleu.metrics.CHRF()
metric_ter = sacrebleu.metrics.TER()
metric_meteor = evaluate.load("meteor")


def get_all_metrics(source, orig, done):
    return {
        "bleu": metric_bleu.sentence_score(orig, [done]).score / 100,
        "chrf": metric_chrf.sentence_score(orig, [done]).score / 100,
        "ter": metric_ter.sentence_score(orig, [done]).score / 100,
        "meteor": metric_meteor.compute(predictions=[orig], references=[done])["meteor"],
    }


def get_color(val):
    if val > 0.5:
        return "black"
    else:
        return "white"


data = load_json("data/parsed.json")
hits_inconsistency = 0
hits_total = 0
data_lines = []

for doc in tqdm.tqdm(data):
    for line in doc["lines"]:
        for system_name, translation in line["translations"].items():
            # TODO: hotfix unfinished data
            if any([x is None for x in translation["rating"].values()]):
                continue
            if translation["rating"]["overall"] == 6 and any([x < 6 for x in translation["rating"].values()]):
                hits_inconsistency += 1
            hits_total += 1

            translation["source"] = line["source"]
            data_lines.append(translation)

# TODO DEBUG remove
# data_lines = data_lines[:100]

print("Loading & computing COMET")
metric_comet = evaluate.load("comet", config_name="wmt21-cometinho-da")
comet_scores = metric_comet.compute(
    sources=[x["source"] for x in data_lines],
    predictions=[x["orig"] for x in data_lines],
    references=[x["done"] for x in data_lines],
    progress_bar=True,
)
del metric_comet

print("Loading & computing BLEURT")
metric_bleurt = evaluate.load("bleurt", module_type="metric")
bleurt_scores = metric_bleurt.compute(
    predictions=[x["orig"] for x in data_lines],
    references=[x["done"] for x in data_lines],
)
del metric_bleurt

for line, comet_score, bleurt_score in zip(tqdm.tqdm(data_lines), comet_scores["scores"], bleurt_scores["scores"]):
    line["metrics"] = get_all_metrics(
        line["source"], line["orig"], line["done"]
    )
    line["metrics"]["bleurt"] = bleurt_score
    line["metrics"]["comet"] = comet_score

print(" " * 11 + "".join([f"{category:>15}" for category in CATEGORIES]))

METRICS = list(data_lines[0]["metrics"].keys())

corrs = np.empty((len(METRICS), len(CATEGORIES)))
for metric_i, metric in enumerate(METRICS):
    data_1 = [x["metrics"][metric] for x in data_lines]
    print(f"{metric:>10}:", end="")
    for category_i, category in enumerate(CATEGORIES):
        data_2 = [x["rating"][category] for x in data_lines]
        corr = np.corrcoef(data_1, data_2)[0, 1]
        corrs[metric_i, category_i] = corr
        print(f"{corr:>15.2f}", end="")
    print()


VMIN = 0.2
VMAX = 0.7

# plotting
plt.figure(figsize=(5, 2.7))
ax = plt.gca()
cmap = mpl.cm.get_cmap("inferno").copy()
# show absolute values
plt.imshow(abs(corrs), cmap=cmap, vmin=VMIN, vmax=VMAX, aspect=0.7)

# add doc-level trinagles and texts
for s_i, s in enumerate(METRICS):
    for a_i, a in enumerate(CATEGORIES):
        result = corrs[s_i, a_i]
        plt.text(
            a_i + 0.0, s_i + 0.1, f"{result:.2f}".replace("0.", ".").replace("-", "- "),
            ha="center", va="center", color=get_color(abs(result)),
        )


plt.colorbar(
    cmap=cmap, shrink=0.9, aspect=10, anchor=(0, 0.0),
    ticks=np.round(np.linspace(VMIN, VMAX, num=5), 2),
)
plt.yticks(
    range(len(METRICS)),
    [fig_utils.METRIC_PRETTY_NAME[x] for x in METRICS]
)
plt.xticks(
    list(range(len(CATEGORIES))),
    [("\n" if x_i % 2 else "") + x.title()
     for x_i, x in enumerate(CATEGORIES)],
)

plt.tight_layout(pad=0, rect=[0.02, -0.01, 1, 1])
plt.savefig("figures/pe_score_correlation.pdf")
plt.show()
