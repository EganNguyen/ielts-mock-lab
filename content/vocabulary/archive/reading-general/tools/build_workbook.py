"""Build the printable vocabulary workbook from the JSON source of truth."""
import json
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo

ROOT = Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / "ielts20-21-vocabulary.json").read_text(encoding="utf-8"))
OUT = ROOT / "ielts20-21-vocabulary.xlsx"

INK = "111111"
GREEN = "1D7A46"
PAPER = "F3F4F6"
LINE = "D3D7DC"
AMBER = "FFF4D6"
BLUE = "E8F0FD"
WHITE = "FFFFFF"

thin = Side(style="thin", color=LINE)
border = Border(left=thin, right=thin, top=thin, bottom=thin)
header_fill = PatternFill("solid", fgColor=INK)
header_font = Font(name="Calibri", size=10, bold=True, color=WHITE)
body_font = Font(name="Calibri", size=10, color=INK)
muted_font = Font(name="Calibri", size=10, color="555B61")
title_font = Font(name="Calibri", size=24, bold=True, color=INK)
subtitle_font = Font(name="Calibri", size=12, color="555B61")
section_font = Font(name="Calibri", size=12, bold=True, color=INK)

wb = Workbook()

# ---------- Overview ----------
ws = wb.active
ws.title = "Overview"
ws.sheet_view.showGridLines = False
ws.column_dimensions["A"].width = 3
ws.column_dimensions["B"].width = 34
ws.column_dimensions["C"].width = 26
ws.column_dimensions["D"].width = 26
ws.column_dimensions["E"].width = 26

ws["B2"] = "IELTS 20 & 21 Academic"
ws["B2"].font = Font(name="Calibri", size=11, bold=True, color="555B61")
ws["B3"] = "Reading vocabulary workbook"
ws["B3"].font = title_font
ws["B4"] = f"{DATA['meta']['totalWords']} words from {DATA['meta']['totalPassages']} Reading passages · 8 complete Academic tests"
ws["B4"].font = subtitle_font
ws.merge_cells("B4:E4")

ws["B6"] = "What this is"
ws["B6"].font = section_font
ws["B7"] = ("A study set selected from every Reading passage in IELTS 20 Academic and Cambridge IELTS 21 Academic. "
            "Each word is shown with the meaning it carries in that passage and the sentence it came from, "
            "so revision stays tied to real exam text rather than a generic word list.")
ws["B7"].alignment = Alignment(wrap_text=True, vertical="top")
ws.merge_cells("B7:E9")

ws["B11"] = "At a glance"
ws["B11"].font = section_font
stats = [
    ("Words", DATA["meta"]["totalWords"]),
    ("Reading passages", DATA["meta"]["totalPassages"]),
    ("Tests", DATA["meta"]["totalTests"]),
    ("Words per passage", 15),
]
for i, (label, value) in enumerate(stats):
    r = 12 + i
    ws[f"B{r}"] = label
    ws[f"B{r}"].font = muted_font
    ws[f"C{r}"] = value
    ws[f"C{r}"].font = Font(name="Calibri", size=12, bold=True)
    ws[f"C{r}"].alignment = Alignment(horizontal="left")

ws["B17"] = "Level mix"
ws["B17"].font = section_font
levels = DATA["meta"]["levels"]
row = 18
for label in ["B1", "B2", "C1", "C2"]:
    count = levels.get(label, 0)
    if not count:
        continue
    ws[f"B{row}"] = label
    ws[f"B{row}"].font = Font(name="Calibri", size=11, bold=True)
    ws[f"C{row}"] = count
    ws[f"C{row}"].font = body_font
    row += 1

ws["B23"] = "How to use it"
ws["B23"].font = section_font
tips = [
    "Start with the Vocabulary sheet and filter by Book, Test, Passage or CEFR level.",
    "Read the example sentence aloud, then cover the definition and explain the word in your own words.",
    "Use the By passage sheet to revise one passage at a time after you finish it.",
    "The Flashcards sheet is laid out for printing and cutting into two-sided cards.",
    "The same content is available in the mock lab at /vocabulary/ with search and flashcards.",
]
for i, tip in enumerate(tips):
    r = 24 + i
    ws[f"B{r}"] = f"•  {tip}"
    ws[f"B{r}"].alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells(f"B{r}:E{r}")

ws["B30"] = "Source and copyright"
ws["B30"].font = section_font
ws["B31"] = ("Passages and example sentences: IELTS 20 Academic and Cambridge IELTS 21 Academic, "
             "© Cambridge University Press & Assessment and Qunyan Press. Included for private study only; "
             "do not redistribute. Definitions, CEFR labels and IPA are study aids, not official IELTS materials.")
ws["B31"].alignment = Alignment(wrap_text=True, vertical="top")
ws.merge_cells("B31:E34")

ws["B36"] = "Vocabulary selection and definitions: local study pack, 2026."
ws["B36"].font = Font(name="Calibri", size=9, italic=True, color="7A8086")

# ---------- Vocabulary ----------
ws = wb.create_sheet("Vocabulary")
headers = ["#", "Word", "Part of speech", "CEFR", "IPA (UK)", "Definition", "Example from the passage",
           "Book", "Test", "Passage", "Passage title", "Topic", "Paragraph"]
widths = [5, 18, 14, 7, 18, 48, 76, 11, 7, 9, 34, 24, 10]
for i, (h, w) in enumerate(zip(headers, widths), start=1):
    cell = ws.cell(row=1, column=i, value=h)
    cell.font = header_font
    cell.fill = header_fill
    cell.alignment = Alignment(horizontal="left", vertical="center")
    cell.border = border
    ws.column_dimensions[get_column_letter(i)].width = w
ws.row_dimensions[1].height = 28

for n, word in enumerate(DATA["words"], start=1):
    r = n + 1
    values = [n, word["word"], word["pos"], word["level"], word["ipa"], word["definition"],
              word["example"], word["book"], word["test"], word["passage"], word["passageTitle"],
              word["theme"], word["paragraph"]]
    for c, value in enumerate(values, start=1):
        cell = ws.cell(row=r, column=c, value=value)
        cell.font = body_font
        cell.border = border
        cell.alignment = Alignment(vertical="top", wrap_text=c in (6, 7, 11, 12))
        if c in (1, 4, 9, 10, 13):
            cell.alignment = Alignment(horizontal="center", vertical="top")
    if word["level"] == "C1":
        ws.cell(row=r, column=4).fill = PatternFill("solid", fgColor=AMBER)
    elif word["level"] == "B2":
        ws.cell(row=r, column=4).fill = PatternFill("solid", fgColor=BLUE)

ws.freeze_panes = "B2"
ws.auto_filter.ref = f"A1:M{len(DATA['words']) + 1}"
ws.sheet_view.zoomScale = 90

# ---------- By passage ----------
ws = wb.create_sheet("By passage")
headers = ["Book", "Test", "Passage", "Passage title", "Topic", "Words"]
widths = [11, 7, 9, 40, 24, 105]
for i, (h, w) in enumerate(zip(headers, widths), start=1):
    cell = ws.cell(row=1, column=i, value=h)
    cell.font = header_font
    cell.fill = header_fill
    cell.alignment = Alignment(horizontal="left", vertical="center")
    cell.border = border
    ws.column_dimensions[get_column_letter(i)].width = w
ws.row_dimensions[1].height = 28
by_id = {w["id"]: w for w in DATA["words"]}
for r, passage in enumerate(DATA["passages"], start=2):
    words = [by_id[i]["word"] for i in passage["words"]]
    values = [passage["book"], passage["test"], passage["passage"], passage["title"], passage["theme"], ", ".join(words)]
    for c, value in enumerate(values, start=1):
        cell = ws.cell(row=r, column=c, value=value)
        cell.font = body_font
        cell.border = border
        cell.alignment = Alignment(vertical="top", wrap_text=c in (4, 5, 6))
ws.freeze_panes = "A2"
ws.auto_filter.ref = f"A1:F{len(DATA['passages']) + 1}"

# ---------- Flashcards ----------
ws = wb.create_sheet("Flashcards")
ws.sheet_view.showGridLines = False
for col, w in {"A": 3, "B": 28, "C": 68, "D": 3}.items():
    ws.column_dimensions[col].width = w
ws["B1"] = "Front"
ws["C1"] = "Back"
for c in ("B1", "C1"):
    ws[c].font = header_font
    ws[c].fill = header_fill
    ws[c].alignment = Alignment(horizontal="center", vertical="center")
    ws[c].border = border
ws.row_dimensions[1].height = 24
for r, word in enumerate(DATA["words"], start=2):
    ws[f"B{r}"] = f"{word['word']}\n{word['ipa']}\n{word['level']} · {word['pos']}"
    ws[f"C{r}"] = f"{word['definition']}\n\n{word['example']}"
    for c in (f"B{r}", f"C{r}"):
        ws[c].font = body_font
        ws[c].border = border
        ws[c].alignment = Alignment(wrap_text=True, vertical="top")
    ws.row_dimensions[r].height = 54
ws.freeze_panes = "A2"

wb.save(OUT)
print(f"Wrote {OUT} ({OUT.stat().st_size:,} bytes)")
