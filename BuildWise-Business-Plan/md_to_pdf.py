#!/usr/bin/env python3
"""Convert the BuildWise Business Plan Markdown report into a professionally
formatted PDF matching the lecturer's sample university-report style.

  Headings : Caladea (metric-compatible with Cambria), Dark Navy #163A6B
  Body     : Liberation Serif (metric-compatible with Times New Roman), 12 pt justified
  Tables   : navy header (white) / serif body, alternating row shading
  Layout   : every chapter starts on a new page; bordered Table of Contents
  Fallback : DejaVu Sans provides the rupee glyph missing from the serif fonts

A two-pass build is used: pass 1 records the start page of every chapter, and
pass 2 renders the Table of Contents with those page numbers.  The page map is
also written to chapter_pages.json so the .docx TOC can reuse it.
"""

import os
import re
import json
from fpdf import FPDF
from fpdf.enums import XPos, YPos, MethodReturnValue

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, "Business_Plan_Report.md")
OUT = os.path.join(BASE, "BuildWise_Business_Plan_Report.pdf")

NAVY = (22, 58, 107)
GREY = (89, 89, 89)
BLACK = (33, 33, 33)
WHITE = (255, 255, 255)
ROW_ALT = (238, 242, 248)
RULE = (187, 187, 187)

F = "/usr/share/fonts"
CAL = f"{F}/caladea"
LIB = f"{F}/liberation-serif"
DVM = f"{F}/dejavu-sans-mono-fonts/DejaVuSansMono.ttf"
DVDIR = f"{F}/dejavu-sans-fonts"

FRONT_MATTER = {"DECLARATION", "ACKNOWLEDGEMENT", "TABLE OF CONTENTS"}

# ---- runtime state (reset each build pass) ----
pdf = None
EPW = 0.0
FIG = {"n": 0}
CAPTURED = []          # chapter start pages recorded during a pass
TOC_PAGES = None       # page map used to fill the TOC (None on pass 1)


class PDF(FPDF):
    def header(self):
        if self.page_no() == 1:
            return
        self.set_y(9)
        self.set_font("Body", "", 9.5)
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
        self.set_y(-13)
        self.set_font("Body", "", 9.5)
        self.set_text_color(*GREY)
        self.cell(0, 6, f"Page {self.page_no() - 1}", align="C")


def strip_md(t):
    return t.replace("**", "").replace("*", "")


def _md_to_plain_marked(text):
    text = re.sub(r"\*\*(.+?)\*\*", r"@@B@@\1@@/B@@", text)
    text = re.sub(r"\*([^*]+)\*", r"__\1__", text)
    return text.replace("@@B@@", "**").replace("@@/B@@", "**")


def wrapped_lines(text, width, font, style, size, markdown=False):
    pdf.set_font(font, style, size)
    out = pdf.multi_cell(width, 5, text, dry_run=True,
                         output=MethodReturnValue.LINES, markdown=markdown,
                         new_x=XPos.RIGHT, new_y=YPos.TOP)
    return max(len(out), 1)


def write_rich(text, size=12, color=BLACK, lh=6.4, align="J"):
    pdf.set_x(pdf.l_margin)
    pdf.set_text_color(*color)
    pdf.set_font("Body", "", size)
    pdf.multi_cell(EPW, lh, _md_to_plain_marked(text), align=align,
                   new_x=XPos.LMARGIN, new_y=YPos.NEXT, markdown=True)


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
    line_h = 5.4
    pad = 1.8
    pdf.ln(1)
    alt = {"n": 0}

    def draw_row(cells, is_header=False):
        size = 11 if is_header else 11
        font = "Head" if is_header else "Body"
        style = "B" if is_header else ""
        nlines = max(wrapped_lines(cells[k], widths[k] - 2 * pad, font, style, size)
                     for k in range(ncol))
        h = nlines * line_h + 2 * pad
        if pdf.get_y() + h > pdf.page_break_trigger:
            pdf.add_page()
        x0 = pdf.l_margin
        y0 = pdf.get_y()
        x = x0
        for k, c in enumerate(cells):
            if is_header:
                pdf.set_fill_color(*NAVY)
                pdf.set_text_color(*WHITE)
            else:
                pdf.set_fill_color(*(ROW_ALT if alt["n"] % 2 else WHITE))
                pdf.set_text_color(*BLACK)
            pdf.set_draw_color(*RULE)
            pdf.set_line_width(0.2)
            pdf.rect(x, y0, widths[k], h, style="DF")
            pdf.set_xy(x + pad, y0 + pad)
            pdf.set_font(font, style, size)
            pdf.multi_cell(widths[k] - 2 * pad, line_h, c, align="L",
                           new_x=XPos.RIGHT, new_y=YPos.TOP)
            x += widths[k]
        pdf.set_xy(x0, y0 + h)
        if not is_header:
            alt["n"] += 1

    draw_row(header, is_header=True)
    for cells in body:
        draw_row(cells)
    pdf.ln(3)
    pdf.set_text_color(*BLACK)


def render_toc(items):
    """Bordered Table of Contents: S. No | Contents | Page No."""
    sno_w, page_w = 20.0, 24.0
    cont_w = EPW - sno_w - page_w
    widths = [sno_w, cont_w, page_w]
    aligns = ["C", "L", "C"]
    line_h = 6.2
    pad = 2.0
    headers = ["S. No", "Contents", "Page No"]

    def draw(cells, is_header=False):
        h = line_h + 2 * pad
        x0 = pdf.l_margin
        y0 = pdf.get_y()
        x = x0
        for k, c in enumerate(cells):
            if is_header:
                pdf.set_fill_color(*NAVY)
                pdf.set_text_color(*WHITE)
                pdf.set_font("Head", "B", 12)
            else:
                pdf.set_fill_color(*(ROW_ALT if draw.n % 2 else WHITE))
                pdf.set_text_color(*BLACK)
                pdf.set_font("Body", "", 12)
            pdf.set_draw_color(*RULE)
            pdf.set_line_width(0.2)
            pdf.rect(x, y0, widths[k], h, style="DF")
            pdf.set_xy(x + pad, y0 + pad)
            pdf.multi_cell(widths[k] - 2 * pad, line_h, c, align=aligns[k],
                           new_x=XPos.RIGHT, new_y=YPos.TOP)
            x += widths[k]
        pdf.set_xy(x0, y0 + h)
        if not is_header:
            draw.n += 1
    draw.n = 0

    pdf.ln(2)
    draw(headers, is_header=True)
    for idx, title in enumerate(items, start=1):
        page = ""
        if TOC_PAGES and idx - 1 < len(TOC_PAGES) and TOC_PAGES[idx - 1]:
            page = str(TOC_PAGES[idx - 1])
        draw([str(idx), title, page])
    pdf.set_text_color(*BLACK)


def render_code(codelines):
    while codelines and not codelines[0].strip():
        codelines.pop(0)
    while codelines and not codelines[-1].strip():
        codelines.pop()
    line_h = 4.9
    block_h = len(codelines) * line_h + 4
    if pdf.get_y() + block_h > pdf.page_break_trigger:
        pdf.add_page()
    pdf.ln(1)
    pdf.set_font("Mono", "", 9.5)
    pdf.set_text_color(*NAVY)
    pdf.set_fill_color(245, 247, 250)
    for ln in codelines:
        pdf.set_x(pdf.l_margin)
        pdf.cell(EPW, line_h, ln, new_x=XPos.LMARGIN, new_y=YPos.NEXT, fill=True, align="C")
    pdf.ln(3)
    pdf.set_text_color(*BLACK)


def render_image(path, caption=None, chapter_end=False):
    from PIL import Image
    iw, ih = Image.open(path).size
    max_w, max_h = EPW, 185.0
    disp_w = max_w
    disp_h = disp_w * ih / iw
    if disp_h > max_h:
        disp_h = max_h
        disp_w = disp_h * iw / ih
    # Measure the caption so the image + caption are never split across pages.
    cap_desc = None
    cap_h = 0
    if caption:
        mm = re.match(r"^Figure\s*\d*\s*:\s*(.*)$", caption)
        cap_desc = mm.group(1) if mm else caption
        nlines = wrapped_lines(f"Figure 0: {cap_desc}", EPW, "Body", "I", 11)
        cap_h = nlines * 5.4 + 3
    block = 3 + disp_h + 2 + cap_h
    if pdf.get_y() + block > pdf.page_break_trigger:
        pdf.add_page()
        # A chapter-ending figure that lands on its own page is centred
        # vertically so the page looks balanced rather than top-heavy.
        if chapter_end:
            avail = pdf.page_break_trigger - pdf.get_y()
            pdf.ln(max(0, (avail - block) / 2 - 5))
    x = pdf.l_margin + (EPW - disp_w) / 2
    pdf.ln(3)
    pdf.image(path, x=x, w=disp_w)
    pdf.ln(2)
    if cap_desc is not None:
        FIG["n"] += 1
        pdf.set_font("Body", "I", 11)
        pdf.set_text_color(*GREY)
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(EPW, 5.4, f"Figure {FIG['n']}: {cap_desc}", align="C",
                       new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(3)
    pdf.set_text_color(*BLACK)


def render_callout(title, body):
    """A shaded highlight box with a navy left accent bar."""
    pad = 4.0
    bar = 3.0
    inner_w = EPW - bar - 2 * pad
    tlines = wrapped_lines(title, inner_w, "Head", "B", 12) if title else 0
    blines = wrapped_lines(_md_to_plain_marked(body), inner_w, "Body", "", 11.5, markdown=True)
    th = tlines * 6.4
    bh = blines * 6.0
    h = pad + th + (2 if title else 0) + bh + pad
    if pdf.get_y() + h + 6 > pdf.page_break_trigger:
        pdf.add_page()
    pdf.ln(2)
    y0 = pdf.get_y()
    pdf.set_fill_color(*ROW_ALT)
    pdf.rect(pdf.l_margin, y0, EPW, h, style="F")
    pdf.set_fill_color(*NAVY)
    pdf.rect(pdf.l_margin, y0, bar, h, style="F")
    tx = pdf.l_margin + bar + pad
    cy = y0 + pad
    if title:
        pdf.set_xy(tx, cy)
        pdf.set_font("Head", "B", 12)
        pdf.set_text_color(*NAVY)
        pdf.multi_cell(inner_w, 6.4, title, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        cy = pdf.get_y() + 2
    pdf.set_xy(tx, cy)
    pdf.set_font("Body", "", 11.5)
    pdf.set_text_color(*BLACK)
    pdf.multi_cell(inner_w, 6.0, _md_to_plain_marked(body), markdown=True,
                   new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_y(y0 + h)
    pdf.ln(4)
    pdf.set_text_color(*BLACK)


def render_cards(cards):
    """A row of navy KPI / statistic cards (big value + small label)."""
    n = len(cards)
    gap = 3.5
    cw = (EPW - gap * (n - 1)) / n
    ch = 22.0
    if pdf.get_y() + ch + 8 > pdf.page_break_trigger:
        pdf.add_page()
    pdf.ln(2)
    y0 = pdf.get_y()
    x = pdf.l_margin
    for val, lab in cards:
        pdf.set_fill_color(*NAVY)
        pdf.rect(x, y0, cw, ch, style="F")
        pdf.set_xy(x, y0 + 4.5)
        pdf.set_font("Head", "B", 16)
        pdf.set_text_color(*WHITE)
        pdf.multi_cell(cw, 8, val, align="C", new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.set_xy(x, y0 + ch - 7.5)
        pdf.set_font("Body", "", 9.5)
        pdf.set_text_color(212, 222, 238)
        pdf.multi_cell(cw, 4.5, lab, align="C", new_x=XPos.RIGHT, new_y=YPos.TOP)
        x += cw + gap
    pdf.set_y(y0 + ch)
    pdf.ln(5)
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


def cover_divider(sb=4, sa=6):
    pdf.ln(sb)
    pdf.set_draw_color(*NAVY)
    pdf.set_line_width(0.5)
    pdf.line(pdf.l_margin, pdf.get_y(), pdf.w - pdf.r_margin, pdf.get_y())
    pdf.ln(sa)


def build_cover():
    pdf.add_page()
    pdf.set_auto_page_break(False)
    pdf.ln(10)
    cover_center("BUILDWISE CONSTRUCTIONS PVT. LTD.", "Head", "B", 26, NAVY, sa=3)
    cover_center('"Building Trust Through Technology and Quality Construction"',
                 "Head", "I", 14, GREY, sa=7)
    cover_center("BUSINESS PLAN REPORT", "Head", "B", 19, NAVY, sa=2)
    cover_divider(sb=3, sa=8)
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
    for name, reg in [("THILAK KUMAR K", "RA2311042040014"),
                      ("ARJUN S", "RA2311042040018"),
                      ("SANJAY KUMAR A M", "RA2311042040024")]:
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
    pdf.set_auto_page_break(True, margin=16)


# ==================== MAIN BUILD ====================
def build(toc_pages):
    """Render the whole document once. Returns the list of chapter start pages."""
    global pdf, EPW, TOC_PAGES, CAPTURED
    FIG["n"] = 0
    CAPTURED = []
    TOC_PAGES = toc_pages

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
    pdf.add_font("DejaVu", "", f"{DVDIR}/DejaVuSans.ttf")
    pdf.add_font("DejaVu", "B", f"{DVDIR}/DejaVuSans-Bold.ttf")
    pdf.add_font("DejaVu", "I", f"{DVDIR}/DejaVuSans-Oblique.ttf")
    pdf.add_font("DejaVu", "BI", f"{DVDIR}/DejaVuSans-BoldOblique.ttf")
    pdf.set_fallback_fonts(["DejaVu"], exact_match=False)
    EPW = pdf.w - pdf.l_margin - pdf.r_margin

    build_cover()

    with open(SRC, encoding="utf-8") as f:
        lines = f.read().split("\n")

    i = 0
    while i < len(lines):
        stripped = lines[i].strip()

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
            # Is this figure the last element of its chapter?
            k = i + 1
            while k < len(lines) and (lines[k].strip() == "" or lines[k].strip() == "---"):
                k += 1
            chapter_end = (k >= len(lines)) or lines[k].strip().startswith("# ")
            if os.path.exists(img_path):
                render_image(img_path, caption, chapter_end=chapter_end)
            i += 1
            continue

        if stripped.startswith(":::callout"):
            title = stripped[len(":::callout"):].strip()
            body_lines = []
            i += 1
            while i < len(lines) and lines[i].strip() != ":::":
                if lines[i].strip():
                    body_lines.append(lines[i].strip())
                i += 1
            render_callout(title, " ".join(body_lines))
            i += 1
            continue

        if stripped.startswith(":::cards"):
            cards = []
            i += 1
            while i < len(lines) and lines[i].strip() != ":::":
                s = lines[i].strip()
                if "::" in s:
                    v, l = s.split("::", 1)
                    cards.append((v.strip(), l.strip()))
                i += 1
            if cards:
                render_cards(cards)
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

            if level == 2 and text.upper() == "TABLE OF CONTENTS":
                pdf.add_page()
                pdf.ln(2)
                pdf.set_font("Head", "B", 16)
                pdf.set_text_color(*NAVY)
                pdf.set_x(pdf.l_margin)
                pdf.multi_cell(EPW, 9, "TABLE OF CONTENTS", align="C",
                               new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                pdf.ln(3)
                pdf.set_text_color(*BLACK)
                j = i + 1
                items = []
                while j < len(lines):
                    s = lines[j].strip()
                    if s == "" or s == "---":
                        j += 1
                        continue
                    mm = re.match(r"^\d+\.\s+(.*)$", s)
                    if mm:
                        items.append(mm.group(1).strip())
                        j += 1
                        continue
                    break
                render_toc(items)
                i = j
                continue

            if level == 1:
                pdf.add_page()
                CAPTURED.append(pdf.page_no() - 1)   # footer page number
                size = heading_fit_size(text, 18, 13)
                pdf.set_font("Head", "B", size)
                pdf.set_text_color(*NAVY)
                pdf.set_x(pdf.l_margin)
                pdf.cell(0, 11, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                pdf.set_draw_color(*NAVY)
                pdf.set_line_width(0.5)
                pdf.line(pdf.l_margin, pdf.get_y() + 0.5, pdf.w - pdf.r_margin, pdf.get_y() + 0.5)
                pdf.ln(5)
                pdf.set_text_color(*BLACK)
            elif level == 2 and text.upper() in FRONT_MATTER:
                if text.upper() == "ACKNOWLEDGEMENT":
                    pdf.ln(34)
                else:
                    pdf.add_page()
                    pdf.ln(52)
                pdf.set_font("Head", "B", 16)
                pdf.set_text_color(*NAVY)
                pdf.set_x(pdf.l_margin)
                pdf.multi_cell(EPW, 9, text.upper(), align="C",
                               new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                pdf.ln(4)
                pdf.set_text_color(*BLACK)
            else:
                sz = {2: 15, 3: 13, 4: 12}.get(level, 12)
                ensure_space(24)
                pdf.ln(2 if level == 2 else 1)
                size = heading_fit_size(text, sz, 11)
                pdf.set_font("Head", "B", size)
                pdf.set_text_color(*NAVY)
                pdf.set_x(pdf.l_margin)
                pdf.multi_cell(EPW, size * 0.52, text, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                pdf.ln(1.5)
                pdf.set_text_color(*BLACK)
            i += 1
            continue

        if stripped.startswith(">"):
            text = strip_md(stripped.lstrip(">").strip())
            if text:
                ensure_space(18)
                pdf.set_font("Body", "I", 12)
                nlines = wrapped_lines(text, EPW - 10, "Body", "I", 12)
                h = nlines * 6.0 + 5
                y0 = pdf.get_y()
                pdf.set_fill_color(*ROW_ALT)
                pdf.rect(pdf.l_margin, y0, EPW, h, style="F")
                pdf.set_xy(pdf.l_margin + 5, y0 + 2.5)
                pdf.set_text_color(*NAVY)
                pdf.multi_cell(EPW - 10, 6.0, text, align="C",
                               new_x=XPos.LMARGIN, new_y=YPos.NEXT)
                pdf.set_y(y0 + h)
                pdf.ln(3)
                pdf.set_text_color(*BLACK)
            i += 1
            continue

        if stripped.startswith("- "):
            text = _md_to_plain_marked(stripped[2:])
            bullet_w = 6
            nlines = wrapped_lines(text, EPW - 2 - bullet_w, "Body", "", 12, markdown=True)
            h = nlines * 6.2
            if pdf.get_y() + h > pdf.page_break_trigger:
                pdf.add_page()
            y0 = pdf.get_y()
            pdf.set_font("Body", "", 12)
            pdf.set_text_color(*BLACK)
            pdf.set_xy(pdf.l_margin + 3, y0)
            pdf.cell(bullet_w, 6.2, "\u2022")
            pdf.set_xy(pdf.l_margin + 3 + bullet_w, y0)
            pdf.multi_cell(EPW - 3 - bullet_w, 6.2, text,
                           align="L", new_x=XPos.LMARGIN, new_y=YPos.NEXT, markdown=True)
            pdf.set_y(max(pdf.get_y(), y0 + h))
            pdf.ln(0.6)
            i += 1
            continue

        om = re.match(r"^(\d+)\.\s+(.*)$", stripped)
        if om:
            txt = strip_md(om.group(2))
            nlines = wrapped_lines(txt, EPW - 10, "Body", "", 12)
            h = nlines * 6.2
            if pdf.get_y() + h > pdf.page_break_trigger:
                pdf.add_page()
            y0 = pdf.get_y()
            pdf.set_font("Body", "", 12)
            pdf.set_text_color(*BLACK)
            pdf.set_xy(pdf.l_margin + 2, y0)
            pdf.cell(9, 6.2, f"{om.group(1)}.")
            pdf.set_xy(pdf.l_margin + 11, y0)
            pdf.multi_cell(EPW - 11, 6.2, txt, align="L",
                           new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.set_y(max(pdf.get_y(), y0 + h))
            pdf.ln(0.6)
            i += 1
            continue

        if stripped == "":
            i += 1
            continue

        write_rich(stripped, size=12, color=BLACK, lh=6.4, align="J")
        pdf.ln(1.8)
        i += 1

    pdf.output(OUT)
    return list(CAPTURED)


if __name__ == "__main__":
    pages = build(None)                     # pass 1: record chapter pages
    build(pages)                            # pass 2: render TOC with page numbers
    json.dump(pages, open(os.path.join(BASE, "chapter_pages.json"), "w"))
    print("Saved:", OUT)
    print("Chapter pages:", pages)
