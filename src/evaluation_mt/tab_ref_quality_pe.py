import sys
sys.path.append("src")
import utils
import metrics_wrapper
import collections
import numpy as np
import argparse

args = argparse.ArgumentParser()
args.add_argument("--aggregate", default="random", choices={"random", "average"})
args.add_argument("--annotator", default=".*", choices={".*", "layman", "student", "professional"})
args = args.parse_args()


data_wmt = utils.load_wmt()

VAL_MIN=0.07
VAL_MAX=0.20
def format_corr_cell(value1, value2):
    if value2 > value1:
        return f"& \\plusA {value2-value1:.3f}".replace("%", "\\%")
    else:
        return f"& \\minusA {value1-value2:.3f}".replace("%", "\\%")

ref_avg = collections.defaultdict(list)

for metric in ["bleu", "chrf", "ter", "comet20", "comet22", "bleurt"]:
    print(f"{metrics_wrapper.METRIC_NAMES[metric]:<12}", end=" ")
    for pattern_ref in ["R1", "R2", "R3", "R4"]:
        metric_score = utils.load_metric_scores(
            f"computed/metric_scores_{metric}.json",
            pattern_ref=pattern_ref,
            aggregate=args.aggregate
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

        corr_orig, _ = utils.compute_segment_tau(data_wmt_local)

        metric_score = utils.load_metric_scores(
            f"computed/metric_scores_{metric}.json",
            pattern_ref=f"PE {args.annotator} {pattern_ref}",
            aggregate="average"
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
        corr_pe, _ = utils.compute_segment_tau(data_wmt_local)
        ref_avg[pattern_ref].append((corr_orig, corr_pe))


        print(format_corr_cell(corr_orig, corr_pe), end=" ")

    print("\\\\")
print(r"\bf Average", end=" ")
for pattern_ref in ["R1", "R2", "R3", "R4"]:
    print(format_corr_cell(
        np.average([x[0] for x in ref_avg[pattern_ref]]),
        np.average([x[1] for x in ref_avg[pattern_ref]]),
    ), end=" ")

print("\\\\")
