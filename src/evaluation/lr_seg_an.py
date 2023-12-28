#!/usr/bin/env python3

import sys
sys.path.append("src")
from utils import load_json, UID_MAP
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import collections
import sacrebleu

metric_bleu = sacrebleu.metrics.BLEU(effective_order=True)

data = load_json("data/parsed.json")
xs_uid = collections.defaultdict(list)
bleus_uid = collections.defaultdict(list)
ys_uid = collections.defaultdict(list)
features = [
    'spelling', 'terminology',
    'grammar', 'meaning', 'style', 'pragmatics'
]

SYSTEMS = ["1", "2", "3", "4"]

for doc in data:
    data_local = []
    for system_name in SYSTEMS:
        for line in doc["lines"]:
            translation = line["translations"][system_name]
            # TODO: hotfix unfinished data
            if any([x is None for x in translation["rating"].values()]):
                continue
            ys_uid[doc["uid"]].append(translation["rating"]["overall"])
            xs_uid[doc["uid"]].append(
                [translation["rating"][f] for f in features]
            )
            score_bleu = metric_bleu.sentence_score(
                translation["orig"], [translation["done"]]
            ).score / 100
            bleus_uid[doc["uid"]].append(score_bleu)

# BLEU + UID should work

print("Individual LR corr")
for uid in UID_MAP.keys():
    xs_train, xs_test, ys_train, ys_test = train_test_split(
        xs_uid[uid], ys_uid[uid],
        test_size=100,
        random_state=0
    )
    model = LinearRegression()
    model.fit(xs_train, ys_train)
    ys_pred = model.predict(xs_test)
    corrcoef = np.corrcoef((ys_pred, ys_test))[0, 1]
    print(f"{uid + ' (' + UID_MAP[uid] + ')':>30}: {corrcoef:.2f}")
print()


def encode_expertise(uid):
    expertise = UID_MAP[uid]
    if expertise == "translator":
        return [1, 0, 0]
    elif expertise == "student":
        return [0, 1, 0]
    elif expertise == "nontranslator":
        return [0, 0, 1]

UID_KEYS = list(UID_MAP.keys())
def encode_uid(uid):
    out = [0] * len(UID_MAP)
    i = UID_KEYS.index(uid)
    out[i] = 1
    return out


# merge all together
xs_all = [
    x + encode_uid(uid)
    for uid in UID_MAP.keys() for x in xs_uid[uid]
]
ys_all = [y for uid in UID_MAP.keys() for y in ys_uid[uid]]


xs_train, xs_test, ys_train, ys_test = train_test_split(
    xs_all, ys_all,
    test_size=100,
    random_state=0
)
model = LinearRegression()
model.fit(xs_train, ys_train)
ys_pred = model.predict(xs_test)
corrcoef = np.corrcoef((ys_pred, ys_test))[0, 1]
print(f"categories + expertise: {corrcoef:.2f}")


# merge all together
xs_all = [
    [x] + encode_expertise(uid)
    for uid in UID_MAP.keys() for x in bleus_uid[uid]
]
ys_all = [y for uid in UID_MAP.keys() for y in ys_uid[uid]]

xs_train, xs_test, ys_train, ys_test = train_test_split(
    xs_all, ys_all,
    test_size=100,
    random_state=0
)
model = LinearRegression()
model.fit(xs_train, ys_train)
ys_pred = model.predict(xs_test)
corrcoef = np.corrcoef((ys_pred, ys_test))[0, 1]
print(f"bleu + expertise: {corrcoef:.2f}")

# merge all together
xs_all = [
    [x] + encode_uid(uid)
    for uid in UID_MAP.keys() for x in bleus_uid[uid]
]
ys_all = [y for uid in UID_MAP.keys() for y in ys_uid[uid]]

xs_train, xs_test, ys_train, ys_test = train_test_split(
    xs_all, ys_all,
    test_size=100,
    random_state=0
)
model = LinearRegression()
model.fit(xs_train, ys_train)
ys_pred = model.predict(xs_test)
corrcoef = np.corrcoef((ys_pred, ys_test))[0, 1]
print(f"bleu + uid: {corrcoef:.2f}")

# merge all together
xs_all = [
    encode_expertise(uid)
    for uid in UID_MAP.keys() for x in bleus_uid[uid]
]
ys_all = [y for uid in UID_MAP.keys() for y in ys_uid[uid]]

xs_train, xs_test, ys_train, ys_test = train_test_split(
    xs_all, ys_all,
    test_size=100,
    random_state=0
)
model = LinearRegression()
model.fit(xs_train, ys_train)
ys_pred = model.predict(xs_test)
corrcoef = np.corrcoef((ys_pred, ys_test))[0, 1]
print(f"expertise: {corrcoef:.2f}")


# merge all together
xs_all = [
    encode_uid(uid)
    for uid in UID_MAP.keys() for x in bleus_uid[uid]
]
ys_all = [y for uid in UID_MAP.keys() for y in ys_uid[uid]]

xs_train, xs_test, ys_train, ys_test = train_test_split(
    xs_all, ys_all,
    test_size=100,
    random_state=0
)
model = LinearRegression()
model.fit(xs_train, ys_train)
ys_pred = model.predict(xs_test)
corrcoef = np.corrcoef((ys_pred, ys_test))[0, 1]
print(f"uid: {corrcoef:.2f}")