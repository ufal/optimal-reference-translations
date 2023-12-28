import sys
sys.path.append("src")
import utils
import metrics_wrapper
import collections
import numpy as np
import argparse

args = argparse.ArgumentParser()
args.add_argument("--aggregate", default="average", choices={"min", "max", "average"})
args.add_argument("--mode", default="seg", choices={"seg", "sys"})
args = args.parse_args()

data_wmt = utils.load_wmt()

VAL_MIN=0.07
VAL_MAX=0.21
def format_corr_cell(value):
    scaled_value = (value - VAL_MIN)/(VAL_MAX-VAL_MIN)
    return f"& {value:.3f}".replace("%", "\\%") + f" \\blackindicator{{{scaled_value:.2f}}}"

ref_avg = collections.defaultdict(list)
PATTERNS_REF = ["R3", "R[34]", r"R\d", r"PE .* R\d"]

for metric in ["bleu", "chrf", "ter", "comet20", "comet22", "bleurt"]:
    print(f"{metrics_wrapper.METRIC_NAMES[metric]:<12}", end=" ")
    for pattern_ref in PATTERNS_REF:
        metric_score = utils.load_metric_scores(
            f"computed/metric_scores_{metric}.json",
            pattern_ref=pattern_ref,
            aggregate=args.aggregate,
        )

        data_wmt_local = [
            {
                "src": x["src"],
                "tgt": x["tgt"],
                "system": x["system"],
                "human": x["score"],
                "metric": metric_score[(x["src"], x["tgt"])],
            }
            for x in data_wmt
        ]

        if args.mode == "seg":
            corr, _ = utils.compute_segment_tau(data_wmt_local)
            print(format_corr_cell(corr), end=" ")
            ref_avg[pattern_ref].append(corr)
        elif args.mode == "sys":
            acc = utils.compute_system_acc(data_wmt_local)
            print(f"& {acc:.3f}", end=" ")

            corr, _ = utils.compute_system_spearman(data_wmt_local)
            print(f"& {corr:.1%}", end=" ")

    print("\\\\")

print(r"\bf Average", end=" ")
for pattern_ref in PATTERNS_REF:
    print(format_corr_cell(np.average(ref_avg[pattern_ref])), end=" ")

print("\\\\")
