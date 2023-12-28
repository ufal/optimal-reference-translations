import sys
sys.path.append("src")
from utils import load_json, save_json
from metrics_wrapper import METRICS
import argparse

args = argparse.ArgumentParser()
args.add_argument("--out", default="computed/metric_scores_{METRIC}.json")
args.add_argument("--metric", "-m", default="random")
args = args.parse_args()

data = load_json("computed/metric_scores_none.json")
prev_size = sum([len(line['ref']) for line in data])

data = {
    # ref[0] contains the text
    # ref[1] contains additional information which is not needed
    (line["src"], line["tgt"], ref[0])
    for line in data
    for ref in line["ref"]
}
# fix the set order (shouldn't matter for Python 3.8+)
data = list(data)

print(
    "Condensing from",
    f"{prev_size//1000}k",
    "to",
    f"{len(data)//1000}k",
    "lines"
)

metric = METRICS[args.metric]

data_scores = metric(data)
assert len(data) == len(data_scores)

data = [
    # JSON doesn't support tuple keys
    tuple([*x, score])
    for x, score in zip(data, data_scores)
]

save_json(args.out.replace("{METRIC}", args.metric), data)