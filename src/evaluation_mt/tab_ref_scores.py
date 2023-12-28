import sys
sys.path.append("src")
import utils
import metrics_wrapper
import collections
import numpy as np
import argparse

data_wmt = utils.load_wmt()

def format_corr_cell(value):
    return f"& {value:.1f}".replace("-", r"\offsetminus")

ref_avg = collections.defaultdict(list)

for metric in ["bleu", "chrf", "ter", "comet20", "comet22", "bleurt"]:
    print(f"{metrics_wrapper.METRIC_NAMES[metric]:<12}", end=" ")
    for pattern_ref in ["R1", "R2", "R3", "R4", "PE professional R1", "PE professional R3"]:
        metric_score = utils.load_metric_scores(
            f"computed/metric_scores_{metric}.json",
            pattern_ref=pattern_ref,
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

        avg_score = np.average([x["metric"] for x in data_wmt_local])

        print(format_corr_cell(avg_score), end=" ")

    print("\\\\")