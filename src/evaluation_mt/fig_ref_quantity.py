import sys
sys.path.append("src")
import utils
import metrics_wrapper
import collections
import numpy as np
import random
import tqdm
import matplotlib.pyplot as plt
import scipy.stats as st 

random.seed(0)

data_wmt = utils.load_wmt()

plt.figure(figsize=(4, 1.5))
ax = plt.gca()
ax.spines[['right', 'top']].set_visible(False)

ref_avg = collections.defaultdict(list)
PATTERNS_REF = ["R3", "R[34]", r"R\d", r"PE .* R\d"]
X_TICKS = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21]

METRIC_COLORS = {
    "bleu": "#44a",
    "chrf": "#774",
    "comet20": "#a44",
    "bleurt": "#393",
}


METRIC_OFFSET = {
    "bleu": (-0, -0.012),
    "chrf": (-0, +0.009),
    "comet20": (+0.5, -0.012),
    "bleurt": (-0, +0.007),
}
for metric in ["bleu", "chrf", "comet20", "bleurt"]:
    scores = []
    metric_score = utils.load_metric_scores(
        f"computed/metric_scores_{metric}.json",
        pattern_ref=".*",
        aggregate=lambda x: x,
    )
    for ref_count in tqdm.tqdm(X_TICKS):
        aggregate = lambda x: np.average(random.sample(x, min(len(x), ref_count)))

        corrs = []

        for _ in range(10):
            data_wmt_local = [
                {
                    "src": x["src"],
                    "tgt": x["tgt"],
                    "system": x["system"],
                    "human": x["score"],
                    "metric": aggregate(metric_score[(x["src"], x["tgt"])]),
                }
                for x in data_wmt
            ]

            corr, _ = utils.compute_segment_tau(data_wmt_local)
            corrs.append(corr)

        scores.append(corrs)

    # plot confidence interval
    interval_min, interval_max = zip(*[
        st.norm.interval(
            confidence=0.999,
            loc=np.mean(corrs), 
            scale=st.sem(corrs)
        )
        for corrs in scores
    ])
    plt.fill_between(
        X_TICKS,
        interval_min,
        interval_max,
        color=METRIC_COLORS[metric],
        alpha=0.5,
        linewidth=0,
    )

    plt.plot(
        X_TICKS, [np.average(corrs) for corrs in scores],
        color=METRIC_COLORS[metric],
        linewidth=2,
    )
    plt.text(
        x=X_TICKS[-1]+METRIC_OFFSET[metric][0],
        y=np.average(scores[-1])+METRIC_OFFSET[metric][1],
        s=metrics_wrapper.METRIC_NAMES[metric],
        ha="right", va="center",
        color=METRIC_COLORS[metric],
    )

plt.xticks(
    [1, 3, 5, 7, 17, 19, 21],
)
plt.yticks(
    [0.09, 0.12, 0.15, 0.18, 0.21],
    ["0.09", ".12", ".15", "0.18", "0.21"],
)
plt.ylim(0.085)
plt.ylabel("Kendall's $\\tau$" + " " * 5, labelpad=-7, fontsize=10)
plt.xlabel(" "*7 + "References count", labelpad=-10)
plt.tight_layout(pad=0.05)
plt.savefig("computed/ref_quantity.pdf")
plt.show()