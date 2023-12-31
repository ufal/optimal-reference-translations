import re
import sys
sys.path.append("src")
import utils
import metrics_wrapper
import collections
import numpy as np
import argparse
import itertools

args = argparse.ArgumentParser()
args.add_argument("--aggregate", default="average", choices={"min", "max", "average"})
args = args.parse_args()

data_wmt = utils.load_wmt()

VAL_MIN=0.07
VAL_MAX=0.21
def format_corr_cell(value):
    scaled_value = (value - VAL_MIN)/(VAL_MAX-VAL_MIN)
    return f"& {value:.3f}".replace("%", "\\%") + f" \\blackindicator{{{scaled_value:.2f}}}"

ref_avg = collections.defaultdict(list)
PATTERNS_REF = [f"R{i}" for i in [1,2,3,4]]
PATTERNS_REF = [
    "R[" + "".join([x.removeprefix("R") for x in subset]) + "]"
    for n in [1, 2, 3, 4]
    for subset in itertools.combinations(PATTERNS_REF, n)
]
print(PATTERNS_REF, len(PATTERNS_REF))

metric_scores = {
    metric:{
        pattern_ref:utils.load_metric_scores(
            f"computed/metric_scores_{metric}.json",
            pattern_ref=pattern_ref,
            aggregate=args.aggregate,
        )
        for pattern_ref in PATTERNS_REF
    }
    for metric in metrics_wrapper.METRICS.keys()
}

for metric in metrics_wrapper.METRICS.keys():
    print(f"& {metrics_wrapper.METRIC_NAMES[metric]:<12}", end=" ")
    for pattern_ref in PATTERNS_REF:
        data_wmt_local = [
            {
                "src": x["src"],
                "tgt": x["tgt"],
                "system": x["system"],
                "human": x["score"],
                "metric": metric_scores[metric][pattern_ref][(x["src"], x["tgt"])],
            }
            for x in data_wmt
        ]

        corr, _ = utils.compute_segment_tau(data_wmt_local)
        print(format_corr_cell(corr), end=" ")
        ref_avg[pattern_ref].append(corr)

    print("\\\\")

print(r"\cmidrule{2-17}")
print(r"& \bf Average", end=" ")
for pattern_ref in PATTERNS_REF:
    print(format_corr_cell(np.average(ref_avg[pattern_ref])), end=" ")

print("\\\\")
