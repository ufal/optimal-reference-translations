#!/usr/bin/env python3

from utils import load_json
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append("src")
import fig_utils
from consts import *

data = load_json("data/parsed.json")
rating_scores = []

data_time = defaultdict(lambda: list())
data_time_avg = defaultdict(lambda: list())
data_time_class = defaultdict(lambda: list())
data_time_all = []
count_class = {0: 4, 1: 4, 2: 4}

for doc in data:
    data_time[doc["uid"]].append(doc["time"])
    data_time_all.append(doc["time"])
    data_time_class[UID_CLASS[doc["uid"]]].append(doc["time"])

cost_done = 0
docs_done = 0
cost_todo = 0
docs_todo = 0

for uid, times in data_time.items():
    price_per_hour = COST[UID_CLASS[uid]]
    count_class[UID_CLASS[uid]] -= 1
    cost_done += sum([price_per_hour/60 * t for t in times])
    docs_done += len(times)
    avg_time_est = np.average(times[1:])
    cost_todo += price_per_hour/60*avg_time_est * (20-len(times))
    docs_todo += 20-len(times)
    print(f"{uid:<10} | {len(times):<3} | {np.average(times):>3.0f}min | {np.average([price_per_hour/60 * t for t in times]):<3.0f} | {CLASS_NAME[UID_CLASS[uid]]}")

print(f"Currently paid {cost_done:.0f} CZK for {docs_done} docs")
print(f"Estimate {cost_todo:.0f} CZK for {docs_todo} docs (individual estimate)")
docs_generic = 0
cost_generic = 0
for class_k, count in count_class.items():
    docs_generic += count * 20
    cost_generic += count * 20 * COST[class_k] / 60 * np.average(data_time_class[class_k])
print(f"Estimate {cost_generic:.0f} CZK for {docs_generic} unassigned docs")
print(f"Estimate {cost_done + cost_todo + cost_generic:.0f} CZK in total")

plt.figure(figsize=(6, 4))
for uid_i, (uid, times) in enumerate(data_time.items()):
    plt.plot(
        list(range(1, len(times) + 1)),
        times,
        alpha=0.6,
        label=uid,
        color=fig_utils.COLORS[uid_i // 2],
        linestyle=":" if uid_i % 2 == 0 else "-",
    )
    for doc_i, time_v in enumerate(times):
        data_time_avg[doc_i].append(time_v)

XTICKS = list(range(1, len(data_time_avg.values()) + 1))
plt.plot(
    XTICKS,
    [np.average(data_time_avg[x - 1]) for x in XTICKS],
    color="black",
    label="Average*",
)
plt.xticks(XTICKS, XTICKS)

# add average labels
for x in XTICKS:
    plt.text(
        x,
        np.average(data_time_avg[x - 1])+5,
        f"{np.average(data_time_avg[x-1]):.0f}"
    )
plt.hlines(
    np.average(data_time_all),
    XTICKS[0], XTICKS[-1],
    colors="black",
    label="Average",
    alpha=0.5,
)
plt.text(
    XTICKS[-1],
    np.average(data_time_all)+5,
    f"{np.average(data_time_all):.0f}",
    color="gray",
)

plt.legend(ncol=2)
plt.tight_layout()
plt.show()
