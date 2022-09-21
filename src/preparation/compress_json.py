#!/usr/bin/env python3

"""
Creates minified versions of the parsed.json file which is otherwise "human readable"
"""

import json
import gzip


with open("data/parsed.json", "r") as f:
    data = json.load(f)

with open("data/parsed_minified.json", "w") as f:
    json.dump(data, f, ensure_ascii=False)

with open("data/parsed_minified.json", "r") as f:
    data_s = f.read()

with gzip.open('data/parsed_minified.json.gz', 'wb') as f:
    f.write(data_s.encode("utf-8")) 