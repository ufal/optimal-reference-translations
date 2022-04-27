import csv
import pickle
import json
import numpy as np

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
        elif all([len(line[i]) == 0 for i in range(0,len(line))]) and len(bucket) != 0:
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


def read_json(path):
    with open(path, "r") as fread:
        return json.load(fread)

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)