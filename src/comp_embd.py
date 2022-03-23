#!/usr/bin/env python3

from utils import load_data, save_pickle
from czert import Czert
from tqdm import tqdm

model = Czert()

data = load_data()
print(len(data))

data_embd = []
for line in tqdm(data):
    data_embd.append([model.embd(x) for x in line[1:5]])

save_pickle("computed/czert-b.embd", data_embd)