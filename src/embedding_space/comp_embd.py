#!/usr/bin/env python3

from utils import load_data, save_pickle
from embedding_space.lm_models import Czert, RobeCzech
from tqdm import tqdm
from argparse import ArgumentParser

args = ArgumentParser()
args.add_argument("--type-out", default="cls")
args.add_argument("--model", default="czert")
args = args.parse_args()

if args.model == "czertb":
    model = Czert()
elif args.model == "robeczech":
    model = RobeCzech()

data = load_data()
print(len(data), "lines")

data_embd = []
for line in tqdm(data):
    data_embd.append([model.embd(x, args.type_out) for x in line[1:5]])

save_pickle(f"computed/{args.model}-{args.type_out}.embd", data_embd)