import csv
import pickle
import json


def load_data(filename="data/translations.csv"):
    with open(filename, "r") as f:
        data = list(csv.reader(f))[1:]
    # filter by second column
    data = [line[:6] for line in data if len(line[1]) != 0]
    return data


def load_data_structure(filename="data/translations.csv"):
    with open(filename, "r") as f:
        # strip header
        data = list(csv.reader(f))[1:]

    data_new = {}
    bucket = []
    cur_doc = None

    for line in data:
        if len(line[0]) != 0 and all([len(line[i]) == 0 for i in range(1, 3)]):
            # new document
            cur_doc = line[0]
        elif all([len(line[i]) == 0 for i in range(0, len(line))]) and len(bucket) != 0:
            if cur_doc is None:
                raise Exception()
            assert cur_doc not in data_new
            data_new[cur_doc] = bucket
            cur_doc = None
            bucket = []
        elif len(line[1]) != 0:
            # proper text
            bucket.append(line[:6])

    if cur_doc is not None:
        data_new[cur_doc] = bucket

    return data_new


def load_wmt(annotation_path="data/annotations.json", wmt_path="data/data_tmp/"):
    data = load_json(annotation_path)
    srcs = list({line["source"]
                for user_line in data for line in user_line["lines"]})

    data_new = []
    with open(wmt_path + "/text.tsv", "r") as f:
        data = list(f.readlines())
        for line_i, line in enumerate(data):
            sys, tgt, doc, src = line.removesuffix("\n").split("\t")
            # skip if not covered
            if src not in srcs:
                continue
            data_new.append({
                "system": sys,
                "tgt": tgt,
                "src": src,
                "i": line_i
            })

    with open(wmt_path + "/scores.tsv", "r") as f:
        i_to_score = {
            i: float(l.split("\t")[5]) if l.split("\t")[5] != "None" else 0
            for i, l in enumerate(f.readlines())
        }

    data_new = [
        {"score": i_to_score[line.pop("i")]} | line
        for line in data_new
    ]

    return data_new


def compute_segment_tau(data):
    from scipy.stats import kendalltau
    data_x = [x["human"] for x in data]
    data_y = [x["metric"] for x in data]
    return kendalltau(data_x, data_y)


def compute_system_acc(data):
    import collections
    import numpy as np
    import itertools

    system_to_human = collections.defaultdict(list)
    system_to_metric = collections.defaultdict(list)
    for line in data:
        system_to_human[line["system"]].append(line["human"])
        system_to_metric[line["system"]].append(line["metric"])

    # average
    system_to_human = {
        system: np.average(system_v)
        for system, system_v in system_to_human.items()
    }
    system_to_metric = {
        system: np.average(system_v)
        for system, system_v in system_to_metric.items()
    }

    acc = []
    for system_a, system_b in itertools.combinations(system_to_human.keys(), 2):
        # check if directions are the same
        acc.append(
            (system_to_human[system_a] < system_to_human[system_b]) ==
            (system_to_metric[system_a] < system_to_metric[system_b])
        )

    return np.average(acc)


def compute_system_spearman(data):
    import collections
    import numpy as np
    from scipy.stats import spearmanr

    system_to_human = collections.defaultdict(list)
    system_to_metric = collections.defaultdict(list)
    for line in data:
        system_to_human[line["system"]].append(line["human"])
        system_to_metric[line["system"]].append(line["metric"])

    # average
    system_to_human = {
        system: np.average(system_v)
        for system, system_v in system_to_human.items()
    }
    system_to_metric = {
        system: np.average(system_v)
        for system, system_v in system_to_metric.items()
    }
    systems = list(system_to_human.keys())

    return spearmanr(
        [system_to_human[system] for system in systems],
        [system_to_metric[system] for system in systems],
    )


def load_metric_scores(metric_path, pattern_ref, aggregate="average", ref_filter=lambda x: x[3], refids_path="computed/metric_scores_none.json"):
    """
    Returns metrics computed using a specific 
    """

    import re
    import collections
    import numpy as np
    import random

    if type(aggregate) is str:
        if aggregate == "average":
            aggregate = np.average
        elif aggregate == "random":
            aggregate = random.choice
        elif aggregate == "max":
            aggregate = max
        elif aggregate == "min":
            aggregate = min
        else:
            raise Exception("Unknown aggregator " + str(aggregate))

    pattern_ref = re.compile(pattern_ref)

    # checks if a particular (src, tgt, ref) is permissible
    refids_data = load_json(refids_path, cache=True)
    triplet_to_refids = collections.defaultdict(set)
    for line in refids_data:
        for ref in line["ref"]:
            triplet_to_refids[(line["src"], line["tgt"], ref[0])].add(ref[1])

    data_metric = load_json(metric_path, cache=True)

    tuple_to_metric_score = collections.defaultdict(list)
    for x in data_metric:
        refids = triplet_to_refids[(x[0], x[1], x[2])]

        # filter scores which don't satisfy the pattern match
        if not any(pattern_ref.match(refid) for refid in refids):
            continue

        tuple_to_metric_score[(x[0], x[1])].append(ref_filter(x))

    # average multiple scores
    tuple_to_metric_score = {
        # src, tgt -> score
        k: aggregate(v)
        for k, v in tuple_to_metric_score.items()
    }
    return tuple_to_metric_score


def get_device():
    import torch
    if torch.cuda.is_available():
        return torch.device("cuda:0")
    else:
        return torch.device("cpu")


def read_pickle(path):
    with open(path, "rb") as fread:
        reader = pickle.Unpickler(fread)
        return reader.load()


def save_pickle(path, data):
    with open(path, "wb") as fwrite:
        pickler = pickle.Pickler(fwrite)
        pickler.dump(data)


JSON_CACHE = {}


def load_json(path, cache=False):
    if cache:
        import copy
        if path in JSON_CACHE:
            return copy.deepcopy(JSON_CACHE[path])

    with open(path, "r") as fread:
        data = json.load(fread)

    if cache:
        JSON_CACHE[path] = copy.deepcopy(data)

    return data


def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
