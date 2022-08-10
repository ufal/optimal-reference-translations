#!/usr/bin/env python3

import sys
sys.path.append("src")
from utils import save_json, read_json
from openpyxl import load_workbook
import json
from pathlib import Path
import numpy as np

# override
UIDs = [
    "sahara", "cardiff", "hanoi",
    "caracas", "montevideo", "washington", "kampala", "funafuti",
    "ashgabat", "ankara", "tiraspol", "lome", "bangkok",
    "dodoma", "dushanbe", "damascus", "bern", "stockholm",
]
DATA = []

COL_ORIG = ["B", "C", "D", "E"]
COL_DONE = ["B", "J", "R", "Z"]
COL_DONE_RATING = [
    ["C", "D", "E", "F", "G", "H", "I"],
    ["K", "L", "M", "N", "O", "P", "Q"],
    ["S", "T", "U", "V", "W", "X", "Y"],
    ["AA", "AB", "AC", "AD", "AE", "AF", "AG"],
]
ATTRIBUTES = [
    "spelling", "terminology", "grammar",
    "meaning", "style", "pragmatics", "overall"
]

def parse_time(val):
    # we need this function because some people wrote also some text into the 
    # time field
    if val is None:
        return None
    elif type(val) == float:
        return val
    elif type(val) == str:
        return float("".join([x for x in val if x.isdigit()]))
    else:
        raise Exception("Unable to parse", val, "as time")

print(f"{'UID':<13} | {'docs':>4} | {'avg. time':>10} | {'sum time':>10} |")
docs_time_avgs = []
for uid in UIDs:
    if not Path(f"data/done/translations_{uid}.xlsx").is_file():
        continue
    mapping = read_json(f"data/mapping/mapping_{uid}.json")
    wb = load_workbook(f"data/done/translations_{uid}.xlsx")
    docs_skipped = []
    docs_time = []

    for i in range(20):
        doc = mapping["docs"][i]
        systems = mapping["systems"][doc]
        sheet_done = wb[f"Edit{i+1}"]
        sheet_orig = wb[f"Orig{i+1}"]
        row_start = None
        row_end = None
        for row in range(2, 50):
            is_empty = sheet_orig[f"B{row}"].value is None
            if is_empty and row_start is not None:
                row_end = row
                break
            if not is_empty and row_start is None:
                row_start = row

        row_rating = None
        for row in range(row_end, 50):
            is_empty = sheet_done[f"A{row}"].value is None
            if is_empty:
                row_rating = row+1
                break

        line_doc = {
            "uid": uid,
            "doc": doc,
            "overall": {},
            "time": parse_time(sheet_done[f"B{row_rating+1}"].value),
            "rating": {},
            "lines": []
        }
        if line_doc["time"] is None:
            docs_skipped.append(doc)
            # skip this doc
            continue

        docs_time.append(line_doc["time"])

        for system_permd in range(4):
            rating = {}
            for rating_i, rating_col in enumerate(COL_DONE_RATING[system_permd]):
                attribute_name = ATTRIBUTES[rating_i]
                rating[attribute_name] = sheet_done[f"{rating_col}{row_rating}"].value

            # TODO: check that the permutation is correct and that we don't need the inverse
            system_i = systems[system_permd]
            line_doc["rating"][system_i] = rating
                
        # row end points to the first empty after segment
        for row in range(row_start, row_end):
            line_transl = {
                "source": sheet_orig[f"A{row}"].value,
                "comment": sheet_done[f"AH{row}"].value,
                "translations": {},
            }
            for system_permd in range(4):
                line_system = {
                    "orig": str(sheet_orig[f"{COL_ORIG[system_permd]}{row}"].value),
                    "done": str(sheet_done[f"{COL_DONE[system_permd]}{row}"].value),
                }
                rating = {}
                for rating_i, rating_col in enumerate(COL_DONE_RATING[system_permd]):
                    attribute_name = ATTRIBUTES[rating_i]
                    rating[attribute_name] = sheet_done[f"{rating_col}{row}"].value
                line_system["rating"] = rating

                # TODO: check that the permutation is correct and that we don't need the inverse
                system_i = systems[system_permd]
                line_transl["translations"][system_i] = line_system

            line_doc["lines"].append(line_transl)
        DATA.append(line_doc)
    
    print(f"{uid:<13} | {20-len(docs_skipped):>4} | ", f"{np.average(docs_time):>6.0f}min | " if docs_time else f"{'':>9} | ", f"{sum(docs_time)/60:>8.1f}h |")
    if docs_time:
        docs_time_avgs.append(np.average(docs_time))
print(f"Average time per document: {np.average(docs_time_avgs):.0f}min")

# not using save_json because of cache/encoding issue?
with open("data/parsed.json", "w") as f:
    json.dump(DATA, f, indent=4, ensure_ascii=False)
