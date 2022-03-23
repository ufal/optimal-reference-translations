import csv
import pickle
import numpy as np

def load_data(filename="translations.csv"):
    with open(filename, "r") as f:
        data = list(csv.reader(f))[1:]
    # filter by second column
    data = [line[:6] for line in data if len(line[1]) != 0]
    return data


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