#!/usr/bin/env python3
"""Render the BuildWise Business Plan (report_content.BLOCKS) to a polished,
precisely-paginated PDF using reportlab.

DejaVu Serif is embedded (it approximates Times New Roman and, unlike the PDF
core Times font, carries the Indian Rupee glyph).  Output overwrites the
existing ``BuildWise_Business_Plan_Report.pdf``.
"""

import os
import re
import matplotlib
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, mm
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle,
    Image, PageBreak, KeepTogether, HRFlowable, Flowable, CondPageBreak,
)
from reportlab.lib.utils import ImageReader

import report_content as RC

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "BuildWise_Business_Plan_Report.pdf")

# ---------------------------------------------------------------------------
# Colours
# ---------------------------------------------------------------------------
NAVY = colors.HexColor("#163A70")
NAVY_DK = colors.HexColor("#0E2A52")
STEEL = colors.HexColor("#4E77B0")
GREY = colors.HexColor("#54606E")
LGREY = colors.HexColor("#8A94A0")
ROW_ALT = colors.HexColor("#EEF3FA")
CARD_BG = colors.HexColor("#F2F5FA")
RULE = colors.HexColor("#BFC7D2")
WHITE = colors.white

# ---------------------------------------------------------------------------
# Fonts
# ---------------------------------------------------------------------------
FDIR = os.path.join(os.path.dirname(matplotlib.__file__), "mpl-data", "fonts", "ttf")
pdfmetrics.registerFont(TTFont("Serif", os.path.join(FDIR, "DejaVuSerif.ttf")))
pdfmetrics.registerFont(TTFont("Serif-B", os.path.join(FDIR, "DejaVuSerif-Bold.ttf")))
pdfmetrics.registerFont(TTFont("Serif-I", os.path.join(FDIR, "DejaVuSerif-Italic.ttf")))
pdfmetrics.registerFont(TTFont("Serif-BI", os.path.join(FDIR, "DejaVuSerif-BoldItalic.ttf")))
pdfmetrics.registerFontFamily("Serif", normal="Serif", bold="Serif-B",
                              italic="Serif-I", boldItalic="Serif-BI")

# ---------------------------------------------------------------------------
# Geometry
# ---------------------------------------------------------------------------
PAGE_W, PAGE_H = A4
MARGIN = inch
CW = PAGE_W - 2 * MARGIN            # content width ~451pt

# ---------------------------------------------------------------------------
# Paragraph styles
# ---------------------------------------------------------------------------
S_BODY = ParagraphStyle("body", fontName="Serif", fontSize=10, leading=12.7,
                        alignment=TA_JUSTIFY, textColor=colors.black,
                        spaceAfter=2.5, spaceBefore=1)
S_BODY_L = ParagraphStyle("bodyL", parent=S_BODY, alignment=TA_LEFT)
S_H2 = ParagraphStyle("h2", fontName="Serif-B", fontSize=13, leading=15,
                      textColor=NAVY, spaceBefore=5, spaceAfter=2)
S_H3 = ParagraphStyle("h3", fontName="Serif-B", fontSize=11, leading=13,
                      textColor=NAVY, spaceBefore=4, spaceAfter=2)
S_CHLABEL = ParagraphStyle("chlabel", fontName="Serif-B", fontSize=12, leading=14,
                           textColor=STEEL, alignment=TA_LEFT, spaceAfter=1)
S_CHTITLE = ParagraphStyle("chtitle", fontName="Serif-B", fontSize=18, leading=21,
                           textColor=NAVY, alignment=TA_LEFT, spaceAfter=2)
S_FMHEAD = ParagraphStyle("fmhead", fontName="Serif-B", fontSize=18, leading=22,
                          textColor=NAVY, alignment=TA_CENTER, spaceBefore=4,
                          spaceAfter=6)
S_CAP = ParagraphStyle("cap", fontName="Serif-I", fontSize=9, leading=11,
                       textColor=GREY, alignment=TA_CENTER, spaceBefore=2,
                       spaceAfter=5)
S_NOTE = ParagraphStyle("note", fontName="Serif-I", fontSize=10, leading=13,
                        textColor=GREY, alignment=TA_CENTER, spaceBefore=6)
S_TH = ParagraphStyle("th", fontName="Serif-B", fontSize=9.2, leading=11.2,
                      textColor=WHITE)
S_TD = ParagraphStyle("td", fontName="Serif", fontSize=9, leading=11.2,
                      textColor=colors.black)
S_BULLET = ParagraphStyle("bul", fontName="Serif", fontSize=10, leading=13,
                          leftIndent=14, bulletIndent=2, spaceAfter=1,
                          textColor=colors.black)
S_KPI_BIG = ParagraphStyle("kpibig", fontName="Serif-B", fontSize=13, leading=15.5,
                           textColor=WHITE, alignment=TA_CENTER)
S_KPI_SM = ParagraphStyle("kpism", fontName="Serif", fontSize=8.6, leading=10.5,
                          textColor=colors.HexColor("#D6E1F0"), alignment=TA_CENTER)
S_CARD_T = ParagraphStyle("cardt", fontName="Serif-B", fontSize=9.6, leading=11.5,
                          textColor=WHITE, alignment=TA_CENTER)
S_CARD_B = ParagraphStyle("cardb", fontName="Serif", fontSize=8.7, leading=11,
                          textColor=colors.HexColor("#33414F"), alignment=TA_LEFT)
S_CARD_BL = ParagraphStyle("cardbl", parent=S_CARD_B, leftIndent=8, bulletIndent=1)
S_CO_T = ParagraphStyle("cot", fontName="Serif-BI", fontSize=10.5, leading=13,
                        textColor=NAVY, spaceAfter=2)
S_CO_B = ParagraphStyle("cob", fontName="Serif", fontSize=9.5, leading=12.4,
                        textColor=colors.HexColor("#2A2A2A"), alignment=TA_JUSTIFY)


def md(text):
    """Convert **bold** to reportlab <b> markup and escape stray ampersands."""
    text = text.replace("&", "&amp;")
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    return text


# ---------------------------------------------------------------------------
# Flowable builders
# ---------------------------------------------------------------------------
_figcount = [0]


class RoundBox(Flowable):
    """A rounded rectangle background wrapper drawn behind a table of content.
    Used for KPI/card grids to fake rounded corners."""
    def __init__(self, inner, radius=6, fill=NAVY, pad=0):
        self.inner = inner
        self.radius = radius
        self.fill = fill
        Flowable.__init__(self)

    def wrap(self, aw, ah):
        w, h = self.inner.wrap(aw, ah)
        self.w, self.h = w, h
        return w, h

    def draw(self):
        self.canv.saveState()
        self.canv.setFillColor(self.fill)
        self.canv.roundRect(0, 0, self.w, self.h, self.radius, fill=1, stroke=0)
        self.canv.restoreState()
        self.inner.drawOn(self.canv, 0, 0)


def make_table(header, rows, widths):
    if widths is None:
        widths = [1.0 / len(header)] * len(header)
    col_w = [w * CW for w in widths]
    data = [[Paragraph(md(str(c)), S_TH) for c in header]]
    for r in rows:
        data.append([Paragraph(md(str(c)), S_TD) for c in r])
    t = Table(data, colWidths=col_w, repeatRows=1)
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 2.2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.2),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("LINEBELOW", (0, 0), (-1, -1), 0.4, RULE),
        ("LINEAFTER", (0, 0), (-2, -1), 0.4, RULE),
        ("BOX", (0, 0), (-1, -1), 0.6, RULE),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style.append(("BACKGROUND", (0, i), (-1, i), ROW_ALT))
    t.setStyle(TableStyle(style))
    return t


def make_kpis(cardlist):
    n = len(cardlist)
    gap = 8
    cw = (CW - (n - 1) * gap) / n
    cells = []
    for big, small in cardlist:
        inner = Table([[Paragraph(md(big), S_KPI_BIG)],
                       [Paragraph(md(small), S_KPI_SM)]], colWidths=[cw])
        inner.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), NAVY),
            ("TOPPADDING", (0, 0), (-1, 0), 9),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 1),
            ("TOPPADDING", (0, 1), (-1, 1), 1),
            ("BOTTOMPADDING", (0, 1), (-1, 1), 9),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ]))
        cells.append(RoundBox(inner, radius=7, fill=NAVY))
    row = [cells[i // 2] if i % 2 == 0 else Spacer(gap, 1) for i in range(2 * n - 1)]
    widths = []
    for i in range(2 * n - 1):
        widths.append(cw if i % 2 == 0 else gap)
    outer = Table([row], colWidths=widths)
    outer.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                               ("LEFTPADDING", (0, 0), (-1, -1), 0),
                               ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                               ("TOPPADDING", (0, 0), (-1, -1), 0),
                               ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    return outer


def _card_inner(title, body, cw):
    if isinstance(body, list):
        body_flow = [Paragraph(f"\u2022 {md(x)}", S_CARD_BL) for x in body]
        body_cell = body_flow
    else:
        body_cell = Paragraph(md(body), S_CARD_B)
    inner = Table([[Paragraph(md(title), S_CARD_T)], [body_cell]], colWidths=[cw])
    inner.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("BACKGROUND", (0, 1), (-1, 1), CARD_BG),
        ("TOPPADDING", (0, 0), (-1, 0), 4),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 4),
        ("TOPPADDING", (0, 1), (-1, 1), 5),
        ("BOTTOMPADDING", (0, 1), (-1, 1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("BOX", (0, 0), (-1, -1), 0.5, RULE),
        ("VALIGN", (0, 1), (-1, 1), "TOP"),
    ]))
    return inner


def make_cards(items, cols):
    gap = 8
    cw = (CW - (cols - 1) * gap) / cols
    rows = []
    i = 0
    while i < len(items):
        chunk = items[i:i + cols]
        row_cells = []
        widths = []
        for j in range(cols):
            if j > 0:
                row_cells.append(Spacer(gap, 1))
                widths.append(gap)
            if j < len(chunk):
                title, body = chunk[j]
                row_cells.append(_card_inner(title, body, cw))
            else:
                row_cells.append(Spacer(cw, 1))
            widths.append(cw)
        rows.append((row_cells, widths))
        i += cols
    flow = []
    for idx, (cells, widths) in enumerate(rows):
        t = Table([cells], colWidths=widths)
        t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                               ("LEFTPADDING", (0, 0), (-1, -1), 0),
                               ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                               ("TOPPADDING", (0, 0), (-1, -1), 0),
                               ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
        flow.append(t)
    return flow


def make_callout(title, text):
    inner = Table([[Paragraph(md(title), S_CO_T)], [Paragraph(md(text), S_CO_B)]],
                  colWidths=[CW - 16])
    inner.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#EEF1F6")),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, 0), 4),
        ("BOTTOMPADDING", (0, -1), (-1, -1), 4),
        ("TOPPADDING", (0, 1), (-1, 1), 0),
        ("LINEBEFORE", (0, 0), (0, -1), 3.2, NAVY),
    ]))
    return inner


def make_figure(src, caption, w):
    path = os.path.join(BASE, src)
    iw, ih = ImageReader(path).getSize()
    disp_w = w * CW
    disp_h = disp_w * ih / iw
    # cap height so a single figure never blows past the frame
    max_h = 2.5 * inch
    if disp_h > max_h:
        disp_h = max_h
        disp_w = disp_h * iw / ih
    img = Image(path, width=disp_w, height=disp_h)
    img.hAlign = "CENTER"
    _figcount[0] += 1
    cap = Paragraph(f"Figure {_figcount[0]}. {md(caption)}", S_CAP)
    return KeepTogether([img, cap])


def bullet_flow(items, title, check):
    flow = []
    if title:
        flow.append(Paragraph(f"<b>{md(title)}</b>", S_H3))
    mark = "\u2714" if check else "\u2022"
    for it in items:
        flow.append(Paragraph(f'<font color="#163A70">{mark}</font>&nbsp;&nbsp;{md(it)}',
                              S_BULLET))
    return flow


# ---------------------------------------------------------------------------
# Cover page
# ---------------------------------------------------------------------------
def cover_flowables():
    C = ParagraphStyle
    company = C("company", fontName="Serif-B", fontSize=24, leading=29,
                textColor=NAVY, alignment=TA_CENTER)
    tag = C("tag", fontName="Serif-I", fontSize=14, leading=18,
            textColor=GREY, alignment=TA_CENTER)
    subttl = C("subttl", fontName="Serif-B", fontSize=20, leading=24,
               textColor=NAVY, alignment=TA_CENTER)
    prep = C("prep", fontName="Serif-B", fontSize=15, leading=19, textColor=NAVY,
             alignment=TA_CENTER, spaceBefore=4)
    nm = C("nm", fontName="Serif-B", fontSize=15, leading=18, textColor=colors.black,
           alignment=TA_CENTER)
    reg = C("reg", fontName="Serif", fontSize=12, leading=15, textColor=GREY,
            alignment=TA_CENTER)
    inst = C("inst", fontName="Serif", fontSize=13, leading=16, textColor=colors.black,
             alignment=TA_CENTER)
    inst_b = C("instb", fontName="Serif-B", fontSize=13, leading=16, textColor=NAVY,
               alignment=TA_CENTER)
    lblcol = colors.black

    def navline(frac=0.8, sb=6, sa=6):
        return [Spacer(1, sb),
                HRFlowable(width=f"{int(frac*100)}%", thickness=1.4, color=NAVY,
                           spaceBefore=0, spaceAfter=0, hAlign="CENTER"),
                Spacer(1, sa)]

    F = []
    F.append(Spacer(1, 26))
    F.append(Paragraph("BUILDWISE CONSTRUCTIONS PVT. LTD.", company))
    F.append(Spacer(1, 10))
    F.append(Paragraph('"Building Trust Through Technology and Quality Construction"', tag))
    F.append(Spacer(1, 25))            # ~0.35"
    F.append(Paragraph("BUSINESS PLAN REPORT", subttl))
    F += navline(0.8, sb=8, sa=12)

    # business information table (centred, borderless, aligned columns)
    info = [("Industry", "Construction"),
            ("Business Model", "Technology-Enabled Construction Startup"),
            ("Headquarters", "Chennai, Tamil Nadu"),
            ("Initial Capital", "\u20b91.00 Crore"),
            ("Academic Year", "2026\u20132027")]
    lbl = C("lbl", fontName="Serif-B", fontSize=13, leading=18, textColor=lblcol,
            alignment=TA_LEFT)
    val = C("val", fontName="Serif", fontSize=13, leading=18, textColor=colors.black,
            alignment=TA_LEFT)
    data = [[Paragraph(k, lbl), Paragraph(": " + v, val)] for k, v in info]
    itab = Table(data, colWidths=[1.7 * inch, 3.6 * inch], hAlign="CENTER")
    itab.setStyle(TableStyle([("TOPPADDING", (0, 0), (-1, -1), 2),
                             ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                             ("LEFTPADDING", (0, 0), (-1, -1), 0),
                             ("RIGHTPADDING", (0, 0), (-1, -1), 0)]))
    F.append(itab)
    F += navline(0.8, sb=12, sa=10)

    F.append(Paragraph("PREPARED BY", prep))
    F.append(Spacer(1, 12))            # ~0.18"
    for name, rno in [("THILAK KUMAR K", "RA2311042040014"),
                      ("ARJUN S", "RA2311042040018"),
                      ("SANJAY KUMAR A M", "RA2311042040024")]:
        F.append(Paragraph(name, nm))
        F.append(Paragraph(rno, reg))
        F.append(Spacer(1, 12))
    F.append(Spacer(1, 20))            # ~0.45"
    F.append(Paragraph("Entrepreneurship and Family Business Management", inst_b))
    F.append(Spacer(1, 6))
    F.append(Paragraph("Department of Computer Science and Engineering "
                       "(Emerging Technologies)", inst))
    F.append(Paragraph("&amp; Computer Science and Business Systems (Final Year)", inst))
    F.append(Spacer(1, 8))
    F.append(Paragraph("SRM Institute of Science and Technology", inst_b))
    F.append(Paragraph("Vadapalani Campus, Chennai", inst))
    return F


# ---------------------------------------------------------------------------
# Build the flowable stream from the shared content model
# ---------------------------------------------------------------------------
def build_story():
    story = []
    for blk in RC.BLOCKS:
        t = blk["t"]
        if t == "cover":
            story += cover_flowables()
        elif t == "pagebreak":
            story.append(PageBreak())
        elif t == "chapter":
            story.append(PageBreak())
            story.append(Paragraph(blk["label"], S_CHLABEL))
            story.append(Paragraph(blk["title"], S_CHTITLE))
            story.append(HRFlowable(width="100%", thickness=1.6, color=NAVY,
                                    spaceBefore=2, spaceAfter=8))
        elif t == "fmhead":
            story.append(Paragraph(blk["text"], S_FMHEAD))
            if blk.get("rule"):
                story.append(HRFlowable(width="80%", thickness=1.4, color=NAVY,
                                        spaceBefore=2, spaceAfter=10, hAlign="CENTER"))
            else:
                story.append(Spacer(1, 4))
        elif t == "h":
            story.append(Paragraph(blk["text"], S_H2 if blk["lvl"] == 2 else S_H3))
        elif t == "p":
            story.append(Paragraph(md(blk["text"]), S_BODY))
        elif t == "bullets":
            story += bullet_flow(blk["items"], blk.get("title"), blk.get("check", True))
        elif t == "table":
            story.append(Spacer(1, 1))
            story.append(make_table(blk["header"], blk["rows"], blk["widths"]))
            story.append(Spacer(1, 3))
        elif t == "kpis":
            story.append(Spacer(1, 2))
            story.append(make_kpis(blk["cards"]))
            story.append(Spacer(1, 4))
        elif t == "cards":
            story.append(Spacer(1, 1))
            story += make_cards(blk["items"], blk["cols"])
            story.append(Spacer(1, 2))
        elif t == "callout":
            story.append(Spacer(1, 2))
            story.append(make_callout(blk["title"], blk["text"]))
            story.append(Spacer(1, 3))
        elif t == "figure":
            story.append(Spacer(1, 1))
            story.append(make_figure(blk["src"], blk["caption"], blk["w"]))
        elif t == "note":
            story.append(Spacer(1, 10))
            story.append(Paragraph(md(blk["text"]), S_NOTE))
        elif t == "hr":
            story.append(Spacer(1, 6))
            story.append(HRFlowable(width="100%", thickness=0.8, color=RULE,
                                    spaceBefore=2, spaceAfter=8))
        elif t == "refs":
            for i, item in enumerate(blk["items"], 1):
                story.append(Paragraph(f"{i}.&nbsp;&nbsp;{md(item)}", S_BULLET))
    return story


# ---------------------------------------------------------------------------
# Page furniture (footer with page number, no footer on cover)
# ---------------------------------------------------------------------------
def on_page(canvas, doc):
    pg = canvas.getPageNumber()
    if pg == 1:
        return
    canvas.saveState()
    canvas.setFont("Serif", 9)
    canvas.setFillColor(GREY)
    canvas.drawCentredString(PAGE_W / 2, 0.55 * inch, f"Page {pg - 1}")
    canvas.setStrokeColor(RULE)
    canvas.setLineWidth(0.4)
    canvas.line(MARGIN, PAGE_H - 0.7 * inch, PAGE_W - MARGIN, PAGE_H - 0.7 * inch)
    canvas.setFont("Serif-I", 8.5)
    canvas.setFillColor(LGREY)
    canvas.drawRightString(PAGE_W - MARGIN, PAGE_H - 0.62 * inch,
                           "BuildWise Constructions Pvt. Ltd.")
    canvas.restoreState()


def build():
    doc = BaseDocTemplate(OUT, pagesize=A4, leftMargin=MARGIN, rightMargin=MARGIN,
                          topMargin=MARGIN, bottomMargin=MARGIN, title="BuildWise Business Plan Report")
    frame = Frame(MARGIN, MARGIN, CW, PAGE_H - 2 * MARGIN, id="main",
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([PageTemplate(id="main", frames=[frame], onPage=on_page)])
    _figcount[0] = 0
    doc.build(build_story())
    print("Saved:", OUT, "| figures embedded:", _figcount[0])


if __name__ == "__main__":
    build()
