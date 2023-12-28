#!/usr/bin/env python3


from utils import load_json, save_json
data = load_json("data/parsed.json")

UID_TO_EXPERTISE = {
    "sahara": 1,
    "cardiff": 0,
    "hanoi": 0,
    "caracas": 2,
    "montevideo": 1,
    "washington": 0,
    "kampala": 1,
    "funafuti": 0,
    "ankara": 2,
    "tiraspol": 2,
    "lome": 2,
}
EXPERTISE_TO_NAME = {
    0: "layman",
    1: "student",
    2: "professional"
}


data_new = []

for doc in data:
    # shenanigans so that expertise is at the top
    uid = doc.pop("uid")
    data_new.append({
        "uid": uid,
        "expertise": EXPERTISE_TO_NAME[UID_TO_EXPERTISE[uid]],
        **doc
    })


save_json("data/for_lindat/annotations.json", data_new)