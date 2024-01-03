import sys
sys.path.append("src")
import utils
import metrics_wrapper
import collections
import argparse

args = argparse.ArgumentParser()
args.add_argument("-m1", "--metric1", default="bleu", help="Metrics to seek adversarials by")
args.add_argument("-m2", "--metric2", default="comet20", help="Secondary metric to show scores")
args = args.parse_args()

data_wmt = utils.load_wmt()


ref_avg = collections.defaultdict(list)

METRICS = [args.metric1, args.metric2]

metric_score = {
    metric: utils.load_metric_scores(
            f"computed/metric_scores_{metric}.json",
            pattern_ref=".*",
            aggregate=lambda x: x,
            ref_filter=lambda x: x,
        )
    for metric in METRICS
}

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
data_wmt_local = [x for x in data_wmt_local if len(x["src"].split()) < 10]

# sort from the beginning with the highest differences
data_wmt_local.sort(
    key=lambda x: max([x[3] for x in x["metric"][args.metric1]])-min([x[3] for x in x["metric"][args.metric1]]),
    reverse=True
)

for line in data_wmt_local[:10]:
    # skip nonpresentable examples
    if "suicide" in line["src"].lower():
        continue
    if "scottish" in line["src"].lower():
        continue

    print(line["src"])
    print(line["tgt"])
    line["metric"][args.metric1].sort(key=lambda x: x[3])

    metric2_map = {
        ref[2]: ref[3]
        for ref in line["metric"][args.metric2]
    }
    for ref in line["metric"][args.metric1]:
        print(
            f"{ref[3]:.0f}",
            f"{metric2_map[ref[2]]:.0f}",
            ref[2],
            sep=" & ",
            end=" \\\\\n"
        )
    print()
