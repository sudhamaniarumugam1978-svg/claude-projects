#!/usr/bin/env python3
"""Diagnostic: split BLOCKS into intended pages (at cover/chapter/pagebreak
boundaries) and report how many physical pages each consumes."""
import io
import report_content as RC
import render_pdf as R
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, PageBreak
from reportlab.lib.pagesizes import A4
from pypdf import PdfReader


def segments():
    segs, cur, labels = [], [], []
    label = "COVER"
    for b in RC.BLOCKS:
        if b["t"] in ("cover", "pagebreak", "chapter"):
            if cur:
                segs.append((label, cur))
            cur = []
            if b["t"] == "cover":
                label = "P1 COVER"
            elif b["t"] == "chapter":
                label = f"{b['label']} {b['title'][:22]}"
            else:
                label = "cont."
        cur.append(b)
    if cur:
        segs.append((label, cur))
    return segs


def count_pages(blocks):
    R._figcount[0] = 0
    buf = io.BytesIO()
    doc = BaseDocTemplate(buf, pagesize=A4, leftMargin=R.MARGIN, rightMargin=R.MARGIN,
                          topMargin=R.MARGIN, bottomMargin=R.MARGIN)
    frame = Frame(R.MARGIN, R.MARGIN, R.CW, A4[1] - 2 * R.MARGIN, id="m",
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([PageTemplate(id="m", frames=[frame])])
    # temporarily swap BLOCKS
    old = RC.BLOCKS
    story = []
    for blk in blocks:
        if blk["t"] in ("pagebreak", "chapter", "cover"):
            # strip leading break so a single segment = 1 page baseline
            if blk["t"] == "chapter":
                story.append(R.Paragraph(blk["label"], R.S_CHLABEL))
                story.append(R.Paragraph(blk["title"], R.S_CHTITLE))
                from reportlab.platypus import HRFlowable
                story.append(HRFlowable(width="100%", thickness=1.6, color=R.NAVY,
                                        spaceBefore=2, spaceAfter=8))
            elif blk["t"] == "cover":
                story += R.cover_flowables()
            continue
        _render_one(story, blk)
    try:
        doc.build(story)
        return len(PdfReader(buf).pages)
    except Exception as e:
        return f"ERR:{e}"


def _render_one(story, blk):
    from reportlab.platypus import Spacer, PageBreak, HRFlowable
    t = blk["t"]
    if t == "fmhead":
        story.append(R.Paragraph(blk["text"], R.S_FMHEAD))
    elif t == "h":
        story.append(R.Paragraph(blk["text"], R.S_H2 if blk["lvl"] == 2 else R.S_H3))
    elif t == "p":
        story.append(R.Paragraph(R.md(blk["text"]), R.S_BODY))
    elif t == "bullets":
        story += R.bullet_flow(blk["items"], blk.get("title"), blk.get("check", True))
    elif t == "table":
        story.append(R.make_table(blk["header"], blk["rows"], blk["widths"]))
        story.append(Spacer(1, 5))
    elif t == "kpis":
        story.append(R.make_kpis(blk["cards"]))
        story.append(Spacer(1, 6))
    elif t == "cards":
        story += R.make_cards(blk["items"], blk["cols"])
    elif t == "callout":
        story.append(R.make_callout(blk["title"], blk["text"]))
        story.append(Spacer(1, 5))
    elif t == "figure":
        story.append(R.make_figure(blk["src"], blk["caption"], blk["w"]))
    elif t == "note":
        story.append(R.Paragraph(R.md(blk["text"]), R.S_NOTE))
    elif t == "refs":
        for i, item in enumerate(blk["items"], 1):
            story.append(R.Paragraph(f"{i}. {R.md(item)}", R.S_BULLET))


if __name__ == "__main__":
    total = 0
    for label, blocks in segments():
        n = count_pages(blocks)
        total += n if isinstance(n, int) else 0
        flag = "  <-- OVERFLOW" if isinstance(n, int) and n > 1 else ""
        print(f"{n} pg | {label}{flag}")
    print("APPROX TOTAL (independent):", total)
