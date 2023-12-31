import re
import sys
sys.path.append("src")
import utils
import metrics_wrapper
import collections
import numpy as np
import argparse

args = argparse.ArgumentParser()
args.add_argument("--aggregate", default="average", choices={"min", "max", "average"})
args.add_argument("--professionality", default="professional", choices={"professional", "student", "layman"})
args = args.parse_args()

data_wmt = utils.load_wmt()

VAL_MIN=0.07
VAL_MAX=0.21
def format_corr_cell(value):
    scaled_value = (value - VAL_MIN)/(VAL_MAX-VAL_MIN)
    return f"& {value:.3f}".replace("%", "\\%") + f" \\blackindicator{{{scaled_value:.2f}}}"

ref_avg = collections.defaultdict(list)
PATTERNS_REF = [f"R{i}" for i in [1,2,3,4]] + [f"PE {args.professionality} R{i}" for i in [1,2,3,4]]
HYPERPATTERNS_REF = [
    "PE R1",
    "PE R2",
    "PE R3",
    "PE R4",
    "PE R[1234]",
    "(PE |)R1",
    "(PE |)R2",
    "(PE |)R3",
    "(PE |)R4",
    "(PE |)R[1234]",
]
metric_scores = {
    metric:{
        pattern_ref.replace(args.professionality + " ", ""):utils.load_metric_scores(
            f"computed/metric_scores_{metric}.json",
            pattern_ref=pattern_ref,
            aggregate="average",
        )
        for pattern_ref in PATTERNS_REF
    }
    for metric in metrics_wrapper.METRICS.keys()
}

for metric in metrics_wrapper.METRICS.keys():
    print(f"& {metrics_wrapper.METRIC_NAMES[metric]:<12}", end=" ")
    for hyperpattern_ref in HYPERPATTERNS_REF:
        re_hyperpattern_ref = re.compile(hyperpattern_ref)

        # allow only patterns that pass hyperpatterns
        metric_scores_local = [
            metric_score
            for pattern_ref, metric_score in  metric_scores[metric].items()
            if re_hyperpattern_ref.match(pattern_ref)
        ]

        data_wmt_local = [
            {
                "src": x["src"],
                "tgt": x["tgt"],
                "system": x["system"],
                "human": x["score"],
                "metric": np.average([
                    metric_score[(x["src"], x["tgt"])]
                    for metric_score in metric_scores_local
                ]),
            }
            for x in data_wmt
        ]

        corr, _ = utils.compute_segment_tau(data_wmt_local)
        print(format_corr_cell(corr), end=" ")
        ref_avg[hyperpattern_ref].append(corr)

    print("\\\\")

print(r"\cmidrule{2-12}")
print(r"& \bf Average", end=" ")
for pattern_ref in HYPERPATTERNS_REF:
    print(format_corr_cell(np.average(ref_avg[pattern_ref])), end=" ")

print("\\\\")
