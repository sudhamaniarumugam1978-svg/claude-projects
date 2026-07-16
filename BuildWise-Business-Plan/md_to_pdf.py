#!/usr/bin/env python3
"""Convert the BuildWise Business Plan Markdown report into a professionally
formatted PDF using the same design system as the .docx.

  Headings : Caladea (metric-compatible with Cambria), Dark Navy #163A6B
  Body     : Liberation Serif (metric-compatible with Times New Roman), justified
  Tables   : navy header (white) / serif body, alternating row shading
  Fallback : DejaVu Sans provides the rupee glyph missing from the serif fonts
"""

import os
import re
from fpdf import FPDF
from fpdf.enums import XPos, YPos, MethodReturnValue

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, "Business_Plan_Report.md")
OUT = os.path.join(BASE, "BuildWise_Business_Plan_Report.pdf")

NAVY = (22, 58, 107)      # #163A6B
GREY = (89, 89, 89)
BLACK = (33, 33, 33)
WHITE = (255, 255, 255)
ROW_ALT = (238, 242, 248)
RULE = (187, 187, 187)

F = "/usr/share/fonts"
CAL = f"{F}/caladea"
LIB = f"{F}/liberation-serif"
DVM = f"{F}/dejavu-sans-mono-fonts/DejaVuSansMono.ttf"
DVS = f"{F}/dejavu-sans-fonts/DejaVuSans.ttf"

FRONT_MATTER = {"DECLARATION", "ACKNOWLEDGEMENT", "TABLE OF CONTENTS"}


class PDF(FPDF):
    def header(self):
        if self.page_no() == 1:
            return
        self.set_y(9)
        self.set_font("Body", "", 9)
        self.set_text_color(*GREY)
        self.set_x(self.l_margin)
        self.cell(0, 5, "BuildWise Constructions Pvt. Ltd.  |  Business Plan Report",
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="R")
        self.set_draw_color(*RULE)
        self.set_line_width(0.2)
        self.line(self.l_margin, self.get_y() + 0.5, self.w - self.r_margin, self.get_y() + 0.5)
        self.ln(3)
        self.set_text_color(*BLACK)

    def footer(self):
        if self.page_no() == 1:
            return
        self.set_y(-12)
        self.set_font("Body", "", 9)
        self.set_text_color(*GREY)
        self.cell(0, 6, f"Page {self.page_no() - 1}", align="C")


pdf = PDF(format="A4")
pdf.set_margins(24, 16, 24)
pdf.set_auto_page_break(auto=True, margin=16)

pdf.add_font("Head", "", f"{CAL}/Caladea-Regular.ttf")
pdf.add_font("Head", "B", f"{CAL}/Caladea-Bold.ttf")
pdf.add_font("Head", "I", f"{CAL}/Caladea-Italic.ttf")
pdf.add_font("Head", "BI", f"{CAL}/Caladea-BoldItalic.ttf")
pdf.add_font("Body", "", f"{LIB}/LiberationSerif-Regular.ttf")
pdf.add_font("Body", "B", f"{LIB}/LiberationSerif-Bold.ttf")
pdf.add_font("Body", "I", f"{LIB}/LiberationSerif-Italic.ttf")
pdf.add_font("Body", "BI", f"{LIB}/LiberationSerif-BoldItalic.ttf")
pdf.add_font("Mono", "", DVM)
DVDIR = f"{F}/dejavu-sans-fonts"
pdf.add_font("DejaVu", "", f"{DVDIR}/DejaVuSans.ttf")
pdf.add_font("DejaVu", "B", f"{DVDIR}/DejaVuSans-Bold.ttf")
pdf.add_font("DejaVu", "I", f"{DVDIR}/DejaVuSans-Oblique.ttf")
pdf.add_font("DejaVu", "BI", f"{DVDIR}/DejaVuSans-BoldOblique.ttf")
pdf.set_fallback_fonts(["DejaVu"], exact_match=False)  # supplies the rupee glyph in any style

EPW = pdf.w - pdf.l_margin - pdf.r_margin


def strip_md(t):
    return t.replace("**", "").replace("*", "")


def wrapped_lines(text, width, font, style, size, markdown=False):
    """Exact wrapped-line count using fpdf2's own line breaker (dry run)."""
    pdf.set_font(font, style, size)
    out = pdf.multi_cell(width, 5, text, dry_run=True,
                         output=MethodReturnValue.LINES, markdown=markdown,
                         new_x=XPos.RIGHT, new_y=YPos.TOP)
    return max(len(out), 1)


# ------- inline bold/italic aware writer (used for body paragraphs) -------
INLINE_RE = re.compile(r"(\*\*.+?\*\*|\*[^*]+\*)")


def write_rich(text, size=11.5, color=BLACK, lh=5.9, align="J", base_style=""):
    """Render a paragraph with **bold**/*italic* using write() then break."""
    pdf.set_x(pdf.l_margin)
    pdf.set_text_color(*color)
    # fpdf2 write() supports justify only via multi_cell; use multi_cell with markdown
    pdf.set_font("Body", base_style, size)
    pdf.multi_cell(EPW, lh, _md_to_plain_marked(text), align=align,
                   new_x=XPos.LMARGIN, new_y=YPos.NEXT, markdown=True)


def _md_to_plain_marked(text):
    # fpdf2 markdown uses ** for bold and __ for italic; convert *italic* -> __italic__
    # protect bold first
    text = re.sub(r"\*\*(.+?)\*\*", r"@@B@@\1@@/B@@", text)
    text = re.sub(r"\*([^*]+)\*", r"__\1__", text)
    text = text.replace("@@B@@", "**").replace("@@/B@@", "**")
    return text


def heading_fit_size(text, base_size, min_size, font="Head", style="B"):
    size = base_size
    pdf.set_font(font, style, size)
    while pdf.get_string_width(text) > EPW and size > min_size:
        size -= 0.5
        pdf.set_font(font, style, size)
    return size


def ensure_space(min_mm):
    if pdf.get_y() + min_mm > pdf.page_break_trigger:
        pdf.add_page()


# ==================== TABLES ====================
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
    elif ncol == 4:
        widths = [EPW * 0.28, EPW * 0.24, EPW * 0.24, EPW * 0.24]
    else:
        widths = [EPW / ncol] * ncol
    line_h = 5.0
    pad = 1.4
    pdf.ln(1)
    alt = {"n": 0}

    def draw_row(cells, is_header=False):
        size = 11 if is_header else 10.5
        font = "Head" if is_header else "Body"
        style = "B" if is_header else ""
        nlines = max(wrapped_lines(cells[i], widths[i] - 2 * pad, font, style, size)
                     for i in range(ncol))
        h = nlines * line_h + 2 * pad
        if pdf.get_y() + h > pdf.page_break_trigger:
            pdf.add_page()
        x0 = pdf.l_margin
        y0 = pdf.get_y()
        x = x0
        for i, c in enumerate(cells):
            if is_header:
                pdf.set_fill_color(*NAVY)
                pdf.set_text_color(*WHITE)
            else:
                pdf.set_fill_color(*(ROW_ALT if alt["n"] % 2 else WHITE))
                pdf.set_text_color(*BLACK)
            pdf.set_draw_color(*RULE)
            pdf.set_line_width(0.2)
            pdf.rect(x, y0, widths[i], h, style="DF")
            pdf.set_xy(x + pad, y0 + pad)
            pdf.set_font(font, style, size)
            pdf.multi_cell(widths[i] - 2 * pad, line_h, c, align="L",
                           new_x=XPos.RIGHT, new_y=YPos.TOP)
            x += widths[i]
        pdf.set_xy(x0, y0 + h)
        if not is_header:
            alt["n"] += 1

    draw_row(header, is_header=True)
    for cells in body:
        draw_row(cells)
    pdf.ln(3)
    pdf.set_text_color(*BLACK)


def render_code(codelines):
    while codelines and not codelines[0].strip():
        codelines.pop(0)
    while codelines and not codelines[-1].strip():
        codelines.pop()
    line_h = 4.7
    block_h = len(codelines) * line_h + 4
    if pdf.get_y() + block_h > pdf.page_break_trigger:
        pdf.add_page()
    pdf.ln(1)
    pdf.set_font("Mono", "", 9)
    pdf.set_text_color(*NAVY)
    pdf.set_fill_color(245, 247, 250)
    for ln in codelines:
        pdf.set_x(pdf.l_margin)
        pdf.cell(EPW, line_h, ln, new_x=XPos.LMARGIN, new_y=YPos.NEXT, fill=True, align="C")
    pdf.ln(3)
    pdf.set_text_color(*BLACK)


def render_image(path, caption=None):
    from PIL import Image
    iw, ih = Image.open(path).size
    disp_w = min(EPW, 140)
    disp_h = disp_w * ih / iw
    needed = disp_h + (10 if caption else 5)
    if pdf.get_y() + needed > pdf.page_break_trigger:
        pdf.add_page()
    x = pdf.l_margin + (EPW - disp_w) / 2
    pdf.ln(2)
    pdf.image(path, x=x, w=disp_w)
    pdf.ln(1)
    if caption:
        pdf.set_font("Body", "I", 9.5)
        pdf.set_text_color(*GREY)
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(EPW, 5, caption, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(2)
    pdf.set_text_color(*BLACK)


# ==================== COVER ====================
def cover_center(text, font, style, size, color, sa=6, sb=0):
    if sb:
        pdf.ln(sb)
    pdf.set_font(font, style, size)
    pdf.set_text_color(*color)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(EPW, size * 0.48, text, align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(sa)


def cover_divider(sb=4, sa=6, half=False):
    pdf.ln(sb)
    pdf.set_draw_color(*NAVY)
    pdf.set_line_width(0.5)
    x1 = pdf.l_margin + (EPW * 0.2 if half else 0)
    x2 = pdf.w - pdf.r_margin - (EPW * 0.2 if half else 0)
    pdf.line(x1, pdf.get_y(), x2, pdf.get_y())
    pdf.ln(sa)


def build_cover():
    pdf.add_page()
    pdf.set_auto_page_break(False)   # keep the whole cover on one page
    pdf.ln(10)
    cover_center("BUILDWISE CONSTRUCTIONS PVT. LTD.", "Head", "B", 26, NAVY, sa=3)
    cover_center('"Building Trust Through Technology and Quality Construction"',
                 "Head", "I", 14, GREY, sa=7)
    cover_center("BUSINESS PLAN REPORT", "Head", "B", 19, NAVY, sa=2)
    cover_divider(sb=3, sa=8)

    # business details (aligned colons)
    details = [
        ("Industry", "Construction"),
        ("Business Model", "Technology-Enabled Construction Startup"),
        ("Location", "Chennai, Tamil Nadu, India"),
        ("Initial Capital", "\u20b91.00 Crore"),
        ("Academic Year", "2026"),
    ]
    x_label = pdf.l_margin + 14
    x_colon = x_label + 42
    row_h = 6.8
    for label, value in details:
        y = pdf.get_y()
        pdf.set_xy(x_label, y)
        pdf.set_font("Head", "B", 12)
        pdf.set_text_color(*NAVY)
        pdf.cell(42, row_h, label)
        pdf.set_xy(x_colon, y)
        pdf.cell(5, row_h, ":")
        pdf.set_font("Body", "", 12)
        pdf.set_text_color(*BLACK)
        pdf.set_xy(x_colon + 5, y)
        pdf.cell(EPW - (x_colon + 5 - pdf.l_margin), row_h, value)
        pdf.ln(row_h)

    cover_divider(sb=6, sa=7)

    cover_center("PREPARED BY", "Head", "B", 14, NAVY, sa=4)
    team = [
        ("THILAK KUMAR K", "RA2311042040014"),
        ("ARJUN S", "RA2311042040018"),
        ("SANJAY KUMAR A M", "RA2311042040024"),
    ]
    for name, reg in team:
        cover_center(name, "Head", "B", 13, BLACK, sa=1)
        cover_center(reg, "Body", "", 11, GREY, sa=4)

    cover_divider(sb=5, sa=6)

    cover_center("Entrepreneurship and Family Business Management", "Head", "", 12, NAVY, sa=5)
    cover_center("Department of Computer Science and Engineering (Emerging Technologies)",
                 "Head", "", 12, BLACK, sa=1)
    cover_center("& Computer Science and Business Systems (Final Year)",
                 "Head", "", 12, BLACK, sa=7)
    cover_center("SRM Institute of Science and Technology", "Head", "B", 13, NAVY, sa=1)
    cover_center("Vadapalani Campus, Chennai", "Body", "", 12, BLACK, sa=0)
    pdf.set_auto_page_break(True, margin=16)   # restore for the body


# ==================== BUILD ====================
build_cover()

with open(SRC, encoding="utf-8") as f:
    lines = f.read().split("\n")

# body begins on a fresh page
i = 0
first_chapter = True
while i < len(lines):
    stripped = lines[i].strip()

    # image
    im = re.match(r"^!\[(.*?)\]\((.*?)\)\s*$", stripped)
    if im:
        img_path = os.path.join(BASE, im.group(2))
        caption = None
        j = i + 1
        while j < len(lines) and lines[j].strip() == "":
            j += 1
        if j < len(lines) and re.match(r"^\*Figure.*\*$", lines[j].strip()):
            caption = lines[j].strip().strip("*")
            i = j
        if os.path.exists(img_path):
            render_image(img_path, caption)
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
            # Flowing chapters: the first chapter starts on a fresh page; later
            # chapters continue on the current page unless little room remains,
            # which keeps pages full and avoids large blank areas.
            if first_chapter:
                pdf.add_page()
                first_chapter = False
            elif pdf.get_y() > pdf.page_break_trigger - 78:
                pdf.add_page()
            else:
                pdf.ln(9)
            size = heading_fit_size(text, 18, 13)
            pdf.set_font("Head", "B", size)
            pdf.set_text_color(*NAVY)
            pdf.set_x(pdf.l_margin)
            pdf.cell(0, 10, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.set_draw_color(*NAVY)
            pdf.set_line_width(0.5)
            pdf.line(pdf.l_margin, pdf.get_y() + 0.5, pdf.w - pdf.r_margin, pdf.get_y() + 0.5)
            pdf.ln(5)
            pdf.set_text_color(*BLACK)
        elif level == 2 and text.upper() in FRONT_MATTER:
            # Declaration and Table of Contents start their own page; the short
            # Acknowledgement flows directly under the Declaration.
            if text.upper() == "ACKNOWLEDGEMENT":
                pdf.ln(10)
            else:
                pdf.add_page()
                pdf.ln(2)
            pdf.set_font("Head", "B", 16)
            pdf.set_text_color(*NAVY)
            pdf.set_x(pdf.l_margin)
            pdf.multi_cell(EPW, 9, text.upper(), align="C",
                           new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.ln(4)
            pdf.set_text_color(*BLACK)
        else:
            sz = {2: 14, 3: 12, 4: 11}.get(level, 11)
            ensure_space(20)
            pdf.ln(2 if level == 2 else 1)
            size = heading_fit_size(text, sz, 10)
            pdf.set_font("Head", "B", size)
            pdf.set_text_color(*NAVY)
            pdf.set_x(pdf.l_margin)
            pdf.multi_cell(EPW, size * 0.5, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.ln(1)
            pdf.set_text_color(*BLACK)
        i += 1
        continue

    if stripped.startswith(">"):
        text = strip_md(stripped.lstrip(">").strip())
        if text:
            ensure_space(16)
            pdf.set_font("Body", "I", 11)
            nlines = wrapped_lines(text, EPW - 10, "Body", "I", 11)
            h = nlines * 5.6 + 4
            y0 = pdf.get_y()
            pdf.set_fill_color(*ROW_ALT)
            pdf.rect(pdf.l_margin, y0, EPW, h, style="F")
            pdf.set_xy(pdf.l_margin + 5, y0 + 2)
            pdf.set_text_color(*NAVY)
            pdf.multi_cell(EPW - 10, 5.6, text, align="C",
                           new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.set_y(y0 + h)
            pdf.ln(3)
            pdf.set_text_color(*BLACK)
        i += 1
        continue

    if stripped.startswith("- "):
        text = _md_to_plain_marked(stripped[2:])
        bullet_w = 6
        nlines = wrapped_lines(text, EPW - 2 - bullet_w, "Body", "", 11.5, markdown=True)
        h = nlines * 5.8
        if pdf.get_y() + h > pdf.page_break_trigger:  # keep bullet whole
            pdf.add_page()
        y0 = pdf.get_y()
        pdf.set_font("Body", "", 11.5)
        pdf.set_text_color(*BLACK)
        pdf.set_xy(pdf.l_margin + 2, y0)
        pdf.cell(bullet_w, 5.8, "\u2022")
        pdf.set_xy(pdf.l_margin + 2 + bullet_w, y0)
        pdf.multi_cell(EPW - 2 - bullet_w, 5.8, text,
                       align="L", new_x=XPos.LMARGIN, new_y=YPos.NEXT, markdown=True)
        pdf.set_y(max(pdf.get_y(), y0 + h))
        i += 1
        continue

    om = re.match(r"^(\d+)\.\s+(.*)$", stripped)
    if om:
        txt = strip_md(om.group(2))
        nlines = wrapped_lines(txt, EPW - 10, "Body", "", 11.5)
        h = nlines * 5.8
        if pdf.get_y() + h > pdf.page_break_trigger:
            pdf.add_page()
        y0 = pdf.get_y()
        pdf.set_font("Body", "", 11.5)
        pdf.set_text_color(*BLACK)
        pdf.set_xy(pdf.l_margin + 2, y0)
        pdf.cell(8, 5.8, f"{om.group(1)}.")
        pdf.set_xy(pdf.l_margin + 10, y0)
        pdf.multi_cell(EPW - 10, 5.8, txt, align="L",
                       new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_y(max(pdf.get_y(), y0 + h))
        i += 1
        continue

    if stripped == "":
        i += 1
        continue

    # normal paragraph
    write_rich(stripped, size=11.5, color=BLACK, lh=5.9, align="J")
    pdf.ln(1.5)
    i += 1

pdf.output(OUT)
print("Saved:", OUT)
