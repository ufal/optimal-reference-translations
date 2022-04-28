#!/usr/bin/env python3

from utils import load_data, load_data_structure, save_json
import csv
from argparse import ArgumentParser
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Alignment, Color, PatternFill, Font
import random
from collections import defaultdict
from xlsx_consts import *

args = ArgumentParser()
args = args.parse_args()

data = load_data_structure()


def add_edit_sheet(workbook, doc_i, doc_k, doc_v):
    sheet = workbook.create_sheet("D" + str(doc_i))
    sheet.add_data_validation(NUM_VALIDATION)

    for col in "ABCDEFGHIJKLMNOPQR":
        sheet[col + "1"].font = Font(bold=True, name="Calibri")

    # header styling
    sheet["A1"].value = "Source"
    sheet["A1"].fill = FILL_A_0
    sheet["B1"].value = "Translation 1"
    for col in "BCDE":
        sheet[col + "1"].fill = FILL_B_0
    sheet["C1"].value = "T1 Adequacy"
    sheet["D1"].value = "T1 Fluency"
    sheet["E1"].value = "T1 Overall"
    sheet["F1"].value = "Translation 2"
    for col in "FGHI":
        sheet[col + "1"].fill = FILL_F_0
    sheet["G1"].value = "T2 Adequacy"
    sheet["H1"].value = "T2 Fluency"
    sheet["I1"].value = "T2 Overall"
    sheet["J1"].value = "Translation 3"
    for col in "JKLM":
        sheet[col + "1"].fill = FILL_J_0
    sheet["K1"].value = "T3 Adequacy"
    sheet["L1"].value = "T3 Fluency"
    sheet["M1"].value = "T3 Overall"
    sheet["N1"].value = "Translation 4"
    for col in "NOPQ":
        sheet[col + "1"].fill = FILL_N_0
    sheet["O1"].value = "T4 Adequacy"
    sheet["P1"].value = "T4 Fluency"
    sheet["Q1"].value = "T4 Overall"
    sheet["R1"].value = "Comments"

    for col in "CDEGHIKLMOPQ":
        sheet[col + "1"].alignment = Alignment(
            textRotation=90, horizontal="left"
        )
        sheet.column_dimensions[col].width = 4
    for col in "ABCDEFGHIJKLMNOPQR":
        sheet[col + "1"].border = THICK_BORDER_BOTTOM

    sheet.row_dimensions[1].height = 65
    sheet.freeze_panes = sheet["B2"]

    # fill values
    for line_i, line in enumerate(doc_v):
        line_i += 2
        for sent_i, (sent, col) in enumerate(zip(line, "ABFJNR")):
            cell = sheet[col + str(line_i)]
            if col == "A" or (line_i -1 >= DOC_SPANS[doc_k][0] and line_i -1 <= DOC_SPANS[doc_k][1]):
                cell.value = sent
            cell.alignment = Alignment(wrap_text=True)

        if line_i % 2 == 0:
            sheet["A" + str(line_i)].fill = FILL_A_1
            for col in "BCDE":
                sheet[col + str(line_i)].fill = FILL_B_1
            for col in "FGHI":
                sheet[col + str(line_i)].fill = FILL_F_1
            for col in "JKLM":
                sheet[col + str(line_i)].fill = FILL_J_1
            for col in "NOPQ":
                sheet[col + str(line_i)].fill = FILL_N_1

        # set borders
        for col in "BCDFGHJKLNOPR":
            sheet[col + str(line_i)].border = THIN_BORDER_ALL
        for col in "EIMQ":
            sheet[col + str(line_i)].border = MEDIUM_BORDER_RIGHT

        # add data validation
        for col in "CDEGHIKLMOPQ":
            NUM_VALIDATION.add(col + str(line_i))

        sheet["A" + str(line_i)].border = THICK_BORDER_RIGHT

        sheet.row_dimensions[line_i].height = 70

    line_i += 1
    sheet["A" + str(line_i+1)].value = "Document fluency"
    sheet["A" + str(line_i+2)].value = "Document adequacy"
    sheet["A" + str(line_i+3)].value = "Document overall"
    sheet["A" + str(line_i+1)].font = Font(bold=True, name="Calibri")
    sheet["A" + str(line_i+2)].font = Font(bold=True, name="Calibri")
    sheet["A" + str(line_i+3)].font = Font(bold=True, name="Calibri")

    for col in "BFJN":
        sheet[col + str(line_i+1)].border = MEDIUM_BORDER_ALL
        sheet[col + str(line_i+2)].border = MEDIUM_BORDER_ALL
        sheet[col + str(line_i+3)].border = MEDIUM_BORDER_ALL
        sheet[col + str(line_i+1)].border
        sheet[col + str(line_i+2)].border
        sheet[col + str(line_i+3)].border
        NUM_VALIDATION.add(col + str(line_i + 1))
        NUM_VALIDATION.add(col + str(line_i + 2))
        NUM_VALIDATION.add(col + str(line_i + 3))


    for col in "ABFJNR":
        sheet.column_dimensions[col].width = 60


def add_locked_sheet(workbook, doc_i, doc_k, doc_v):
    sheet = workbook.create_sheet("D" + str(doc_i) + "org")
    sheet.protection.sheet = True

    for col in "ABCDEFGHIJKLMNOPQR":
        sheet[col + "1"].font = Font(bold=True, name="Calibri")

    # header styling
    sheet["A1"].value = "Source"
    sheet["A1"].fill = FILL_A_0
    sheet["B1"].value = "Translation 1"
    sheet["B1"].fill = FILL_B_0
    sheet["C1"].value = "Translation 2"
    sheet["C1"].fill = FILL_F_0
    sheet["D1"].value = "Translation 3"
    sheet["D1"].fill = FILL_J_0
    sheet["E1"].value = "Translation 4"
    sheet["E1"].fill = FILL_N_0

    for col in "ABCDE":
        sheet[col + "1"].border = THICK_BORDER_BOTTOM

    sheet.row_dimensions[1].height = 65
    sheet.freeze_panes = sheet["B2"]

    # fill values
    for line_i, line in enumerate(doc_v):
        line_i += 2
        for sent_i, (sent, col) in enumerate(zip(line, "ABCDE")):
            cell = sheet[col + str(line_i)]
            if col == "A" or (line_i -1 >= DOC_SPANS[doc_k][0] and line_i -1 <= DOC_SPANS[doc_k][1]):
                cell.value = sent
            cell.alignment = Alignment(wrap_text=True)

        if line_i % 2 == 0:
            sheet["A" + str(line_i)].fill = FILL_A_1
            sheet["B" + str(line_i)].fill = FILL_B_1
            sheet["C" + str(line_i)].fill = FILL_F_1
            sheet["D" + str(line_i)].fill = FILL_J_1
            sheet["E" + str(line_i)].fill = FILL_N_1

        # set borders
        for col in "BCDE":
            sheet[col + str(line_i)].border = MEDIUM_BORDER_RIGHT

        sheet["A" + str(line_i)].border = THICK_BORDER_RIGHT
        sheet.row_dimensions[line_i].height = 70

    for col in "ABCDE":
        sheet.column_dimensions[col].width = 60

# sanitize keys
data = {
    k.strip(): v for k, v in data.items()
}

data = {
    k: v for k, v in data.items()
    if k in {
        'upi.205735', 'upi.205660', 'en.ndtv.com.13152', 'independent.281139',
    }
}

DOC_SPANS = {
    'upi.205735': (3, 11),
    'upi.205660': (1, 8),
    'en.ndtv.com.13152': (3, 11),
    'independent.281139': (3, 11),
}

for uid_i, uid in enumerate(UIDs[:3]):
    random.seed(uid_i)
    new_data = {}

    keys = list(data.keys())
    random.shuffle(keys)
    print(len(data.keys()), [len(data[k]) for k in keys])

    mapping = {
        "systems": {}, "docs": keys
    }

    for doc_k, doc_v in data.items():
        new_data[doc_k] = []

        # shuffle separatedly for each doc
        order = [1, 2, 3, 4]
        random.shuffle(order)
        mapping["systems"][doc_k] = order

        for sent in doc_v:
            new_sent = []
            for i in order:
                new_sent.append(sent[i])

            # source is always first
            new_data[doc_k].append([sent[0]] + new_sent)

    # save mapping
    save_json(f"data/mapping_{uid}.json", mapping)

    # generate XLSX document
    workbook = Workbook()
    # remove default sheet
    workbook.remove(workbook.active)

    for doc_i, (doc_k, doc_v) in enumerate(new_data.items()):
        doc_i += 1
        add_edit_sheet(workbook, doc_i, doc_k, doc_v)
        add_locked_sheet(workbook, doc_i, doc_k, doc_v)

    workbook.save(f"data/translations_{uid}.xlsx")
