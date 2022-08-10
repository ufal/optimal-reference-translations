#!/usr/bin/env python3

from utils import load_data, read_pickle
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.dummy import DummyClassifier
from sklearn.model_selection import train_test_split

data = read_pickle("computed/czertb-tokens.embd")

data_x = []
data_y = []

for line in data:
    data_x.append(line[0])
    data_y.append(0)
    
    data_x.append(line[1])
    data_y.append(0)
    
    data_x.append(line[2])
    data_y.append(0)
    
    data_x.append(line[3])
    data_y.append(1)

print(len([x for x in data_y if x == 0]), "nonexpert")
print(len([x for x in data_y if x == 1]), "superhuman")

data_x = StandardScaler().fit_transform(data_x)

data_train, data_dev = train_test_split(
    list(zip(data_x, data_y)), test_size=100, random_state=0
)

data_train_x, data_train_y = zip(*data_train)
data_dev_x, data_dev_y = zip(*data_dev)

model = LogisticRegression(max_iter=500)
model.fit(data_train_x, data_train_y)
train_acc = model.score(data_train_x, data_train_y)
dev_acc = model.score(data_dev_x, data_dev_y)

print(f"[lr] Train acc: {train_acc:.2%}%")
print(f"[lr] Dev acc: {dev_acc:.2%}%")

model = DummyClassifier(strategy="most_frequent")
model.fit(data_train_x, data_train_y)
train_acc = model.score(data_train_x, data_train_y)
dev_acc = model.score(data_dev_x, data_dev_y)

print(f"[dummy] Train acc: {train_acc:.2%}%")
print(f"[dummy] Dev acc: {dev_acc:.2%}%")
