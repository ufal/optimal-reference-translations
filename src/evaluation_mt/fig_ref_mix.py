import sys
sys.path.append("src")
import metrics_wrapper
import utils
import numpy as np
import random
import matplotlib.pyplot as plt

random.seed(0)

data_wmt = utils.load_wmt()

PATTERNS_REF = ["R1", "R2", "R4", "R3"]
PROP_COUNT = 10
METRIC_COLORS = {
    "bleu": "#44a",
    "chrf": "#774",
    "comet20": "#a44",
    "bleurt": "#393",
}
METRIC_OFFSET = {
    "bleu": (-0.0, -0.011),
    "chrf": (-0.0, +0.006),
    "comet20": (+0.5, -0.010),
    "bleurt": (-0.0, +0.0055),
}

fig, (ax1, ax2) = plt.subplots(
    2, 1,
    height_ratios=(7, 1),
    figsize=(4, 1.7),
    sharex=True
)
ax1.spines[['right', 'top', 'bottom']].set_visible(False)
ax2.spines[['left', 'right', 'top', 'bottom']].set_visible(False)

for metric in ["comet20", "bleurt", "chrf", "bleu"]:
    metric_score = {
        pattern_ref: utils.load_metric_scores(
            f"computed/metric_scores_{metric}.json",
            pattern_ref=pattern_ref,
            aggregate="average",
        )
        for pattern_ref in PATTERNS_REF
    }

    scores = []
    for RA, RB in zip(PATTERNS_REF, PATTERNS_REF[1:]):
        for proportion in np.linspace(1, 0, PROP_COUNT):
            indices = list(range(len(data_wmt)))

            corrs = []
            for _ in range(50):
                indices_a = set(random.sample(
                    indices, k=int(proportion * len(data_wmt))
                ))
                indices_b = {i for i in indices if i not in indices_a}
                data_wmt_local = [
                    {
                        "src": x["src"],
                        "tgt": x["tgt"],
                        "system": x["system"],
                        "human": x["score"],
                        "metric": (
                            metric_score[RA][(x["src"], x["tgt"])]
                            if i in indices_a else
                            metric_score[RB][(x["src"], x["tgt"])]
                        ),
                    }
                    for i, x in enumerate(data_wmt)
                ]

                corr, _ = utils.compute_segment_tau(data_wmt_local)
                corrs.append(corr)

            scores.append(np.average(corrs))

        if RB != PATTERNS_REF[-1]:
            ax1.vlines(
                x=len(scores),
                ymin=0.08, ymax=0.20,
                color="black", alpha=0.3,
            )

    ax1.plot(
        scores,
        color=METRIC_COLORS[metric],
        linewidth=2,
    )
    ax1.text(
        x=len(scores) + METRIC_OFFSET[metric][0],
        y=scores[-1] + METRIC_OFFSET[metric][1],
        s=metrics_wrapper.METRIC_NAMES[metric],
        ha="right", va="center",
        color=METRIC_COLORS[metric],
    )


PATTERNS_REF_COLORS = {
    "R1": "#555",
    "R2": "#888",
    "R3": "#ccc",
    "R4": "#aaa",
}

for r_i, r_v in enumerate(PATTERNS_REF):
    if r_i != len(PATTERNS_REF) - 1:
        ax2.fill_between(
            x=[r_i * PROP_COUNT, r_i * PROP_COUNT + PROP_COUNT],
            y1=[0, 0],
            y2=[1, 0],
            color=PATTERNS_REF_COLORS[r_v],
        )
    if r_i != 0:
        ax2.fill_between(
            x=[(r_i - 1) * PROP_COUNT, (r_i - 1) * PROP_COUNT + PROP_COUNT],
            y1=[1, 0],
            y2=[1, 1],
            color=PATTERNS_REF_COLORS[r_v],
        )
    ax2.text(
        x=(
            r_i * PROP_COUNT + 1.25
            if r_i == 0 else
            r_i * PROP_COUNT - 1
        ),
        y=0.3 if r_i == 0 else 0.5,
        s=r_v,
        ha="center", va="center",
    )

ax1.set_ylabel(" " * 5 + r"Kendall's $\tau$", labelpad=-7)
ax1.set_xticks([])
ax1.set_yticks(
    [0.10, 0.15, 0.20],
    ["0.10", ".15", "0.20"],
)
ax2.set_xticks([])
ax2.set_yticks([])
ax2.set_ylim(0, 1)
ax2.set_ylabel("Proportion", rotation=0, fontsize=8.5)
ax2.yaxis.set_label_coords(-0.045, 0.1)

plt.tight_layout(pad=0.05)
plt.subplots_adjust(hspace=-0.06)
plt.savefig("computed/ref_mix.pdf")
plt.show()
