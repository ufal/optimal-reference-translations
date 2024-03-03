import sys
sys.path.append("src")
import utils
import collections
import json

data_wmt = utils.load_wmt()
data_out = collections.defaultdict(lambda: {"src": None, "systems": {}})

for line in data_wmt:
    data_out[line["src"]]["src"] = line["src"]
    data_out[line["src"]]["systems"][line["system"]] = { "tgt": line["tgt"], "score": line["score"] }

data_out = list(data_out.values())

with open("data/ort_wmt.json", "w") as f:
    json.dump(data_out, f, ensure_ascii=False, indent=2)