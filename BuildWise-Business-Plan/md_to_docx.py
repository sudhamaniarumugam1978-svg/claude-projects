#!/usr/bin/env python3
"""Convert the BuildWise Business Plan Markdown report into a formatted .docx."""

import re
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

SRC = "/projects/sandbox/claude-projects/BuildWise-Business-Plan/Business_Plan_Report.md"
OUT = "/projects/sandbox/claude-projects/BuildWise-Business-Plan/BuildWise_Business_Plan_Report.docx"

doc = Document()

# Base styles
normal = doc.styles["Normal"]
normal.font.name = "Calibri"
normal.font.size = Pt(11)
normal.paragraph_format.space_after = Pt(6)
normal.paragraph_format.line_spacing = 1.15

for lvl, sz, color in [(1, 18, "1F3864"), (2, 14, "2E5496"), (3, 12, "2E5496"), (4, 11, "44546A")]:
    st = doc.styles[f"Heading {lvl}"]
    st.font.name = "Calibri"
    st.font.size = Pt(sz)
    st.font.color.rgb = RGBColor.from_string(color)
    st.font.bold = True


def add_runs(paragraph, text):
    """Add text to a paragraph, honouring **bold** markup."""
    parts = re.split(r"(\*\*.+?\*\*)", text)
    for part in parts:
        if part.startswith("**") and part.endswith("**"):
            run = paragraph.add_run(part[2:-2])
            run.bold = True
        else:
            paragraph.add_run(part)


def shade_cell(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:fill"), hex_color)
    tcPr.append(shd)


def add_table(rows):
    header = [c.strip() for c in rows[0].strip().strip("|").split("|")]
    body = []
    for r in rows[2:]:
        cells = [c.strip() for c in r.strip().strip("|").split("|")]
        body.append(cells)
    table = doc.add_table(rows=1, cols=len(header))
    table.style = "Light Grid Accent 1"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = table.rows[0].cells
    for i, h in enumerate(header):
        hdr[i].paragraphs[0].text = ""
        add_runs(hdr[i].paragraphs[0], h)
        for run in hdr[i].paragraphs[0].runs:
            run.bold = True
        shade_cell(hdr[i], "1F3864")
        for run in hdr[i].paragraphs[0].runs:
            run.font.color.rgb = RGBColor.from_string("FFFFFF")
    for cells in body:
        row = table.add_row().cells
        for i in range(len(header)):
            txt = cells[i] if i < len(cells) else ""
            row[i].paragraphs[0].text = ""
            add_runs(row[i].paragraphs[0], txt)
    doc.add_paragraph()


def add_code_block(lines):
    for ln in lines:
        p = doc.add_paragraph()
        run = p.add_run(ln if ln else " ")
        run.font.name = "Consolas"
        run.font.size = Pt(9.5)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.0
    doc.add_paragraph()


with open(SRC, encoding="utf-8") as f:
    lines = f.read().split("\n")

i = 0
first_h1 = True
while i < len(lines):
    line = lines[i]

    # Code block
    if line.strip().startswith("```"):
        block = []
        i += 1
        while i < len(lines) and not lines[i].strip().startswith("```"):
            block.append(lines[i])
            i += 1
        add_code_block(block)
        i += 1
        continue

    # Table
    if line.strip().startswith("|") and i + 1 < len(lines) and re.match(r"^\|[\s:\-|]+\|?$", lines[i + 1].strip()):
        tbl = []
        while i < len(lines) and lines[i].strip().startswith("|"):
            tbl.append(lines[i])
            i += 1
        add_table(tbl)
        continue

    stripped = line.strip()

    # Horizontal rule -> page break before major chapter handled by headings; skip rule
    if stripped == "---":
        i += 1
        continue

    # Headings
    m = re.match(r"^(#{1,6})\s+(.*)$", stripped)
    if m:
        level = len(m.group(1))
        text = m.group(2).strip()
        if level == 1:
            if not first_h1:
                doc.add_page_break()
            first_h1 = False
            h = doc.add_heading(level=1)
            add_runs(h, text)
        else:
            h = doc.add_heading(level=min(level, 4))
            add_runs(h, text)
        i += 1
        continue

    # Blockquote
    if stripped.startswith(">"):
        text = stripped.lstrip(">").strip()
        if text:
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Inches(0.4)
            r = p.add_run("")
            add_runs(p, text)
            for run in p.runs:
                run.italic = True
        i += 1
        continue

    # Bullet list
    if stripped.startswith("- "):
        p = doc.add_paragraph(style="List Bullet")
        add_runs(p, stripped[2:])
        i += 1
        continue

    # Ordered list (TOC)
    om = re.match(r"^\d+\.\s+(.*)$", stripped)
    if om:
        p = doc.add_paragraph(style="List Number")
        add_runs(p, om.group(1))
        i += 1
        continue

    # Blank line
    if stripped == "":
        i += 1
        continue

    # Regular paragraph
    p = doc.add_paragraph()
    add_runs(p, stripped)
    i += 1

# Title styling: center the very first block and subtitle
doc.save(OUT)
print("Saved:", OUT)
