#!/usr/bin/env python3
"""Convert the BuildWise Business Plan Markdown report into a formatted PDF."""

import re
from fpdf import FPDF
from fpdf.enums import XPos, YPos

SRC = "/projects/sandbox/claude-projects/BuildWise-Business-Plan/Business_Plan_Report.md"
OUT = "/projects/sandbox/claude-projects/BuildWise-Business-Plan/BuildWise_Business_Plan_Report.pdf"

DARK = (31, 56, 100)
BLUE = (46, 84, 150)
GREY = (240, 242, 246)
WHITE = (255, 255, 255)

FONT_DIR = "/usr/share/fonts"
REG = f"{FONT_DIR}/dejavu-sans-fonts/DejaVuSans.ttf"
BOLD = f"{FONT_DIR}/dejavu-sans-fonts/DejaVuSans-Bold.ttf"
ITAL = f"{FONT_DIR}/dejavu-sans-fonts/DejaVuSans-Oblique.ttf"
MONO = f"{FONT_DIR}/dejavu-sans-mono-fonts/DejaVuSansMono.ttf"


class PDF(FPDF):
    def header(self):
        if self.page_no() == 1:
            return
        self.set_font("DejaVu", "", 8)
        self.set_text_color(150, 150, 150)
        self.set_x(self.l_margin)
        self.cell(0, 6, "BuildWise Constructions Pvt. Ltd. — Business Plan Report",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="R")
        self.set_draw_color(210, 210, 210)
        self.line(self.l_margin, self.get_y(), self.w - self.r_margin, self.get_y())
        self.ln(2)
        self.set_text_color(40, 40, 40)

    def footer(self):
        if self.page_no() == 1:
            return
        self.set_y(-13)
        self.set_font("DejaVu", "", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 8, f"Page {self.page_no() - 1}", align="C")

    def mc(self, w, h, txt, align="L", fill=False):
        """multi_cell that always resets cursor to the left margin afterwards."""
        self.set_x(self.l_margin)
        self.multi_cell(w, h, txt, align=align, fill=fill,
                        new_x=XPos.LMARGIN, new_y=YPos.NEXT)


pdf = PDF(format="A4")
pdf.set_margins(20, 18, 20)
pdf.set_auto_page_break(auto=True, margin=16)
pdf.add_font("DejaVu", "", REG)
pdf.add_font("DejaVu", "B", BOLD)
pdf.add_font("DejaVu", "I", ITAL)
pdf.add_font("Mono", "", MONO)

EPW = pdf.w - pdf.l_margin - pdf.r_margin


def strip_md(text):
    return text.replace("**", "")


def wrapped_lines(text, width, font_style, size):
    """Estimate number of lines a string needs within width (mm)."""
    pdf.set_font("DejaVu", font_style, size)
    words = text.split(" ")
    if not words:
        return 1
    lines, cur = 0, ""
    for wd in words:
        trial = wd if cur == "" else cur + " " + wd
        if pdf.get_string_width(trial) <= width - 1:
            cur = trial
        else:
            lines += 1
            cur = wd
    if cur:
        lines += 1
    return max(lines, 1)


# ---------- Title page ----------
pdf.add_page()
pdf.ln(28)
pdf.set_text_color(*DARK)
pdf.set_font("DejaVu", "B", 25)
pdf.mc(0, 12, "BuildWise Constructions Pvt. Ltd.", align="C")
pdf.ln(2)
pdf.set_font("DejaVu", "I", 14)
pdf.set_text_color(*BLUE)
pdf.mc(0, 8, '"Building Trust, Brick by Brick"', align="C")
pdf.ln(3)
pdf.set_font("DejaVu", "", 13)
pdf.set_text_color(60, 60, 60)
pdf.mc(0, 8, "A Technology-Enabled Construction Startup", align="C")
pdf.ln(6)
pdf.set_font("DejaVu", "B", 16)
pdf.set_text_color(*DARK)
pdf.mc(0, 9, "BUSINESS PLAN REPORT", align="C")
pdf.ln(16)
pdf.set_draw_color(*DARK)
pdf.set_line_width(0.6)
pdf.line(60, pdf.get_y(), pdf.w - 60, pdf.get_y())
pdf.ln(10)
pdf.set_font("DejaVu", "", 11)
pdf.set_text_color(70, 70, 70)
for row in [
    "Industry: Construction",
    "Business Type: Technology-Enabled Construction Startup",
    "Registered Location: Coimbatore, Tamil Nadu, India",
    "Year of Establishment: 2026",
    "Startup Capital: Rs. 1.00 Crore",
    "Academic Year: 2026",
]:
    pdf.mc(0, 8, row, align="C")


def render_table(rows):
    header = [strip_md(c.strip()) for c in rows[0].strip().strip("|").split("|")]
    body = []
    for r in rows[2:]:
        cells = [strip_md(c.strip()) for c in r.strip().strip("|").split("|")]
        while len(cells) < len(header):
            cells.append("")
        body.append(cells[:len(header)])
    ncol = len(header)

    if ncol == 2:
        widths = [EPW * 0.40, EPW * 0.60]
    elif ncol == 3:
        widths = [EPW * 0.34, EPW * 0.33, EPW * 0.33]
    else:
        widths = [EPW / ncol] * ncol

    line_h = 5.0
    pdf.ln(1)
    alt = {"n": 0}

    def draw_row(cells, is_header=False):
        size = 9 if is_header else 8.5
        style = "B" if is_header else ""
        h = max(wrapped_lines(cells[i], widths[i] - 3, style, size) for i in range(ncol)) * line_h + 2.0
        if pdf.get_y() + h > pdf.page_break_trigger:
            pdf.add_page()
        x0 = pdf.l_margin
        y0 = pdf.get_y()
        x = x0
        for i, c in enumerate(cells):
            if is_header:
                pdf.set_fill_color(*DARK)
                pdf.set_text_color(*WHITE)
            else:
                pdf.set_fill_color(*(GREY if alt["n"] % 2 else WHITE))
                pdf.set_text_color(40, 40, 40)
            pdf.set_font("DejaVu", style, size)
            pdf.set_draw_color(205, 205, 205)
            pdf.set_line_width(0.2)
            pdf.rect(x, y0, widths[i], h, style="DF")
            pdf.set_xy(x + 1.5, y0 + 1.0)
            pdf.multi_cell(widths[i] - 3, line_h, c, align="L",
                           new_x=XPos.RIGHT, new_y=YPos.TOP)
            x += widths[i]
        pdf.set_xy(x0, y0 + h)
        if not is_header:
            alt["n"] += 1

    draw_row(header, is_header=True)
    for cells in body:
        draw_row(cells)
    pdf.ln(2.5)
    pdf.set_text_color(40, 40, 40)


def render_code(codelines):
    pdf.ln(1)
    pdf.set_font("Mono", "", 8.3)
    pdf.set_fill_color(245, 246, 248)
    pdf.set_text_color(45, 45, 45)
    for ln in codelines:
        if pdf.get_y() + 4.5 > pdf.page_break_trigger:
            pdf.add_page()
        pdf.set_x(pdf.l_margin)
        pdf.cell(EPW, 4.5, ln, new_x=XPos.LMARGIN, new_y=YPos.NEXT, fill=True)
    pdf.ln(2.5)
    pdf.set_text_color(40, 40, 40)


# ---------- Parse body ----------
with open(SRC, encoding="utf-8") as f:
    lines = f.read().split("\n")

started = False
i = 0
while i < len(lines):
    line = lines[i]
    stripped = line.strip()

    if not started:
        if stripped.startswith("## TABLE OF CONTENTS") or stripped.startswith("# CHAPTER") or stripped.startswith("## DECLARATION"):
            started = True
            pdf.add_page()
        else:
            i += 1
            continue

    if stripped.startswith("```"):
        block = []
        i += 1
        while i < len(lines) and not lines[i].strip().startswith("```"):
            block.append(lines[i])
            i += 1
        render_code(block)
        i += 1
        continue

    if stripped.startswith("|") and i + 1 < len(lines) and re.match(r"^\|[\s:\-|]+\|?$", lines[i + 1].strip()):
        tbl = []
        while i < len(lines) and lines[i].strip().startswith("|"):
            tbl.append(lines[i])
            i += 1
        render_table(tbl)
        continue

    if stripped == "---":
        i += 1
        continue

    m = re.match(r"^(#{1,6})\s+(.*)$", stripped)
    if m:
        level = len(m.group(1))
        text = strip_md(m.group(2).strip())
        if level == 1:
            pdf.add_page()
            pdf.set_font("DejaVu", "B", 17)
            pdf.set_text_color(*DARK)
            pdf.mc(0, 9, text)
            pdf.set_draw_color(*DARK)
            pdf.set_line_width(0.5)
            pdf.line(pdf.l_margin, pdf.get_y() + 1, pdf.w - pdf.r_margin, pdf.get_y() + 1)
            pdf.ln(4)
        elif level == 2:
            pdf.ln(2)
            pdf.set_font("DejaVu", "B", 13)
            pdf.set_text_color(*BLUE)
            pdf.mc(0, 7, text)
            pdf.ln(0.5)
        elif level == 3:
            pdf.ln(1)
            pdf.set_font("DejaVu", "B", 11)
            pdf.set_text_color(*BLUE)
            pdf.mc(0, 6, text)
        else:
            pdf.set_font("DejaVu", "B", 10)
            pdf.set_text_color(60, 60, 60)
            pdf.mc(0, 6, text)
        pdf.set_text_color(40, 40, 40)
        i += 1
        continue

    if stripped.startswith(">"):
        text = strip_md(stripped.lstrip(">").strip())
        if text:
            pdf.set_font("DejaVu", "I", 10.5)
            pdf.set_fill_color(238, 242, 248)
            pdf.set_text_color(*DARK)
            pdf.mc(EPW, 6, text, fill=True)
            pdf.ln(1)
            pdf.set_text_color(40, 40, 40)
        i += 1
        continue

    if stripped.startswith("- "):
        text = strip_md(stripped[2:])
        pdf.set_font("DejaVu", "", 10.5)
        pdf.set_text_color(40, 40, 40)
        pdf.mc(EPW, 5.6, "\u2022  " + text)
        i += 1
        continue

    om = re.match(r"^(\d+)\.\s+(.*)$", stripped)
    if om:
        pdf.set_font("DejaVu", "", 10.5)
        pdf.set_text_color(40, 40, 40)
        pdf.mc(0, 6, f"{om.group(1)}.  {strip_md(om.group(2))}")
        i += 1
        continue

    if stripped == "":
        pdf.ln(2)
        i += 1
        continue

    pdf.set_font("DejaVu", "", 10.5)
    pdf.set_text_color(40, 40, 40)
    pdf.mc(0, 5.8, strip_md(stripped))
    i += 1

pdf.output(OUT)
print("Saved:", OUT)
