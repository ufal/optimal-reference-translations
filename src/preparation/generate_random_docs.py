#!/usr/bin/env python3

from utils import load_data, load_data_structure, save_json
from argparse import ArgumentParser
import random
from collections import defaultdict

args = ArgumentParser()
args.add_argument("-s", "--seed", type=int, default=0)
args = args.parse_args()

random.seed(args.seed)

data = [(k,v) for k,v in load_data_structure().items() if len(v) >= 10 and len(v) <= 15]
print(len(data), "available")

data = random.sample(data, k=22)

print(len(data), "selected")
print()

print("DOC_SPANS = {")
for k, v in data:
    start_i = random.randint(1, len(v)-8-1)
    if "en.ndtv.com.13152" in k:
        start_i = random.randint(3, len(v)-8)

    print(f"    '{k}': ({start_i}, {start_i+8-1}),")
print("}")