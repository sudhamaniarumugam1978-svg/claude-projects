#!/usr/bin/env python3
"""Generate all 36 professional navy-themed diagrams for the BuildWise
Business Plan Report.

Every figure is rendered with matplotlib into ``figures/figNN.png`` using a
consistent corporate identity:

    * Serif typography (DejaVu Serif -> approximates Times New Roman and
      carries the Indian Rupee glyph).
    * Dark navy blue (#163A70) primary colour with a graded blue palette.
    * Rounded rectangles, thick connecting arrows, generous white space.
"""

import os
import math
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Wedge, Polygon
from matplotlib.lines import Line2D
import numpy as np

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "figures")
os.makedirs(OUT, exist_ok=True)

# ----------------------------------------------------------------------------
# Palette
# ----------------------------------------------------------------------------
NAVY = "#163A70"
NAVY_DK = "#0E2A52"
NAVY_MD = "#2E5A9E"
STEEL = "#4E77B0"
SKY = "#7FA3D0"
MIST = "#A9C2E2"
PALE = "#DCE7F5"
LIGHT = "#EEF3FA"
GREY = "#54606E"
LGREY = "#8A94A0"
WHITE = "#FFFFFF"
GOLD = "#C9962F"
GREEN = "#3E7D5A"
RED = "#B4472E"

DOUGHNUT_PALETTE = [NAVY, NAVY_MD, STEEL, SKY, MIST, PALE]

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["DejaVu Serif"],
    "font.size": 11,
    "figure.dpi": 200,
    "savefig.dpi": 200,
    "axes.edgecolor": "#C4CCD6",
})


# ----------------------------------------------------------------------------
# Low-level helpers
# ----------------------------------------------------------------------------
def _new(figsize):
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_axis_off()
    ax.set_aspect("equal")
    return fig, ax


def _save(fig, name, pad=0.12):
    path = os.path.join(OUT, name)
    fig.savefig(path, bbox_inches="tight", pad_inches=pad, facecolor="white")
    plt.close(fig)


def rbox(ax, cx, cy, w, h, text, fc=NAVY, ec=None, tc=WHITE, fs=11,
         bold=True, round_size=0.06, lw=1.4, align="center"):
    """Rounded rectangle centred at (cx, cy) with wrapped text."""
    ec = ec or fc
    patch = FancyBboxPatch(
        (cx - w / 2, cy - h / 2), w, h,
        boxstyle=f"round,pad=0.0,rounding_size={round_size}",
        linewidth=lw, edgecolor=ec, facecolor=fc, zorder=3,
        mutation_aspect=1.0,
    )
    ax.add_patch(patch)
    ax.text(cx, cy, text, ha=align, va="center", color=tc, fontsize=fs,
            fontweight="bold" if bold else "normal", zorder=4, wrap=True,
            linespacing=1.25)
    return patch


def arrow(ax, x1, y1, x2, y2, color=NAVY, lw=2.4, style="-|>", ms=16,
          rad=0.0, ls="-"):
    a = FancyArrowPatch(
        (x1, y1), (x2, y2),
        arrowstyle=style, mutation_scale=ms, linewidth=lw,
        color=color, zorder=2, shrinkA=2, shrinkB=2,
        connectionstyle=f"arc3,rad={rad}", linestyle=ls,
    )
    ax.add_patch(a)


def title_text(ax, x, y, text, fs=14, color=NAVY):
    ax.text(x, y, text, ha="center", va="center", fontsize=fs,
            fontweight="bold", color=color)


# ----------------------------------------------------------------------------
# Composite layouts
# ----------------------------------------------------------------------------
def vertical_flow(items, name, box_w=6.4, box_h=1.05, gap=0.62, fs=12,
                  colors=None, tc=WHITE):
    """Single column of rounded boxes joined by downward arrows."""
    n = len(items)
    step = box_h + gap
    total_h = n * box_h + (n - 1) * gap
    fig, ax = _new((box_w + 1.2, total_h + 0.6))
    ax.set_xlim(0, box_w + 1.2)
    ax.set_ylim(0, total_h + 0.6)
    cx = (box_w + 1.2) / 2
    top = total_h + 0.3
    for i, item in enumerate(items):
        cy = top - box_h / 2 - i * step
        fc = (colors[i] if colors else NAVY)
        rbox(ax, cx, cy, box_w, box_h, item, fc=fc, tc=tc, fs=fs)
        if i < n - 1:
            y1 = cy - box_h / 2
            y2 = cy - box_h / 2 - gap
            arrow(ax, cx, y1, cx, y2)
    _save(fig, name)


def snake_flow(items, name, cols=3, box_w=3.5, box_h=1.15, hgap=0.9,
               vgap=1.0, fs=11.5, colors=None):
    """Serpentine (boustrophedon) flow for long processes."""
    n = len(items)
    rows = math.ceil(n / cols)
    W = cols * box_w + (cols - 1) * hgap
    H = rows * box_h + (rows - 1) * vgap
    fig, ax = _new((W + 0.8, H + 0.8))
    ax.set_xlim(0, W + 0.8)
    ax.set_ylim(0, H + 0.8)
    ox = 0.4
    oy = 0.4

    def center(idx):
        r = idx // cols
        c = idx % cols
        if r % 2 == 1:  # reverse direction on odd rows
            c = cols - 1 - c
        cx = ox + c * (box_w + hgap) + box_w / 2
        cy = H + oy - (r * (box_h + vgap) + box_h / 2)
        return cx, cy, r, (idx % cols)

    centers = [center(i) for i in range(n)]
    for i, item in enumerate(items):
        cx, cy, r, cc = centers[i]
        fc = colors[i] if colors else NAVY
        rbox(ax, cx, cy, box_w, box_h, item, fc=fc, fs=fs)
    # arrows following reading order
    for i in range(n - 1):
        x1, y1, r1, _ = centers[i]
        x2, y2, r2, _ = centers[i + 1]
        if r1 == r2:
            if x2 > x1:
                arrow(ax, x1 + box_w / 2, y1, x2 - box_w / 2, y2)
            else:
                arrow(ax, x1 - box_w / 2, y1, x2 + box_w / 2, y2)
        else:  # wrap down
            arrow(ax, x1, y1 - box_h / 2, x2, y2 + box_h / 2)
    _save(fig, name)


def horizontal_timeline(phases, name, box_w=3.0, box_h=1.9, gap=0.85, fs=11.5):
    """Phases laid left-to-right with connecting arrows. Each phase = (title, sub)."""
    n = len(phases)
    W = n * box_w + (n - 1) * gap
    fig, ax = _new((W + 0.6, box_h + 1.0))
    ax.set_xlim(0, W + 0.6)
    ax.set_ylim(0, box_h + 1.0)
    cy = (box_h + 1.0) / 2
    ox = 0.3
    for i, (ttl, sub) in enumerate(phases):
        cx = ox + i * (box_w + gap) + box_w / 2
        rbox(ax, cx, cy, box_w, box_h, "", fc=NAVY)
        ax.text(cx, cy + box_h / 2 - 0.42, ttl, ha="center", va="center",
                color=WHITE, fontsize=fs + 0.5, fontweight="bold")
        ax.text(cx, cy - 0.15, sub, ha="center", va="center", color=PALE,
                fontsize=fs - 0.5, wrap=True, linespacing=1.2)
        if i < n - 1:
            arrow(ax, cx + box_w / 2, cy, cx + box_w / 2 + gap, cy)
    _save(fig, name)


def doughnut(data, name, title=None, figsize=(6.6, 5.0), start=90):
    labels = list(data.keys())
    values = list(data.values())
    colors = [DOUGHNUT_PALETTE[i % len(DOUGHNUT_PALETTE)] for i in range(len(values))]
    fig, ax = plt.subplots(figsize=figsize)
    wedges, _texts, autos = ax.pie(
        values, colors=colors, startangle=start, counterclock=False,
        wedgeprops=dict(width=0.42, edgecolor="white", linewidth=2),
        autopct="%1.0f%%", pctdistance=0.78,
    )
    for a in autos:
        a.set_color("white")
        a.set_fontsize(10.5)
        a.set_fontweight("bold")
    # legend labels with values
    leg = [f"{l}  ({v}%)" for l, v in zip(labels, values)]
    ax.legend(wedges, leg, loc="center left", bbox_to_anchor=(0.98, 0.5),
              frameon=False, fontsize=10.5)
    if title:
        ax.set_title(title, fontsize=13, fontweight="bold", color=NAVY, pad=12)
    ax.set_aspect("equal")
    _save(fig, name, pad=0.15)


def radial(center_label, nodes, name, figsize=(7.2, 6.4)):
    fig, ax = _new(figsize)
    ax.set_xlim(-5.2, 5.2)
    ax.set_ylim(-5.0, 5.0)
    R = 3.5
    n = len(nodes)
    # center
    c = Circle((0, 0), 1.35, facecolor=NAVY, edgecolor=NAVY_DK, lw=2, zorder=3)
    ax.add_patch(c)
    ax.text(0, 0, center_label, ha="center", va="center", color=WHITE,
            fontsize=12, fontweight="bold", wrap=True, zorder=4, linespacing=1.2)
    for i, node in enumerate(nodes):
        ang = math.pi / 2 - i * 2 * math.pi / n
        x = R * math.cos(ang)
        y = R * math.sin(ang)
        arrow(ax, 0.0, 0.0, x * 0.60, y * 0.60, color=STEEL, lw=1.8, ms=12)
        col = DOUGHNUT_PALETTE[i % len(DOUGHNUT_PALETTE)]
        tc = WHITE if col in (NAVY, NAVY_MD, STEEL) else NAVY
        node_r = 1.15
        cc = Circle((x, y), node_r, facecolor=col, edgecolor="white", lw=1.6, zorder=3)
        ax.add_patch(cc)
        ax.text(x, y, node, ha="center", va="center", color=tc, fontsize=9.8,
                fontweight="bold", wrap=True, zorder=4, linespacing=1.15)
    _save(fig, name)


def matrix_2x2(name, xlabel, ylabel, quadrants, highlight_idx=3,
               figsize=(7.4, 6.4)):
    """quadrants: list of 4 labels ordered [BL, BR, TL, TR] i.e.
    index0=low/low, 1=high-x/low-y, 2=low-x/high-y, 3=high/high."""
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_xticks([])
    ax.set_yticks([])
    # quadrant shading
    ax.add_patch(plt.Rectangle((0, 0), 5, 5, facecolor=LIGHT, zorder=0))
    ax.add_patch(plt.Rectangle((5, 0), 5, 5, facecolor=PALE, zorder=0))
    ax.add_patch(plt.Rectangle((0, 5), 5, 5, facecolor=PALE, zorder=0))
    ax.add_patch(plt.Rectangle((5, 5), 5, 5, facecolor=MIST, zorder=0))
    ax.axhline(5, color=LGREY, lw=1.2, zorder=1)
    ax.axvline(5, color=LGREY, lw=1.2, zorder=1)
    # axis arrows
    ax.annotate("", xy=(10, 0), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=2))
    ax.annotate("", xy=(0, 10), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=2))
    ax.set_xlabel(xlabel, fontsize=12, fontweight="bold", color=NAVY, labelpad=8)
    ax.set_ylabel(ylabel, fontsize=12, fontweight="bold", color=NAVY, labelpad=8)
    centers = [(2.5, 2.5), (7.5, 2.5), (2.5, 7.5), (7.5, 7.5)]
    for i, (label) in enumerate(quadrants):
        cx, cy = centers[i]
        if i == highlight_idx:
            rbox(ax, cx, cy, 3.6, 1.5, label, fc=NAVY, tc=WHITE, fs=12,
                 round_size=0.12)
        else:
            rbox(ax, cx, cy, 3.4, 1.3, label, fc=WHITE, ec=STEEL, tc=NAVY,
                 fs=11, round_size=0.12, lw=1.4)
    for spine in ax.spines.values():
        spine.set_visible(False)
    _save(fig, name)


def swot(name, strengths, weaknesses, opportunities, threats, figsize=(9.2, 8.4)):
    fig, ax = _new(figsize)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    cell = 4.7
    gap = 0.2
    quads = [
        ("STRENGTHS", strengths, (0.1, 5.1), NAVY),
        ("WEAKNESSES", weaknesses, (5.2, 5.1), NAVY_MD),
        ("OPPORTUNITIES", opportunities, (0.1, 0.1), STEEL),
        ("THREATS", threats, (5.2, 0.1), NAVY_DK),
    ]
    for ttl, items, (x, y), col in quads:
        # panel
        panel = FancyBboxPatch((x, y), cell, cell,
                               boxstyle="round,pad=0.0,rounding_size=0.10",
                               facecolor=WHITE, edgecolor=col, linewidth=1.8, zorder=2)
        ax.add_patch(panel)
        # header band
        hb = FancyBboxPatch((x, y + cell - 0.85), cell, 0.85,
                            boxstyle="round,pad=0.0,rounding_size=0.10",
                            facecolor=col, edgecolor=col, zorder=3)
        ax.add_patch(hb)
        ax.text(x + cell / 2, y + cell - 0.42, ttl, ha="center", va="center",
                color=WHITE, fontsize=13, fontweight="bold", zorder=4)
        body = "\n".join(f"\u2022  {it}" for it in items)
        ax.text(x + 0.28, y + cell - 1.1, body, ha="left", va="top",
                color=GREY, fontsize=9.6, zorder=4, linespacing=1.5)
    _save(fig, name)


def pyramid(layers, name, figsize=(7.6, 5.6)):
    """layers: bottom-to-top list of labels. Draws a stacked pyramid."""
    fig, ax = _new(figsize)
    n = len(layers)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, n + 0.6)
    apex_x = 5.0
    base_half = 4.6
    layer_h = 1.0
    for i, label in enumerate(layers):
        y0 = i * layer_h + 0.2
        y1 = y0 + layer_h * 0.9
        # widths shrink toward top
        w_bot = base_half * (1 - i / n)
        w_top = base_half * (1 - (i + 1) / n)
        poly = Polygon([(apex_x - w_bot, y0), (apex_x + w_bot, y0),
                        (apex_x + w_top, y1), (apex_x - w_top, y1)],
                       closed=True, facecolor=DOUGHNUT_PALETTE[(n - 1 - i) % len(DOUGHNUT_PALETTE)],
                       edgecolor="white", linewidth=2, zorder=3)
        ax.add_patch(poly)
        tc = WHITE if i < n - 2 else NAVY
        ax.text(apex_x, (y0 + y1) / 2, label, ha="center", va="center",
                color=tc, fontsize=11, fontweight="bold", zorder=4)
    _save(fig, name)


def funnel(stages, name, figsize=(7.0, 7.2)):
    fig, ax = _new(figsize)
    n = len(stages)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, n * 1.15 + 0.4)
    top_half = 4.4
    bot_half = 1.3
    seg_h = 1.0
    gap = 0.12
    for i, label in enumerate(stages):
        frac_top = i / n
        frac_bot = (i + 1) / n
        w_top = top_half - (top_half - bot_half) * frac_top
        w_bot = top_half - (top_half - bot_half) * frac_bot
        y_top = (n - i) * (seg_h + gap)
        y_bot = y_top - seg_h
        col = DOUGHNUT_PALETTE[i % len(DOUGHNUT_PALETTE)]
        poly = Polygon([(5 - w_top, y_top), (5 + w_top, y_top),
                        (5 + w_bot, y_bot), (5 - w_bot, y_bot)],
                       closed=True, facecolor=col, edgecolor="white",
                       linewidth=2, zorder=3)
        ax.add_patch(poly)
        tc = WHITE if col in (NAVY, NAVY_MD, STEEL, NAVY_DK) else NAVY
        ax.text(5, (y_top + y_bot) / 2, label, ha="center", va="center",
                color=tc, fontsize=10.5, fontweight="bold", zorder=4)
    _save(fig, name)


def circular_cycle(nodes, name, figsize=(7.2, 6.8)):
    fig, ax = _new(figsize)
    ax.set_xlim(-5.4, 5.4)
    ax.set_ylim(-5.2, 5.2)
    R = 3.5
    n = len(nodes)
    pts = []
    for i, node in enumerate(nodes):
        ang = math.pi / 2 - i * 2 * math.pi / n
        x = R * math.cos(ang)
        y = R * math.sin(ang)
        pts.append((x, y))
    # curved arrows between consecutive nodes
    for i in range(n):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % n]
        arrow(ax, x1 * 0.82, y1 * 0.82, x2 * 0.82, y2 * 0.82,
              color=STEEL, lw=2.0, ms=14, rad=-0.25)
    for i, node in enumerate(nodes):
        x, y = pts[i]
        col = DOUGHNUT_PALETTE[i % len(DOUGHNUT_PALETTE)]
        tc = WHITE if col in (NAVY, NAVY_MD, STEEL) else NAVY
        cc = Circle((x, y), 1.12, facecolor=col, edgecolor="white", lw=1.8, zorder=3)
        ax.add_patch(cc)
        ax.text(x, y, node, ha="center", va="center", color=tc, fontsize=10,
                fontweight="bold", wrap=True, zorder=4, linespacing=1.15)
    _save(fig, name)


def hierarchy(root, children, name, figsize=(9.0, 5.2), sub=None):
    """root -> children (list). Optional sub: dict child_index -> [subnodes]."""
    fig, ax = _new(figsize)
    n = len(children)
    W = 10.0
    ax.set_xlim(0, W)
    ax.set_ylim(0, 6.0)
    # root
    rbox(ax, W / 2, 5.3, 3.0, 0.9, root, fc=NAVY, fs=12.5)
    xs = np.linspace(1.4, W - 1.4, n)
    for i, ch in enumerate(children):
        cx = xs[i]
        rbox(ax, cx, 3.4, 2.2, 0.95, ch, fc=STEEL, fs=10.5)
        arrow(ax, W / 2, 5.3 - 0.45, cx, 3.4 + 0.48, color=NAVY, lw=1.8, ms=13)
        if sub and i in sub:
            rbox(ax, cx, 1.5, 2.2, 0.95, sub[i], fc=MIST, tc=NAVY, fs=10)
            arrow(ax, cx, 3.4 - 0.48, cx, 1.5 + 0.48, color=STEEL, lw=1.6, ms=12)
    _save(fig, name)


def org_chart(name, figsize=(9.4, 7.4)):
    fig, ax = _new(figsize)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10)
    md = (6, 9.2)
    rbox(ax, md[0], md[1], 4.0, 0.95, "Managing Director", fc=NAVY, fs=12)
    mids = [
        (2.4, 7.3, "Operations\nManager"),
        (6.0, 7.3, "Finance &\nAdministration"),
        (9.6, 7.3, "Business\nDevelopment"),
    ]
    for x, y, t in mids:
        rbox(ax, x, y, 2.7, 1.0, t, fc=STEEL, fs=10.5)
        arrow(ax, md[0], md[1] - 0.45, x, y + 0.5, color=NAVY, lw=1.7, ms=12)
    # second level
    subs = [
        (2.4, 5.5, "Project Managers"),
        (6.0, 5.5, "Accounts & HR"),
        (9.6, 5.5, "Sales & Marketing"),
    ]
    for i, (x, y, t) in enumerate(subs):
        rbox(ax, x, y, 2.7, 0.9, t, fc=MIST, tc=NAVY, fs=10)
        arrow(ax, mids[i][0], mids[i][1] - 0.5, x, y + 0.45, color=STEEL, lw=1.5, ms=11)
    # operations vertical chain
    chain = ["Site Engineers", "Site Supervisors", "Skilled Workforce"]
    px, py = 2.4, 5.5
    for t in chain:
        ny = py - 1.55
        rbox(ax, 2.4, ny, 2.7, 0.85, t, fc=PALE, tc=NAVY, fs=10, lw=1.2)
        arrow(ax, 2.4, py - 0.45, 2.4, ny + 0.43, color=SKY, lw=1.4, ms=10)
        py = ny
    _save(fig, name)


def canvas_9block(blocks, name, figsize=(11.0, 7.4)):
    """blocks: dict with keys kp, ka, vp, cr, cs, kr, ch, cost, rev (title,[items])."""
    fig, ax = _new(figsize)
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 10)

    def block(x, y, w, h, key):
        ttl, items = blocks[key]
        panel = FancyBboxPatch((x, y), w, h,
                               boxstyle="round,pad=0.0,rounding_size=0.06",
                               facecolor=WHITE, edgecolor=NAVY, linewidth=1.4, zorder=2)
        ax.add_patch(panel)
        hb = FancyBboxPatch((x, y + h - 0.62), w, 0.62,
                            boxstyle="round,pad=0.0,rounding_size=0.06",
                            facecolor=NAVY, edgecolor=NAVY, zorder=3)
        ax.add_patch(hb)
        ax.text(x + w / 2, y + h - 0.31, ttl, ha="center", va="center",
                color=WHITE, fontsize=7.6, fontweight="bold", zorder=4)
        body = "\n".join(f"\u2022 {it}" for it in items)
        ax.text(x + 0.14, y + h - 0.78, body, ha="left", va="top",
                color=GREY, fontsize=7.6, zorder=4, linespacing=1.4)

    # top band split into 5 columns of varying height
    # Layout (Osterwalder): KP | KA/KR | VP | CR/CH | CS
    block(0.1, 3.4, 2.85, 6.4, "kp")
    block(3.05, 6.6, 2.85, 3.2, "ka")
    block(3.05, 3.4, 2.85, 3.1, "kr")
    block(6.0, 3.4, 2.9, 6.4, "vp")
    block(8.95, 6.6, 2.85, 3.2, "cr")
    block(8.95, 3.4, 2.85, 3.1, "ch")
    block(11.9, 3.4, 3.0, 6.4, "cs")
    # bottom band: cost (left half) + revenue (right half)
    block(0.1, 0.1, 7.3, 3.2, "cost")
    block(7.5, 0.1, 7.4, 3.2, "rev")
    _save(fig, name)


def grouped_bar(name, years, series, colors, ylabel="\u20b9 Crore",
                figsize=(7.6, 4.4), fmt="{:.2f}"):
    fig, ax = plt.subplots(figsize=figsize)
    x = np.arange(len(years))
    keys = list(series.keys())
    m = len(keys)
    w = 0.8 / m
    for j, k in enumerate(keys):
        vals = series[k]
        bars = ax.bar(x + (j - (m - 1) / 2) * w, vals, width=w, label=k,
                      color=colors[j], edgecolor="white", linewidth=0.6, zorder=3)
        for b, v in zip(bars, vals):
            ax.text(b.get_x() + b.get_width() / 2, v, "\u20b9" + fmt.format(v),
                    ha="center", va="bottom", fontsize=8.2, color=GREY,
                    fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(years, fontsize=11)
    ax.set_ylabel(ylabel, fontsize=10.5, color=GREY)
    ax.set_ylim(0, max(max(v) for v in series.values()) * 1.22)
    ax.grid(axis="y", color="#E2E7EE", linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    ax.legend(frameon=False, fontsize=10, loc="upper left")
    _save(fig, name, pad=0.15)


def breakeven_line(name, years, revenue, cost, figsize=(7.6, 4.6)):
    fig, ax = plt.subplots(figsize=figsize)
    x = np.arange(len(years))
    ax.plot(x, revenue, marker="o", color=NAVY, lw=2.6, label="Revenue", zorder=3)
    ax.plot(x, cost, marker="s", color=GOLD, lw=2.6, label="Total Cost", zorder=3)
    ax.fill_between(x, revenue, cost, where=[r >= c for r, c in zip(revenue, cost)],
                    interpolate=True, color=GREEN, alpha=0.12, zorder=1)
    # break-even marker near first crossing / year 1
    ax.annotate("Break-even\n(Year 1)", xy=(0, revenue[0]), xytext=(0.35, revenue[0] + 1.4),
                fontsize=9.5, color=NAVY, fontweight="bold",
                arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=1.5))
    ax.set_xticks(x)
    ax.set_xticklabels(years, fontsize=11)
    ax.set_ylabel("\u20b9 Crore", fontsize=10.5, color=GREY)
    ax.grid(color="#E2E7EE", linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    ax.legend(frameon=False, fontsize=10, loc="upper left")
    _save(fig, name, pad=0.15)


def risk_matrix(name, risks, xlabel="Probability  (Low \u2192 High)",
                ylabel="Impact  (Low \u2192 High)", figsize=(8.0, 6.8)):
    """risks: list of (label, x, y, high_flag) with x,y in 0..10."""
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.add_patch(plt.Rectangle((0, 0), 5, 5, facecolor="#EAF0F8", zorder=0))
    ax.add_patch(plt.Rectangle((5, 0), 5, 5, facecolor="#DCE7F5", zorder=0))
    ax.add_patch(plt.Rectangle((0, 5), 5, 5, facecolor="#DCE7F5", zorder=0))
    ax.add_patch(plt.Rectangle((5, 5), 5, 5, facecolor="#C2D4EC", zorder=0))
    ax.axhline(5, color=LGREY, lw=1.0, zorder=1)
    ax.axvline(5, color=LGREY, lw=1.0, zorder=1)
    ax.annotate("", xy=(10, 0), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=2))
    ax.annotate("", xy=(0, 10), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=2))
    ax.set_xlabel(xlabel, fontsize=11.5, fontweight="bold", color=NAVY, labelpad=8)
    ax.set_ylabel(ylabel, fontsize=11.5, fontweight="bold", color=NAVY, labelpad=8)
    for label, x, y, high in risks:
        fc = NAVY if high else STEEL
        rbox(ax, x, y, 2.9, 0.95, label, fc=fc, tc=WHITE, fs=9.2,
             round_size=0.12, lw=1.2)
    for s in ax.spines.values():
        s.set_visible(False)
    _save(fig, name)


def dashboard(name, gauges, bars, figsize=(9.2, 5.2)):
    """gauges: list of (label, pct). bars: list of (label, pct)."""
    fig = plt.figure(figsize=figsize)
    fig.patch.set_facecolor("white")
    n_g = len(gauges)
    # top row gauges
    for i, (label, pct) in enumerate(gauges):
        ax = fig.add_axes([0.04 + i * (0.92 / n_g), 0.52, 0.92 / n_g - 0.03, 0.4])
        ax.set_axis_off()
        ax.set_aspect("equal")
        ax.set_xlim(-1.2, 1.2)
        ax.set_ylim(-0.2, 1.3)
        ax.add_patch(Wedge((0, 0), 1.0, 0, 180, width=0.34, facecolor="#E4E9F1"))
        ax.add_patch(Wedge((0, 0), 1.0, 180 - 180 * pct / 100, 180, width=0.34,
                           facecolor=NAVY))
        ax.text(0, 0.28, f"{pct}%", ha="center", va="center", fontsize=15,
                fontweight="bold", color=NAVY)
        ax.text(0, -0.12, label, ha="center", va="center", fontsize=9.2,
                color=GREY, wrap=True)
    # bottom row horizontal progress bars
    axb = fig.add_axes([0.08, 0.06, 0.86, 0.36])
    axb.set_axis_off()
    axb.set_xlim(0, 100)
    axb.set_ylim(0, len(bars))
    for i, (label, pct) in enumerate(bars):
        y = len(bars) - 1 - i + 0.15
        axb.add_patch(plt.Rectangle((28, y), 68, 0.55, facecolor="#E4E9F1"))
        axb.add_patch(plt.Rectangle((28, y), 68 * pct / 100, 0.55, facecolor=STEEL))
        axb.text(0, y + 0.27, label, ha="left", va="center", fontsize=9.2, color=GREY)
        axb.text(97, y + 0.27, f"{pct}%", ha="left", va="center", fontsize=9,
                 color=NAVY, fontweight="bold")
    _save(fig, name, pad=0.12)


# ============================================================================
# FIGURE DEFINITIONS
# ============================================================================
def build_all():
    # Fig 1 - Executive Business Overview
    vertical_flow(["Customer Needs", "Professional Planning", "Quality Construction",
                   "Technology Integration", "Customer Satisfaction", "Business Growth"],
                  "fig01.png")

    # Fig 2 - Phased Business Growth Strategy (timeline)
    horizontal_timeline([("Phase 1", "Residential\nConstruction"),
                         ("Phase 2", "Commercial\nProjects"),
                         ("Phase 3", "Technology\nIntegration"),
                         ("Phase 4", "Multi-City\nExpansion")], "fig02.png")

    # Fig 3 - BuildWise Business Foundation
    vertical_flow(["Customer Trust", "Quality Construction", "Transparent Operations",
                   "Technology Integration", "Long-Term Growth"], "fig03.png")

    # Fig 4 - Phased Business Growth Philosophy
    vertical_flow(["Customer Trust", "Operational Excellence", "Financial Stability",
                   "Technology Integration", "Regional Expansion", "National Brand"],
                  "fig04.png")

    # Fig 5 - Key Growth Drivers (radial)
    radial("Construction\nIndustry\nGrowth",
           ["Urbanization", "Population\nGrowth", "Government\nInfrastructure",
            "Smart Cities", "Housing\nDemand", "Commercial\nDevelopment"], "fig05.png")

    # Fig 6 - Customer Segmentation Framework
    vertical_flow(["Residential  \u2014  Affordable homes", "Commercial  \u2014  Offices & retail",
                   "SMEs  \u2014  Cost-effective spaces",
                   "Institutions  \u2014  Durable infrastructure",
                   "Investors  \u2014  End-to-end management"], "fig06.png",
                  box_w=7.0, fs=11.5)

    # Fig 7 - Customer Decision Journey
    snake_flow(["Need Identified", "Quotation", "Project Planning", "Construction",
                "Quality Inspection", "Handover", "Warranty Support"], "fig07.png",
               cols=4)

    # Fig 8 - Root Cause Analysis
    vertical_flow(["Poor Planning", "Weak Communication", "Manual Processes",
                   "Limited Quality Checks", "Customer Dissatisfaction"], "fig08.png")

    # Fig 9 - Problem -> Solution -> Customer Value
    vertical_flow(["Industry Problems", "BuildWise Solutions", "Customer Satisfaction",
                   "Business Growth"], "fig09.png", box_w=6.4, box_h=1.1,
                  colors=[RED, NAVY, STEEL, GREEN])

    # Fig 10 - Value Creation Model
    vertical_flow(["Customer Requirements", "Transparent Planning", "Quality Construction",
                   "Continuous Communication", "Customer Satisfaction", "Long-Term Trust"],
                  "fig10.png")

    # Fig 11 - Competitive Positioning Matrix
    matrix_2x2("fig11.png", "Price Transparency  (Low \u2192 High)",
               "Project Quality  (Low \u2192 High)",
               ["Local Contractors", "Small Builders", "Large Construction Firms",
                "BuildWise"], highlight_idx=3)

    # Fig 12 - Service Ecosystem
    hierarchy("BuildWise",
              ["Residential", "Commercial", "Interior"], "fig12.png",
              sub={0: "Renovation", 1: "Consultancy", 2: "Maintenance"})

    # Fig 13 - Service Delivery Workflow
    snake_flow(["Customer Enquiry", "Consultation & Site Visit", "Requirement Analysis",
                "Detailed Quotation", "Project Planning", "Agreement & Approval",
                "Construction Execution", "Stage-wise Inspection", "Final Handover",
                "Warranty & Support"], "fig13.png", cols=4)

    # Fig 14 - Customer Value Pyramid
    pyramid(["Professional Planning", "Transparent Communication", "Quality Construction",
             "Customer Satisfaction", "Customer Loyalty"], "fig14.png")

    # Fig 15 - Business Model Canvas
    canvas_9block({
        "kp": ("KEY PARTNERS", ["Material Suppliers", "Architects", "Structural Engineers",
                                "Interior Designers", "Financial Institutions", "Govt. Authorities"]),
        "ka": ("KEY ACTIVITIES", ["Construction", "Project Planning", "Cost Estimation",
                                  "Site Supervision", "Quality Inspection"]),
        "kr": ("KEY RESOURCES", ["Skilled Workforce", "Engineering Team", "Equipment",
                                 "Technology Platform", "Supplier Network"]),
        "vp": ("VALUE PROPOSITION", ["Transparent Pricing", "Quality Construction",
                                     "Timely Delivery", "Professional Management",
                                     "Long-Term Warranty", "Technology Integration"]),
        "cr": ("CUSTOMER RELATIONS", ["Dedicated Manager", "Weekly Updates",
                                          "Digital Docs", "Warranty Support"]),
        "ch": ("CHANNELS", ["Company Website", "Social Media", "Referral Network",
                            "Architects", "Real-Estate Consultants"]),
        "cs": ("CUSTOMER SEGMENTS", ["Homeowners", "SMEs", "Commercial Clients",
                                     "Property Investors", "Institutions"]),
        "cost": ("COST STRUCTURE", ["Material Procurement", "Employee Salaries", "Equipment",
                                    "Marketing", "Administration", "Technology Investment"]),
        "rev": ("REVENUE STREAMS", ["Residential Projects", "Commercial Projects",
                                    "Interior Works", "Renovation", "Consultancy",
                                    "Maintenance Contracts"]),
    }, "fig15.png")

    # Fig 16 - Revenue Distribution (doughnut)
    doughnut({"Residential Construction": 40, "Commercial Construction": 25,
              "Interior Design": 12, "Renovation": 10, "Consultancy": 8,
              "Maintenance": 5}, "fig16.png")

    # Fig 17 - Business Process Workflow
    snake_flow(["Customer Enquiry", "Site Visit & Analysis", "Estimation & Quotation",
                "Client Approval", "Project Planning", "Material Procurement",
                "Construction Execution", "Quality Inspection", "Project Handover",
                "Warranty & Relationship"], "fig17.png", cols=4)

    # Fig 18 - Cost Allocation (doughnut)
    doughnut({"Construction Materials": 50, "Labour & Workforce": 20,
              "Equipment & Machinery": 10, "Administration": 8,
              "Marketing": 5, "Technology": 4, "Contingency": 3}, "fig18.png")

    # Fig 19 - Competitive Positioning Matrix (Chapter 7)
    matrix_2x2("fig19.png", "Customer Transparency  (Low \u2192 High)",
               "Construction Quality  (Low \u2192 High)",
               ["Local Contractors", "Regional Builders", "National Companies",
                "BuildWise"], highlight_idx=3)

    # Fig 20 - SWOT
    swot("fig20.png",
         ["Transparent milestone billing", "Strong customer communication",
          "Structured project management", "Technology-ready model",
          "Long-term warranty support", "Scalable phased growth"],
         ["New market entrant", "Initial local dependence",
          "Limited financial resources", "Gradual tech implementation"],
         ["Rapid urban development", "Demand for transparency",
          "Digital construction adoption", "Government infrastructure push",
          "Commercial expansion"],
         ["Fluctuating material prices", "Intense competition",
          "Economic slowdown", "Skilled labour shortage",
          "Regulatory / approval delays"])

    # Fig 21 - Competitive Advantage Framework
    vertical_flow(["Customer Trust", "Operational Excellence", "Consistent Quality",
                   "Positive Reputation", "Customer Referrals", "Business Growth"],
                  "fig21.png")

    # Fig 22 - Marketing Channel Ecosystem
    hierarchy("BuildWise",
              ["Website", "Social Media", "Google Profile"], "fig22.png",
              sub={0: "Architects", 1: "Referrals", 2: "Property Consultants"})

    # Fig 23 - Customer Acquisition Funnel
    funnel(["Brand Awareness", "Customer Enquiries", "Site Visit",
            "Requirement Discussion", "Quotation", "Negotiation",
            "Project Confirmation", "Customer Relationship"], "fig23.png")

    # Fig 24 - Customer Relationship Lifecycle
    circular_cycle(["Awareness", "Enquiry", "Consultation", "Construction",
                    "Project Delivery", "Warranty Support", "Referral",
                    "Repeat Business"], "fig24.png")

    # Fig 25 - Construction Workflow
    snake_flow(["Customer Enquiry", "Site Inspection", "Requirement Analysis",
                "Cost Estimation", "Quotation Approval", "Project Planning",
                "Material Procurement", "Construction Execution", "Quality Inspection",
                "Final Handover", "Warranty Support"], "fig25.png", cols=4)

    # Fig 26 - Material Procurement Cycle
    vertical_flow(["Vendor Selection", "Quotation Comparison", "Purchase Order",
                   "Material Delivery", "Quality Verification", "Inventory Recording",
                   "Site Allocation"], "fig26.png", box_h=0.92, gap=0.5)

    # Fig 27 - Quality Assurance Framework
    vertical_flow(["Foundation Inspection", "Structural Quality Check",
                   "Electrical & Plumbing Inspection", "Finishing Inspection",
                   "Final Quality Audit", "Customer Approval"], "fig27.png")

    # Fig 28 - Project Monitoring Dashboard
    dashboard("fig28.png",
              gauges=[("Project Progress", 68), ("Budget Utilization", 61),
                      ("Quality Inspection", 90)],
              bars=[("Material Status", 74), ("Safety Compliance", 96),
                    ("Customer Satisfaction", 88)])

    # Fig 29 - Customer Journey Lifecycle
    snake_flow(["Project Enquiry", "Initial Consultation", "Site Visit & Requirements",
                "Quotation & Planning", "Construction Execution", "Weekly Updates",
                "Quality Inspection", "Project Handover", "Warranty Support",
                "Customer Feedback", "Referral & Repeat Business"], "fig29.png", cols=4)

    # Fig 30 - Customer Relationship Cycle
    circular_cycle(["Trust", "Quality", "Satisfaction", "Referral",
                    "Repeat Customer", "Brand Growth"], "fig30.png")

    # Fig 31 - Organizational Hierarchy
    org_chart("fig31.png")

    # Fig 32 - Startup Capital Allocation (doughnut)
    doughnut({"Initial Material Procurement": 20, "Construction Equipment": 18,
              "Working Capital Reserve": 15, "Salaries & Recruitment": 15,
              "Office Setup": 12, "Marketing": 8, "Technology": 7,
              "Legal & Misc.": 5}, "fig32.png")

    # Fig 33 - Revenue vs Expenses vs Profit
    grouped_bar("fig33.png", ["Year 1", "Year 2", "Year 3"],
                {"Revenue": [2.02, 4.85, 8.76],
                 "Expenses": [1.92, 4.42, 8.10],
                 "Net Profit": [0.10, 0.43, 0.66]},
                colors=[NAVY, STEEL, GOLD])

    # Fig 34 - Revenue Mix (doughnut)
    doughnut({"Residential Construction": 40, "Commercial Construction": 25,
              "Interior Design": 12, "Renovation Projects": 10,
              "Consultancy Services": 8, "Annual Maintenance": 5}, "fig34.png")

    # Fig 35 - Break-even Analysis
    breakeven_line("fig35.png", ["Year 1", "Year 2", "Year 3"],
                   revenue=[2.02, 4.85, 8.76], cost=[1.92, 4.42, 8.10])

    # Fig 36 - Financial Sustainability Framework
    vertical_flow(["Investment", "Operational Efficiency", "Revenue Growth",
                   "Profitability", "Business Expansion", "Long-Term Sustainability"],
                  "fig36.png")

    # Fig 37 - Risk Assessment Matrix
    risk_matrix("fig37.png", [
        ("Material Price\nFluctuation", 7.9, 8.3, True),
        ("Cash Flow\nConstraints", 5.0, 6.6, True),
        ("Project Delays", 5.7, 4.5, False),
        ("Labour Shortage", 2.2, 5.7, False),
        ("Regulatory\nChanges", 1.9, 3.9, False),
        ("Safety Incidents", 3.7, 2.5, False),
    ])

    # Fig 38 - Risk Management Cycle
    circular_cycle(["Identify Risks", "Assess Impact", "Plan Mitigation",
                    "Implement Controls", "Monitor Performance", "Review & Improve"],
                   "fig38.png")

    # Fig 39 - Technology Roadmap timeline
    horizontal_timeline([
        ("Phase 1", "Digital Docs\nCloud Storage\nProject Mgmt"),
        ("Phase 2", "AI Cost\nEstimation\nQR Tracking"),
        ("Phase 3", "Drone\nMonitoring\nDashboards"),
        ("Phase 4", "IoT Smart\nHomes\nPredictive"),
    ], "fig39.png", box_w=3.0, box_h=2.3)

    # Fig 40 - Digital Construction Ecosystem
    hierarchy("BuildWise",
              ["AI Estimation", "QR Tracking", "Drone Monitoring"], "fig40.png",
              sub={0: "Dashboard", 1: "Cloud Docs", 2: "IoT Homes"})

    # Fig 41 - Five-Year Business Growth Roadmap
    horizontal_timeline([
        ("2026", "Launch"),
        ("2027", "Residential\nGrowth"),
        ("2028", "Commercial\nExpansion"),
        ("2029", "Technology\nIntegration"),
        ("2030", "Multi-City\nPresence"),
        ("2031", "National\nBrand"),
    ], "fig41.png", box_w=2.3, box_h=1.7, gap=0.7)

    # Fig 42 - Sustainability Framework
    vertical_flow(["Environmental Responsibility", "Efficient Resource Utilization",
                   "Reduced Waste", "Energy Efficiency", "Customer Value",
                   "Sustainable Business Growth"], "fig42.png")

    # Fig 43 - BuildWise Success Framework
    vertical_flow(["Customer Trust", "Quality Construction", "Operational Excellence",
                   "Technology Integration", "Business Growth",
                   "National Brand Recognition"], "fig43.png")

    print("All figures written to", OUT)


if __name__ == "__main__":
    build_all()
