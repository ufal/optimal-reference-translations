import sys
sys.path.append("src")
import utils
import metrics_wrapper
import collections
import numpy as np

data_wmt = utils.load_wmt()


ref_avg = collections.defaultdict(list)

METRICS = ["bleu", "chrf", "ter", "comet20", "comet22", "bleurt"]
METRICS = ["bleu", "comet20"]

metric_score = {
    metric: utils.load_metric_scores(
            f"computed/metric_scores_{metric}.json",
            pattern_ref=".*",
            aggregate=lambda x: x,
            ref_filter=lambda x: x,
        )
    for metric in METRICS
}

metric = "bleu"
print(metrics_wrapper.METRIC_NAMES[metric])

data_wmt_local = [
    {
        "src": x["src"],
        "tgt": x["tgt"],
        "system": x["system"],
        "human": x["score"],
        "metric": {
            metric:metric_score[metric][(x["src"], x["tgt"])]
            for metric in METRICS
        }
    }
    for x in data_wmt
]
data_wmt_local = [x for x in data_wmt_local if len(x["src"].split()) < 8]

# sort from the beginning with the highest differences
data_wmt_local.sort(
    key=lambda x: max([x[3] for x in x["metric"]["bleu"]])-min([x[3] for x in x["metric"]["bleu"]]),
    reverse=True
)

for line in data_wmt_local[:2]:
    print(line["src"])
    print(line["tgt"])
    line["metric"]["bleu"].sort(key=lambda x: x[3])

    comet20_map = {
        ref[2]: ref[3]
        for ref in line["metric"]["comet20"]
    }
    for ref in line["metric"]["bleu"]:
        print(
            f"{ref[3]:.0f}",
            f"{comet20_map[ref[2]]:.0f}",
            ref[2],
            sep=" & ",
            end=" \\\\\n"
        )
    print()
