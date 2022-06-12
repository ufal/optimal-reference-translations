#!/usr/bin/env python3

from utils import read_json
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

data = read_json("data/parsed.json")
xs = []
ys = []
# hack, assume that all ratings have the same order
features = None

for doc in data:
    for line in doc["lines"]:
        for system_name, translation in line["translations"].items():

            # TODO: hotfix unfinished data
            if translation["rating"]["overall"] is not None and translation["rating"]["pragmatics"] is not None:
                ys.append(translation["rating"]["overall"])
                xs.append(
                    [y for x, y in translation["rating"].items() if x != "overall"]
                )
                if features is None:
                    features = [x for x, y in translation["rating"].items() if x != "overall"]

xs_train, xs_test, ys_train, ys_test = train_test_split(
    xs, ys,
    test_size=0.1,
    random_state=0
)
print("All  ", len(xs), len(ys))
print("Train", len(xs_train), len(ys_train))
print("Test ", len(xs_test), len(ys_test))


model = LinearRegression()
model.fit(xs_train, ys_train)
print(
    f"{model.intercept_:.1f} +",
    " + ".join([f"{c:.1f}*{n}" for c, n in zip(model.coef_, features)]))
ys_pred = model.predict(xs_test)
hits_100 = [
    np.abs(y_pred- y) <= 1.0
    for y_pred, y
    in zip(ys_pred, ys_test)
]
hits_050 = [
    np.abs(y_pred- y) <= 0.5
    for y_pred, y
    in zip(ys_pred, ys_test)
]
hits_025 = [
    np.abs(y_pred- y) <= 0.25
    for y_pred, y
    in zip(ys_pred, ys_test)
]
print(f"Hits (1.0 tolerance):  {np.average(hits_100):.1%}")
print(f"Hits (0.5 tolerance):  {np.average(hits_050):.1%}")
print(f"Hits (0.25 tolerance): {np.average(hits_025):.1%}")