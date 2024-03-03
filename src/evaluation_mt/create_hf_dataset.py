import sys
sys.path.append("src")
import json
import collections
import utils

REF_TYPE = ["R1", "R2", "R3", "R4"]

data_wmt = utils.load_wmt()
data_out = collections.defaultdict(lambda: {"src": None, "systems": {}})


data_human_raw = utils.load_json("data/ort_human.json")
data_human = collections.defaultdict(dict)
for doc in data_human_raw:
    for line in doc["lines"]:
        for ref_type, ref_type_val in line["translations"].items():
            ref_type = REF_TYPE[int(ref_type)-1]
            data_human[line["source"]][ref_type] = ref_type_val["orig"]
            data_human[line["source"]][
                ref_type + "_pe_" + doc["expertise"]+"_" + doc["uid"]
            ] = ref_type_val["done"]

for line in data_wmt:
    data_out[line["src"]]["src"] = line["src"]
    data_out[line["src"]]["systems"][line["system"]] = {
        "tgt": line["tgt"], "score": line["score"]
    }

data_out = list(data_out.values())

for line in data_out:
    line["ref"] = data_human[line["src"]]

with open("data/ort_wmt.json", "w") as f:
    json.dump(data_out, f, ensure_ascii=False, indent=2)
